# 基于Chroma的高级检索技术

## 简介

欢迎来到《基于Chroma的高级检索技术》课程👏🏻👏🏻

本课程由 Anton Troynikov（Chroma联合创始人）和 Deeplearning.ai 联合开发，旨在介绍基于`chroma`的高级检索技术，提升检索结果的准确性。

RAG（Retrieval Augmented Generation），又称检索增强生成，通过检索相关文本，为大语言模型（LLM）提供参考资料，从而提高LLM在特定任务上的回答准确性和可靠性。

这种方法的问题在于，嵌入模型可能会找到与查询相似主题的文本，但并不包含我们想要的答案，对LLM的回答形成干扰。为解决这个问题，我们可以采用查询扩展（Query Expansion）的方法。方式一：通过不同方式重新措辞或重写初始查询，将其扩展为多个查询；方式二：猜测或给定一个参考答案，以查看我们的文本集合中是否有更像答案的内容，而不仅仅是和查询主题有关但不含答案的干扰项。

当然，查询拓展只是其中一个方法，学完这门课程你将了解更多增强检索效果的方法，构建出更加强大的AI系统。


## 课程内容

在本课程中，您将学习到一系列知识和技术：
 - 基于embedding的检索技术概述
 - 检索陷阱——为何简单向量检索有时会失效
 - 查询拓展
 - 运用交叉编码器重新排序
 - Embedding Adaptors
 - 其他技术

## 致谢

最后特别感谢 Chroma 团队的 Jeff Huber, Hammad Bashir, Liquan Pei, Ben Eggers 以及 DeepLearning.AI 团队的 Geoff Ladwig 和 Esmael Gargari 对本课程做出的贡献。
