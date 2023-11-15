# 面向开发者的 LLM 入门课程

## 简介

LLM 正在逐步改变人们的生活，而对于开发者，如何基于 LLM 提供的 API 快速、便捷地开发一些具备更强能力、集成LLM 的应用，来便捷地实现一些更新颖、更实用的能力，是一个急需学习的重要能力。

由吴恩达老师与 OpenAI 合作推出的大模型系列教程，从大模型时代开发者的基础技能出发，深入浅出地介绍了如何基于大模型 API、LangChain 架构快速开发结合大模型强大能力的应用。其中，《Prompt Engineering for Developers》教程面向入门 LLM 的开发者，深入浅出地介绍了对于开发者，如何构造 Prompt 并基于 OpenAI 提供的 API 实现包括总结、推断、转换等多种常用功能，是入门 LLM 开发的经典教程；《Building Systems with the ChatGPT API》教程面向想要基于 LLM 开发应用程序的开发者，简洁有效而又系统全面地介绍了如何基于 ChatGPT API 打造完整的对话系统；《LangChain for LLM Application Development》教程结合经典大模型开源框架 LangChain，介绍了如何基于 LangChain 框架开发具备实用功能、能力全面的应用程序，《LangChain Chat With Your Data》教程则在此基础上进一步介绍了如何使用 LangChain 架构结合个人私有数据开发个性化大模型应用。

上述教程非常适用于开发者学习以开启基于 LLM 实际搭建应用程序之路。因此，我们将该系列课程翻译为中文，并复现其范例代码，也为其中一个视频增加了中文字幕，支持国内中文学习者直接使用，以帮助中文学习者更好地学习 LLM 开发；我们也同时实现了效果大致相当的中文 Prompt，支持学习者感受中文语境下 LLM 的学习使用，对比掌握多语言语境下的 Prompt 设计与 LLM 开发。未来，我们也将加入更多 Prompt 高级技巧，以丰富本课程内容，帮助开发者掌握更多、更巧妙的 Prompt 技能。

## 受众

适用于所有具备基础 Python 能力，想要入门 LLM 的开发者。

## 亮点

《ChatGPT Prompt Engineering for Developers》、《Building Systems with the ChatGPT API》、《LangChain for LLM Application Development》、《LangChain Chat with Your Data》等教程作为由吴恩达老师与 OpenAI 联合推出的官方教程，在可预见的未来会成为 LLM 的重要入门教程，但是目前还只支持英文版且国内访问受限，打造中文版且国内流畅访问的教程具有重要意义；同时，GPT 对中文、英文具有不同的理解能力，本教程在多次对比、实验之后确定了效果大致相当的中文 Prompt，支持学习者研究如何提升 ChatGPT 在中文语境下的理解与生成能力。

## 内容大纲

### 一、面向开发者的提示工程

注：吴恩达《ChatGPT Prompt Engineering for Developers》课程中文版

**目录：**

1. 简介 Introduction @邹雨衡
2. Prompt 的构建原则 Guidelines @邹雨衡
3. 如何迭代优化 Prompt Itrative @邹雨衡
4. 文本总结 Summarizing @玉琳
5. 文本推断 Inferring @长琴
6. 文本转换 Transforming @玉琳
7. 文本扩展 Expanding @邹雨衡
8. 聊天机器人 Chatbot @长琴
9. 总结 @长琴

附1 使用 ChatGLM 进行学习 @宋志学
  
 ### 二、搭建基于 ChatGPT 的问答系统
 
 注：吴恩达《Building Systems with the ChatGPT API》课程中文版
 
 **目录：**

