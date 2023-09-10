"""python-configuration module."""

import json
import os
from importlib.abc import InspectLoader
from types import ModuleType
from typing import Any, Dict, Iterable, List, Optional, TextIO, Union, cast

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None
try:
    import toml
except ImportError:  # pragma: no cover
    toml = None


from .configuration import Configuration
from .configuration_set import ConfigurationSet
from .helpers import InterpolateEnumType, InterpolateType


def config(
    *configs: Iterable,
    prefix: str = "",
    separator: Optional[str] = None,
    remove_level: int = 1,
    lowercase_keys: bool = False,
    ignore_missing_paths: bool = False,
    interpolate: InterpolateType = False,
    interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
) -> ConfigurationSet:
    """
    Create a :class:`ConfigurationSet` instance from an iterable of configs.

    :param configs: iterable of configurations
    :param prefix: prefix to filter environment variables with
    :param remove_level: how many levels to remove from the resulting config
    :param lowercase_keys: whether to convert every key to lower case.
    :param ignore_missing_paths: whether to ignore failures from missing files/folders.
    :param separator: separator for Python modules and environment variables.
    :param interpolate: whether to apply string interpolation when looking for items

    Note that the :py:attr:`separator` parameter  impacts Python modules and and
    environment variables at the same time. To pass different separators to Python
    modules and environments, use the longer version
    ``('python', 'path-to-module', prefix, separator)``
    and ``('env', prefix, separator)`` .
    """
    instances = []
    default_args: List[str] = [prefix]
    if separator is not None:
        default_args.append(separator)
    default_kwargs: Dict[Any, Any] = {
        "lowercase_keys": lowercase_keys,
        # for Configuration Sets, interpolate parameters should be at the Set level
        "interpolate": False,
        "interpolate_type": InterpolateEnumType.STANDARD,
    }

    for config_ in configs:
        if isinstance(config_, dict):
            instances.append(config_from_dict(config_, **default_kwargs))
            continue
        elif isinstance(config_, str):
            if config_.endswith(".py"):
                config_ = ("python", config_, *default_args)
            elif config_.endswith(".json"):
                config_ = ("json", config_, True)
            elif yaml and config_.endswith(".yaml"):
                config_ = ("yaml", config_, True)
            elif toml and config_.endswith(".toml"):
                config_ = ("toml", config_, True)
            elif config_.endswith(".ini"):
                config_ = ("ini", config_, True)
            elif config_.endswith(".env"):
                config_ = ("dotenv", config_, True)
            elif os.path.isdir(config_):
                config_ = ("path", config_, remove_level)
            elif config_ in ("env", "environment"):
                config_ = ("env", *default_args)
            elif all(s and s.isidentifier() for s in config_.split(".")):
                config_ = ("python", config_, *default_args)
            else:
                raise ValueError(f'Cannot determine config type from "{config_}"')

        if not isinstance(config_, (tuple, list)) or len(config_) == 0:
            raise ValueError(
                "configuration parameters must be a list of dictionaries,"
                " strings, or non-empty tuples/lists"
            )
        type_ = config_[0]
        if type_ == "dict":
            instances.append(config_from_dict(*config_[1:], **default_kwargs))
        elif type_ in ("env", "environment"):
            params = list(config_[1:]) + default_args[(len(config_) - 1) :]
            instances.append(config_from_env(*params, **default_kwargs))
        elif type_ == "python":
            if len(config_) < 2:
                raise ValueError("No path specified for python module")
            params = list(config_[1:]) + default_args[(len(config_) - 2) :]
            try:
                instances.append(config_from_python(*params, **default_kwargs))
            except (FileNotFoundError, ModuleNotFoundError):
                if not ignore_missing_paths:
                    raise
        elif type_ == "json":
            try:
                instances.append(config_from_json(*config_[1:], **default_kwargs))
            except FileNotFoundError:
                if not ignore_missing_paths:
                    raise
        elif yaml and type_ == "yaml":
            try:
                instances.append(config_from_yaml(*config_[1:], **default_kwargs))
            except FileNotFoundError:
                if not ignore_missing_paths:
                    raise
        elif toml and type_ == "toml":
            try:
                instances.append(config_from_toml(*config_[1:], **default_kwargs))
            except FileNotFoundError:
                if not ignore_missing_paths:
                    raise
        elif type_ == "ini":
            try:
                instances.append(config_from_ini(*config_[1:], **default_kwargs))
            except FileNotFoundError:
                if not ignore_missing_paths:
                    raise
        elif type_ == "dotenv":
            try:
                instances.append(config_from_dotenv(*config_[1:], **default_kwargs))
            except FileNotFoundError:
                if not ignore_missing_paths:
                    raise
        elif type_ == "path":
            try:
                instances.append(config_from_path(*config_[1:], **default_kwargs))
            except FileNotFoundError:
                if not ignore_missing_paths:
                    raise
        else:
            raise ValueError(f'Unknown configuration type "{type_}"')

    return ConfigurationSet(
        *instances, interpolate=interpolate, interpolate_type=interpolate_type
    )


