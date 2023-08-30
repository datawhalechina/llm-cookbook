本课程中我们会看到很多`from llama import BasicModelRunner`这样的代码，可能很多同学以为要安装`llama`库，其实不然，<b>我们要安装的是`lamini`库</b>，`llama`只是`lamini`库的一个子集。以下为`lamini`库的安装和使用说明。

## 安装
`lamini`库的安装非常简单，只需要执行以下命令即可：

`pip install lamini`

## 注册
接下来我们需要去[ lamini官网](https://www.lamini.ai/)注册一个账号获取api key，才能使用`lamini`库的全部功能。
![lamini官网](../../figures/Finetuning%20Large%20Language%20Models/lamini官网.png)

账号注册可以使用谷歌邮箱（默认）或者其他邮箱。注册完成后点击官网左上角的`Account`即可看到自己的 api key 以及剩余额度。

![lamini官网](../../figures/Finetuning%20Large%20Language%20Models/lamini官网_apikey.png)

## 使用
### 1. 默认方式
`lamini`默认需要在你的用户目录下创建一个配置文件 `~/.powerml/configure_llama.yaml`，然后按如下方式写入配置信息：

```
production:
    key: "<YOUR-KEY-HERE>"
```

用户目录在Windows系统一般为`C:\Users\Administrator`， 在 Linux/maxOS 一般为`~/`。

### 2. 简便方式
鉴于默认方式较为麻烦，我们给大家提供一种更为方便的方法。当我们需要用到`llama`的`LLMEngine`或`BasicModelRunner`类时，直接将`production.key`写入类的参数`config`中即可，比如：

```
llm = LLMEngine(
    id="example_llm",
    config={"production.key": "<YOUR-KEY-HERE>"}
    )
```

又或者：
```
non_finetuned = BasicModelRunner("meta-llama/Llama-2-7b-hf", 
                config={"production.key": "<YOUR-KEY-HERE>"})

```

只需将`<YOUR-KEY-HERE>`替换为我们在`lamini`官网的api key即可。

如果担心代码泄露api key的话，可以仿照使用ChatGPT的方式，用一个配置文件来存储`production.key`，这里就不再展开了。