1. 简介 Introduction @Sarai
2. 模型，范式和 token Language Models, the Chat Format and Tokens @仲泰
3. 检查输入-分类 Classification @诸世纪
4. 检查输入-监督 Moderation @诸世纪
5. 思维链推理 Chain of Thought Reasoning @万礼行
6. 提示链 Chaining Prompts @万礼行
7. 检查输入 Check Outputs @仲泰
8. 评估（端到端系统）Evaluation @邹雨衡
9. 评估（简单问答）Evaluation-part1 @陈志宏、邹雨衡
10. 评估（复杂问答）Evaluation-part2 @邹雨衡
11. 总结 Conclusion @Sarai
  
 ### 三、使用 LangChain 开发应用程序
 
 注：吴恩达《LangChain for LLM Application Development》课程中文版
 
 **目录：**

1. 简介 Introduction @Sarai
2. 模型，提示和解析器 Models, Prompts and Output Parsers @Joye
3. 存储 Memory @徐虎
4. 模型链 Chains @徐虎
5. 基于文档的问答 Question and Answer @苟晓攀
6. 评估 Evaluation @苟晓攀
7. 代理 Agent @Joye
8. 总结 Conclusion @Sarai

 ### 四、使用 LangChain 访问个人数据

 注：吴恩达《LangChain Chat with Your Data》课程中文版

 **目录：**

1. 简介 Introduction @Joye
2. 加载文档 Document Loading @Joye
3. 文档切割 Document Splitting @苟晓攀
4. 向量数据库与词向量 Vectorstores and Embeddings @刘伟鸿、仲泰
5. 检索 Retrieval @刘伟鸿
6. 问答 Question Answering @邹雨衡
7. 聊天 Chat @高立业
8. 总结 Summary @高立业

## 致谢

**核心贡献者**

- [邹雨衡-项目负责人](https://github.com/nowadays0421)（Datawhale成员-对外经济贸易大学研究生）
- [长琴-项目发起人](https://yam.gift/)（内容创作者-Datawhale成员-AI算法工程师）
- [玉琳-项目发起人](https://github.com/Sophia-Huang)（内容创作者-Datawhale成员）
- [徐虎-教程编撰成员](https://github.com/xuhu0115)（内容创作者）
- [Joye-教程编撰成员](https://Joyenjoye.com)（内容创作者-数据科学家）
- [刘伟鸿-教程编撰成员](https://github.com/Weihong-Liu)（内容创作者-江南大学非全研究生）
- [高立业](https://github.com/0-yy-0)（内容创作者-DataWhale成员-算法工程师）
- [Zhang Yixin](https://github.com/YixinZ-NUS)（内容创作者-IT爱好者）
- [万礼行](https://github.com/leason-wan)（内容创作者-视频翻译者）
- [仲泰](https://github.com/ztgg0228)（内容创作者-Datawhale成员）
- [魂兮](https://github.com/wisdom-pan)（内容创作者-前端工程师）
- [诸世纪](https://github.com/very-very-very)（内容创作者-算法工程师）
- [宋志学](https://github.com/KMnO4-zx)（内容创作者-Datawhale成员）
- Sarai（内容创作者-AI应用爱好者）

**其他**

1. 特别感谢 [@Sm1les](https://github.com/Sm1les)、[@LSGOMYP](https://github.com/LSGOMYP) 对本项目的帮助与支持；
2. 感谢 [GithubDaily](https://github.com/GitHubDaily) 提供的双语字幕；
3. 如果有任何想法可以联系我们 DataWhale 也欢迎大家多多提出 issue；
4. 特别感谢以下为教程做出贡献的同学！

<a href="https://github.com/datawhalechina/prompt-engineering-for-developers/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=datawhalechina/prompt-engineering-for-developers" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

## 关注我们

<div align=center>
<p>扫描下方二维码关注公众号：Datawhale</p>
<img src="figures/C0/qrcode.jpeg" width = "180" height = "180">
</div>
Datawhale 是一个专注于数据科学与 AI 领域的开源组织，汇集了众多领域院校和知名企业的优秀学习者，聚合了一群有开源精神和探索精神的团队成员。微信搜索公众号Datawhale可以加入我们。

## LICENSE
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