class EnvConfiguration(Configuration):
    """Configuration from Environment variables."""

    def __init__(
        self,
        prefix: str,
        separator: str = "__",
        *,
        lowercase_keys: bool = False,
        interpolate: InterpolateType = False,
        interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
    ):
        """
        Constructor.

        :param prefix: prefix to filter environment variables with
        :param separator: separator to replace by dots
        :param lowercase_keys: whether to convert every key to lower case.
        """
        self._prefix = prefix
        self._separator = separator
        super().__init__(
            {},
            lowercase_keys=lowercase_keys,
            interpolate=interpolate,
            interpolate_type=interpolate_type,
        )
        self.reload()

    def reload(self) -> None:
        """Reload the environment values."""
        result = {}
        for key, value in os.environ.items():
            if not key.startswith(self._prefix + self._separator):
                continue
            result[
                key[len(self._prefix) :].replace(self._separator, ".").strip(".")
            ] = value
        super().__init__(
            result,
            lowercase_keys=self._lowercase,
            interpolate=self._interpolate,
            interpolate_type=self._interpolate_type,
        )


def config_from_env(
    prefix: str,
    separator: str = "__",
    *,
    lowercase_keys: bool = False,
    interpolate: InterpolateType = False,
    interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
) -> Configuration:
    """
    Create a :class:`EnvConfiguration` instance from environment variables.

    :param prefix: prefix to filter environment variables with
    :param separator: separator to replace by dots
    :param lowercase_keys: whether to convert every key to lower case.
    :param interpolate: whether to apply string interpolation when looking for items
    :return: a :class:`Configuration` instance
    """
    return EnvConfiguration(
        prefix,
        separator,
        lowercase_keys=lowercase_keys,
        interpolate=interpolate,
        interpolate_type=interpolate_type,
    )


class PathConfiguration(Configuration):
    """Configuration from a filesytem path."""

    def __init__(
        self,
        path: str,
        remove_level: int = 1,
        *,
        lowercase_keys: bool = False,
        interpolate: InterpolateType = False,
        interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
    ):
        """
        Constructor.

        :param path: path to read from
        :param remove_level: how many levels to remove from the resulting config
        :param lowercase_keys: whether to convert every key to lower case.
        """
        self._path = path
        self._remove_level = remove_level
        super().__init__(
            {},
            lowercase_keys=lowercase_keys,
            interpolate=interpolate,
            interpolate_type=interpolate_type,
        )
        self.reload()

    def reload(self) -> None:
        """Reload the path."""
        path = os.path.normpath(self._path)
        if not os.path.exists(path) or not os.path.isdir(path):
            raise FileNotFoundError()

        dotted_path_levels = len(path.split("/"))
        files_keys = (
            (
                os.path.join(x[0], y),
                ".".join(
                    (x[0].split("/") + [y])[(dotted_path_levels + self._remove_level) :]
                ),
            )
            for x in os.walk(path)
            for y in x[2]
            if not x[0].split("/")[-1].startswith("..")
        )

        result = {}
        for filename, key in files_keys:
            result[key] = open(filename).read()

        super().__init__(
            result,
            lowercase_keys=self._lowercase,
            interpolate=self._interpolate,
            interpolate_type=self._interpolate_type,
        )


def config_from_path(
    path: str,
    remove_level: int = 1,
    *,
    lowercase_keys: bool = False,
    interpolate: InterpolateType = False,
    interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
) -> Configuration:
    """
    Create a :class:`Configuration` instance from filesystem path.

    :param path: path to read from
    :param remove_level: how many levels to remove from the resulting config
    :param lowercase_keys: whether to convert every key to lower case.
    :param interpolate: whether to apply string interpolation when looking for items
    :return: a :class:`Configuration` instance
    """
    return PathConfiguration(
        path,
        remove_level,
        lowercase_keys=lowercase_keys,
        interpolate=interpolate,
        interpolate_type=interpolate_type,
    )


