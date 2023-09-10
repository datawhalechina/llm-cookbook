"""Helper functions."""

import string
from enum import Enum
from typing import Any, Dict, List, Set, Tuple, Union


TRUTH_TEXT = frozenset(("t", "true", "y", "yes", "on", "1"))
FALSE_TEXT = frozenset(("f", "false", "n", "no", "off", "0", ""))
PROTECTED_KEYS = frozenset(("secret", "password", "passwd", "pwd", "token"))

InterpolateType = Union[bool, Dict[str, str]]


class InterpolateEnumType(Enum):
    """Interpolation Method."""

    # standard matching
    STANDARD = 0
    # interpolation will look through lower levels to attempt to resolve variables.
    # This is particularly useful for templating
    DEEP = 1
    # similar to DEEP, but interpolating will not backtrack levels.
    # That is, lower levels cannot use values from higher levels.
    DEEP_NO_BACKTRACK = 2


class AttributeDict(dict):
    """Dictionary subclass enabling attribute lookup/assignment of keys/values."""

    def __getattr__(self, key: Any) -> Any:  # noqa: D105
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)

    def __setattr__(self, key: Any, value: Any) -> None:  # noqa: D105
        self[key] = value


def as_bool(s: Any) -> bool:
    """
    Boolean value from an object.

    Return the boolean value ``True`` if the case-lowered value of string
    input ``s`` is a `truthy string`. If ``s`` is already one of the
    boolean values ``True`` or ``False``, return it.
    """
    if s is None:
        return False
    if isinstance(s, bool):
        return s
    s = str(s).strip().lower()
    if s not in TRUTH_TEXT and s not in FALSE_TEXT:
        raise ValueError("Expected a valid True or False expression.")
    return s in TRUTH_TEXT


def clean(key: str, value: Any, mask: str = "******") -> Any:
    """
    Mask a value if needed.

    :param key: key
    :param value: value to hide
    :param mask: string to use in case value should be hidden
    :return: clear value or mask
    """
    key = key.lower()
    # check for protected keys
    for pk in PROTECTED_KEYS:
        if pk in key:
            return mask
    # urls
    if isinstance(value, str) and "://" in value:
        from urllib.parse import urlparse

        url = urlparse(value)
        if url.password is None:
            return value
        else:
            return url._replace(
                netloc="{}:{}@{}".format(url.username, mask, url.hostname)
            ).geturl()
    return value


def interpolate_standard(text: str, d: dict, found: Set[Tuple[str, ...]]) -> str:
    """
    Return the string interpolated as many times as needed.

    :param text: string possibly containing an interpolation pattern
    :param d: dictionary
    :param found: variables found so far
    """
    if not isinstance(text, str):
        return text

    variables = tuple(
        sorted(x[1] for x in string.Formatter().parse(text) if x[1] is not None)
    )

    if not variables:
        return text

    if variables in found:
        raise ValueError("Cycle detected while interpolating keys")
    else:
        found.add(variables)

    interpolated = {v: interpolate_standard(d[v], d, found) for v in variables}
    return text.format(**interpolated)


def interpolate_deep(
    attr: str,
    text: str,
    d: List[dict],
    resolved: Dict[str, str],
    levels: Dict[str, int],
    method: InterpolateEnumType,
) -> str:
    """
    Return the string interpolated as many times as needed.

    :param attr: attribute name
    :param text: string possibly containing an interpolation pattern
    :param d: dictionary
    :param resolved: variables resolved so far
    :param levels: last level to read the variable from
    """
    if not isinstance(text, str):
        return text

    variables = {x[1] for x in string.Formatter().parse(text) if x[1] is not None}

    if not variables:
        return text

    length = len(d)

    for variable in variables.difference(resolved.keys()):
        # start at 1 if this is the intended attribute
        level = levels.setdefault(variable, 1 if variable == attr else 0)
        # get the first level for which the variable is defined
        if level == length:
            raise KeyError(variable)
        for i, dict_ in enumerate(d[level:]):
            if variable in dict_:
                level = level + i
                break
        else:
            raise KeyError(variable)
        levels[variable] = level + 1

        new_d = (
            ([{}] * level) + d[level:]
            if method == InterpolateEnumType.DEEP_NO_BACKTRACK
            else d
        )
        resolved[variable] = interpolate_deep(
            attr, d[level][variable], new_d, resolved, levels, method
        )

    return text.format(**resolved)


def flatten(d: List[dict]) -> dict:
    """
    Flatten a list of dictionaries.

    :param d: dictionary list
    """
    result = {}
    [result.update(dict_) for dict_ in d[::-1]]
    return result


def interpolate_object(
    attr: str, obj: Any, d: List[dict], method: InterpolateEnumType
) -> Any:
    """
    Return the interpolated object.

    :param attr: attribute name
    :param obj: object to interpolate
    :param d: dictionary
    :param method: interpolation method
    """
    if isinstance(obj, str):
        if method == InterpolateEnumType.STANDARD:
            return interpolate_standard(obj, flatten(d), set())
        elif method in (
            InterpolateEnumType.DEEP,
            InterpolateEnumType.DEEP_NO_BACKTRACK,
        ):
            return interpolate_deep(attr, obj, d, {}, {}, method)
        else:
            raise ValueError('Invalid interpolation method "%s"' % method)
    elif hasattr(obj, "__iter__"):
        if isinstance(obj, tuple):
            return tuple(interpolate_object(attr, x, d, method) for x in obj)
        else:
            return [interpolate_object(attr, x, d, method) for x in obj]
    else:
        return obj