class FileConfiguration(Configuration):
    """Configuration from a file input."""

    def __init__(
        self,
        data: Union[str, TextIO],
        read_from_file: bool = False,
        *,
        lowercase_keys: bool = False,
        interpolate: InterpolateType = False,
        interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
    ):
        """
        Constructor.

        :param data: path to a config file, or its contents
        :param read_from_file: whether to read from a file path or to interpret
               the :attr:`data` as the contents of the file.
        :param lowercase_keys: whether to convert every key to lower case.
        """
        super().__init__(
            {},
            lowercase_keys=lowercase_keys,
            interpolate=interpolate,
            interpolate_type=interpolate_type,
        )
        self._reload(data, read_from_file)
        self._data = data if read_from_file and isinstance(data, str) else None

    def _reload(
        self, data: Union[str, TextIO], read_from_file: bool = False
    ) -> None:  # pragma: no cover
        raise NotImplementedError()

    def reload(self) -> None:
        """Reload the configuration."""
        if self._data:  # pragma: no branch
            self._reload(self._data, True)


class JSONConfiguration(FileConfiguration):
    """Configuration from a JSON input."""

    def _reload(self, data: Union[str, TextIO], read_from_file: bool = False) -> None:
        """Reload the JSON data."""
        if read_from_file:
            if isinstance(data, str):
                result = json.load(open(data, "rt"))
            else:
                result = json.load(data)
        else:
            result = json.loads(cast(str, data))
        self._config = self._flatten_dict(result)


def config_from_json(
    data: Union[str, TextIO],
    read_from_file: bool = False,
    *,
    lowercase_keys: bool = False,
    interpolate: InterpolateType = False,
    interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
) -> Configuration:
    """
    Create a :class:`Configuration` instance from a JSON file.

    :param data: path to a JSON file or contents
    :param read_from_file: whether to read from a file path or to interpret
           the :attr:`data` as the contents of the JSON file.
    :param lowercase_keys: whether to convert every key to lower case.
    :param interpolate: whether to apply string interpolation when looking for items
    :return: a :class:`Configuration` instance
    """
    return JSONConfiguration(
        data,
        read_from_file,
        lowercase_keys=lowercase_keys,
        interpolate=interpolate,
        interpolate_type=interpolate_type,
    )


class INIConfiguration(FileConfiguration):
    """Configuration from an INI file input."""

    def __init__(
        self,
        data: Union[str, TextIO],
        read_from_file: bool = False,
        *,
        section_prefix: str = "",
        lowercase_keys: bool = False,
        interpolate: InterpolateType = False,
        interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
    ):
        self._section_prefix = section_prefix
        super().__init__(
            data=data,
            read_from_file=read_from_file,
            lowercase_keys=lowercase_keys,
            interpolate=interpolate,
            interpolate_type=interpolate_type,
        )

    def _reload(self, data: Union[str, TextIO], read_from_file: bool = False) -> None:
        """Reload the INI data."""
        import configparser

        lowercase = self._lowercase

        class ConfigParser(configparser.RawConfigParser):
            def optionxform(self, optionstr: str) -> str:
                return super().optionxform(optionstr) if lowercase else optionstr

        if read_from_file:
            if isinstance(data, str):
                data = open(data, "rt").read()
            else:
                data = data.read()
        data = cast(str, data)
        cfg = ConfigParser()
        cfg.read_string(data)
        result = {
            section[len(self._section_prefix) :] + "." + k: v
            for section, values in cfg.items()
            for k, v in values.items()
            if section.startswith(self._section_prefix)
        }
        self._config = self._flatten_dict(result)


def config_from_ini(
    data: Union[str, TextIO],
    read_from_file: bool = False,
    *,
    section_prefix: str = "",
    lowercase_keys: bool = False,
    interpolate: InterpolateType = False,
    interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
) -> Configuration:
    """
    Create a :class:`Configuration` instance from an INI file.

    :param data: path to an INI file or contents
    :param read_from_file: whether to read from a file path or to interpret
           the :attr:`data` as the contents of the INI file.
    :param lowercase_keys: whether to convert every key to lower case.
    :param interpolate: whether to apply string interpolation when looking for items
    :return: a :class:`Configuration` instance
    """
    return INIConfiguration(
        data,
        read_from_file,
        section_prefix=section_prefix,
        lowercase_keys=lowercase_keys,
        interpolate=interpolate,
        interpolate_type=interpolate_type,
    )


class DotEnvConfiguration(FileConfiguration):
    """Configuration from a .env type file input."""

    def _reload(self, data: Union[str, TextIO], read_from_file: bool = False) -> None:
        """Reload the .env data."""
        if read_from_file:
            if isinstance(data, str):
                data = open(data, "rt").read()
            else:
                data = data.read()
        data = cast(str, data)
        result: Dict[str, Any] = dict(
            (y.strip() for y in x.split("=", 1))  # type: ignore
            for x in data.splitlines()
            if x
        )
        self._config = self._flatten_dict(result)


def config_from_dotenv(
    data: Union[str, TextIO],
    read_from_file: bool = False,
    *,
    lowercase_keys: bool = False,
    interpolate: InterpolateType = False,
    interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
) -> Configuration:
    """
    Create a :class:`Configuration` instance from a .env type file.

    :param data: path to a .env type file or contents
    :param read_from_file: whether to read from a file path or to interpret
           the :attr:`data` as the contents of the INI file.
    :param lowercase_keys: whether to convert every key to lower case.
    :param interpolate: whether to apply string interpolation when looking for items
    :return: a :class:`Configuration` instance
    """
    return DotEnvConfiguration(
        data,
        read_from_file,
        lowercase_keys=lowercase_keys,
        interpolate=interpolate,
        interpolate_type=interpolate_type,
    )


class PythonConfiguration(Configuration):
    """Configuration from a python module."""

    def __init__(
        self,
        module: Union[str, ModuleType],
        prefix: str = "",
        separator: str = "_",
        *,
        lowercase_keys: bool = False,
        interpolate: InterpolateType = False,
        interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
    ):
        """
        Constructor.

        :param module: a module or path string
        :param prefix: prefix to use to filter object names
        :param separator: separator to replace by dots
        :param lowercase_keys: whether to convert every key to lower case.
        """
        if isinstance(module, str):
            if module.endswith(".py"):
                import importlib.util
                from importlib import machinery

                spec = cast(
                    machinery.ModuleSpec,
                    importlib.util.spec_from_file_location(module, module),
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader = cast(InspectLoader, spec.loader)
                spec.loader.exec_module(module)
            else:
                import importlib

                module = importlib.import_module(module)
        self._module = module
        self._prefix = prefix
        self._separator = separator
        super().__init__(
            {},
            lowercase_keys=lowercase_keys,
            interpolate=interpolate,
            interpolate_type=interpolate_type,
        )
        self.reload()

    def reload(self) -> None:
        """Reload the path."""
        variables = [
            x
            for x in dir(self._module)
            if not x.startswith("__") and x.startswith(self._prefix)
        ]
        result = {
            k[len(self._prefix) :]
            .replace(self._separator, ".")
            .strip("."): getattr(self._module, k)
            for k in variables
        }
        super().__init__(
            result,
            lowercase_keys=self._lowercase,
            interpolate=self._interpolate,
            interpolate_type=self._interpolate_type,
        )


def config_from_python(
    module: Union[str, ModuleType],
    prefix: str = "",
    separator: str = "_",
    *,
    lowercase_keys: bool = False,
    interpolate: InterpolateType = False,
    interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
) -> Configuration:
    """
    Create a :class:`Configuration` instance from the objects in a Python module.

    :param module: a module or path string
    :param prefix: prefix to use to filter object names
    :param separator: separator to replace by dots
    :param lowercase_keys: whether to convert every key to lower case.
    :param interpolate: whether to apply string interpolation when looking for items
    :return: a :class:`Configuration` instance
    """
    return PythonConfiguration(
        module,
        prefix,
        separator,
        lowercase_keys=lowercase_keys,
        interpolate=interpolate,
        interpolate_type=interpolate_type,
    )


def config_from_dict(
    data: dict,
    *,
    lowercase_keys: bool = False,
    interpolate: InterpolateType = False,
    interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
) -> Configuration:
    """
    Create a :class:`Configuration` instance from a dictionary.

    :param data: dictionary with string keys
    :param lowercase_keys: whether to convert every key to lower case.
    :param interpolate: whether to apply string interpolation when looking for items
    :return: a :class:`Configuration` instance
    """
    return Configuration(
        data,
        lowercase_keys=lowercase_keys,
        interpolate=interpolate,
        interpolate_type=interpolate_type,
    )


def create_path_from_config(
    path: str, cfg: Configuration, remove_level: int = 1
) -> Configuration:
    """
    Output a path configuration from a :class:`Configuration` instance.

    :param path: path to create the config files in
    :param cfg: :class:`Configuration` instance
    :param remove_level: how many levels to remove
    """
    import os.path

    assert os.path.isdir(path)

    d = cfg.as_dict()
    for k, v in d.items():
        with open(os.path.join(path, k), "wb") as f:
            f.write(str(v).encode())

        cfg = config_from_path(path, remove_level=remove_level)
    return cfg


if yaml is not None:  # pragma: no branch

    class YAMLConfiguration(FileConfiguration):
        """Configuration from a YAML input."""

        def _reload(
            self, data: Union[str, TextIO], read_from_file: bool = False
        ) -> None:
            """Reload the YAML data."""
            if read_from_file and isinstance(data, str):
                loaded = yaml.load(open(data, "rt"), Loader=yaml.FullLoader)
            else:
                loaded = yaml.load(data, Loader=yaml.FullLoader)
            if not isinstance(loaded, dict):
                raise ValueError("Data should be a dictionary")
            self._config = self._flatten_dict(loaded)

    def config_from_yaml(
        data: Union[str, TextIO],
        read_from_file: bool = False,
        *,
        lowercase_keys: bool = False,
        interpolate: InterpolateType = False,
        interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
    ) -> Configuration:
        """
        Return a Configuration instance from YAML files.

        :param data: string or file
        :param read_from_file: whether `data` is a file or a YAML formatted string
        :param lowercase_keys: whether to convert every key to lower case.
        :param interpolate: whether to apply string interpolation when looking for items
        :return: a Configuration instance
        """
        return YAMLConfiguration(
            data,
            read_from_file,
            lowercase_keys=lowercase_keys,
            interpolate=interpolate,
            interpolate_type=interpolate_type,
        )


if toml is not None:  # pragma: no branch

    class TOMLConfiguration(FileConfiguration):
        """Configuration from a TOML input."""

        def __init__(
            self,
            data: Union[str, TextIO],
            read_from_file: bool = False,
            *,
            section_prefix: str = "",
            lowercase_keys: bool = False,
            interpolate: InterpolateType = False,
            interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
        ):
            self._section_prefix = section_prefix
            super().__init__(
                data=data,
                read_from_file=read_from_file,
                lowercase_keys=lowercase_keys,
                interpolate=interpolate,
                interpolate_type=interpolate_type,
            )

        def _reload(
            self, data: Union[str, TextIO], read_from_file: bool = False
        ) -> None:
            """Reload the TOML data."""
            if read_from_file:
                if isinstance(data, str):
                    loaded = toml.load(open(data, "rt"))
                else:
                    loaded = toml.load(data)
            else:
                data = cast(str, data)
                loaded = toml.loads(data)
            loaded = cast(dict, loaded)

            result = {
                k[len(self._section_prefix) :]: v
                for k, v in self._flatten_dict(loaded).items()
                if k.startswith(self._section_prefix)
            }

            self._config = result

    def config_from_toml(
        data: Union[str, TextIO],
        read_from_file: bool = False,
        *,
        section_prefix: str = "",
        lowercase_keys: bool = False,
        interpolate: InterpolateType = False,
        interpolate_type: InterpolateEnumType = InterpolateEnumType.STANDARD,
    ) -> Configuration:
        """
        Return a Configuration instance from TOML files.

        :param data: string or file
        :param read_from_file: whether `data` is a file or a TOML formatted string
        :param lowercase_keys: whether to convert every key to lower case.
        :param interpolate: whether to apply string interpolation when looking for items
        :return: a Configuration instance
        """
        return TOMLConfiguration(
            data,
            read_from_file,
            section_prefix=section_prefix,
            lowercase_keys=lowercase_keys,
            interpolate=interpolate,
            interpolate_type=interpolate_type,
        )