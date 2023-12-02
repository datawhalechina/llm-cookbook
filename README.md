![figures/readme.png](https://github.com/datawhalechina/prompt-engineering-for-developers/blob/main/figures/readme2.png)

# 面向开发者的 LLM 入门课程

## 项目简介

本项目是一个面向开发者的 LLM 入门教程，基于吴恩达老师大模型系列课程内容，将原课程内容翻译为中文并复现其范例代码，实现中文 Prompt，指导国内开发者如何基于 LLM 快速、高效开发具备强大能力的应用程序。本项目的主要内容包括：

1. 面向开发者的 Prompt Engineering。基于吴恩达老师《ChatGPT Prompt Engineering for Developers》课程打造，面向入门 LLM 的开发者，深入浅出地介绍了对于开发者，如何构造 Prompt 并基于 OpenAI 提供的 API 实现包括总结、推断、转换等多种常用功能，是入门 LLM 开发的第一步。
2. 搭建基于 ChatGPT 的问答系统。基于吴恩达老师《Building Systems with the ChatGPT API》课程打造，指导开发者如何基于 ChatGPT 提供的 API 开发一个完整的、全面的智能问答系统。通过代码实践，实现了基于 ChatGPT 开发问答系统的全流程，介绍了基于大模型开发的新范式，是大模型开发的实践基础。
3. 使用 LangChain 开发应用程序。基于吴恩达老师《LangChain for LLM Application Development》课程打造，对 LangChain 展开深入介绍，帮助学习者了解如何使用 LangChain，并基于 LangChain 开发完整的、具备强大能力的应用程序。
4. 使用 LangChain 访问个人数据。基于吴恩达老师《LangChain Chat with Your Data》课程打造，深入拓展 LangChain 提供的个人数据访问能力，指导开发者如何使用 LangChain 开发能够访问用户个人数据、提供个性化服务的大模型应用。
5. 使用 Gradio 搭建生成式 AI 应用。基于吴恩达老师《Building Generative AI Applications with Gradio》课程打造，指导开发者如何使用 Gradio 通过 Python 接口程序快速、高效地为生成式 AI 构建用户界面。
6. 评估改进生成式 AI。基于吴恩达老师《Evaluating and Debugging Generative AI》课程打造，结合 wandb，提供一套系统化的方法和工具，帮助开发者有效地跟踪和调试生成式 AI 模型。
7. 微调大语言模型。基于吴恩达老师《Finetuning Large Language Model》课程打造，结合 lamini 框架，讲述如何便捷高效地在本地基于个人数据微调开源大语言模型。


**在线阅读地址：[面向开发者的 LLM 入门课程-在线阅读](https://datawhalechina.github.io/prompt-engineering-for-developers/)**

**PDF下载地址：[面向开发者的 LLM 入门教程-PDF](https://github.com/datawhalechina/prompt-engineering-for-developers/releases)**

**英文原版地址：[吴恩达关于大模型的系列课程](https://learn.deeplearning.ai)**

**双语字幕视频地址：[吴恩达 x OpenAI的Prompt Engineering课程专业翻译版](https://www.bilibili.com/video/BV1Bo4y1A7FU/?share_source=copy_web)**

**中英双语字幕下载：[《ChatGPT提示工程》非官方版中英双语字幕](https://github.com/GitHubDaily/ChatGPT-Prompt-Engineering-for-Developers-in-Chinese)**

**视频讲解：[面向开发者的 Prompt Engineering 讲解（数字游民大会）](https://www.bilibili.com/video/BV1PN4y1k7y2/?spm_id_from=333.999.0.0)**

**目录结构说明：**

    content：基于原课程复现的双语版代码，可运行的 Notebook，更新频率最高，更新速度最快。
    
    docs：文字教程版在线阅读源码，适合阅读的 md。
    
    figures：图片文件。
    
    pdf-code：文字教程版源码，适合阅读的 Notebook。

## 项目意义

LLM 正在逐步改变人们的生活，而对于开发者，如何基于 LLM 提供的 API 快速、便捷地开发一些具备更强能力、集成LLM 的应用，来便捷地实现一些更新颖、更实用的能力，是一个急需学习的重要能力。

由吴恩达老师与 OpenAI 合作推出的大模型系列教程，从大模型时代开发者的基础技能出发，深入浅出地介绍了如何基于大模型 API、LangChain 架构快速开发结合大模型强大能力的应用。其中，《Prompt Engineering for Developers》教程面向入门 LLM 的开发者，深入浅出地介绍了对于开发者，如何构造 Prompt 并基于 OpenAI 提供的 API 实现包括总结、推断、转换等多种常用功能，是入门 LLM 开发的经典教程；《Building Systems with the ChatGPT API》教程面向想要基于 LLM 开发应用程序的开发者，简洁有效而又系统全面地介绍了如何基于 ChatGPT API 打造完整的对话系统；《LangChain for LLM Application Development》教程结合经典大模型开源框架 LangChain，介绍了如何基于 LangChain 框架开发具备实用功能、能力全面的应用程序，《LangChain Chat With Your Data》教程则在此基础上进一步介绍了如何使用 LangChain 架构结合个人私有数据开发个性化大模型应用；《Building Generative AI Applications with Gradio》、《Evaluating and Debugging Generative AI》教程分别介绍了两个实用工具 Gradio 与 W&B，指导开发者如何结合这两个工具来打造、评估生成式 AI 应用。

上述教程非常适用于开发者学习以开启基于 LLM 实际搭建应用程序之路。因此，我们将该系列课程翻译为中文，并复现其范例代码，也为其中一个视频增加了中文字幕，支持国内中文学习者直接使用，以帮助中文学习者更好地学习 LLM 开发；我们也同时实现了效果大致相当的中文 Prompt，支持学习者感受中文语境下 LLM 的学习使用，对比掌握多语言语境下的 Prompt 设计与 LLM 开发。未来，我们也将加入更多 Prompt 高级技巧，以丰富本课程内容，帮助开发者掌握更多、更巧妙的 Prompt 技能。

## 项目受众

适用于所有具备基础 Python 能力，想要入门 LLM 的开发者。

## 项目亮点

《ChatGPT Prompt Engineering for Developers》、《Building Systems with the ChatGPT API》等教程作为由吴恩达老师与 OpenAI 联合推出的官方教程，在可预见的未来会成为 LLM 的重要入门教程，但是目前还只支持英文版且国内访问受限，打造中文版且国内流畅访问的教程具有重要意义；同时，GPT 对中文、英文具有不同的理解能力，本教程在多次对比、实验之后确定了效果大致相当的中文 Prompt，支持学习者研究如何提升 ChatGPT 在中文语境下的理解与生成能力。

## 内容大纲

### 一、面向开发者的 Prompt Engineering

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

### 五、使用 Gradio 搭建生成式 AI 应用

注：吴恩达《Building Generative AI Applications with Gradio》课程中文版

 **目录：**

1. 简介 Introduction @韩颐堃
2. 图像总结应用 Image Captioning App @宋志学
3. NLP 任务接口 NLP Tasks Interface @宋志学
4. 图像生成应用 Image Generation App @小饭同学
5. 描述与生成游戏 Describe and Generate Game @小饭同学
6. 与任意 LLM 交流 Chat with Any LLM @韩颐堃
7. 总结 Conclusion @韩颐堃

### 六、评估改进生成式 AI

注：吴恩达《Evaluating and Debugging Generative AI》课程中文版

 **目录：**

1. 简介 Introduction @高立业
2. 测量权重和偏差 W&B @陈逸涵
3. 训练一个扩散模型 Traing a Diffusion Model with W&B @苟晓攀
4. 评估扩散模型 Evaluating Diffusion Models @苟晓攀
5. 评估与追踪 LLM LLM Evaluation and Tracing with W&B @陈逸涵
6. 微调语言模型 Finetuing a Language Model  @高立业
7. 总结 Conclusion @高立业
  
### 七、微调大语言模型

注：吴恩达《Finetuning Large Language Model》课程中文版

**目录：**

1. 简介 Introduction @韩颐堃
2. 为什么要微调 Why Finetune @宋志学
3. 微调的应用场景 Where Finetuning Fits in @陈逸涵
4. 指令微调 Instruction Tuning @韩颐堃
5. 数据处理 Data Proparation @高立业
6. 训练过程 Training Process @王熠明
7. 评估迭代 Evalution and Itration @邓宇文
8. 入门注意事项 Considration on Getting Started Now @韩颐堃
9. 总结 Conclusion @韩颐堃

### 配套视频

双语字幕视频：[吴恩达 x OpenAI的Prompt Engineering课程专业翻译版](https://www.bilibili.com/video/BV1Bo4y1A7FU/?share_source=copy_web) @万礼行

## 致谢

**核心贡献者**

- [邹雨衡-项目负责人](https://github.com/logan-zou)（Datawhale成员-对外经济贸易大学研究生）
- [长琴-项目发起人](https://yam.gift/)（内容创作者-Datawhale成员-AI算法工程师）
- [玉琳-项目发起人](https://github.com/Sophia-Huang)（内容创作者-Datawhale成员）
- [徐虎-教程编撰者](https://github.com/xuhu0115)（内容创作者-Datawhale成员）
- [刘伟鸿-教程编撰者](https://github.com/Weihong-Liu)（内容创作者-江南大学非全研究生）
- [Joye-教程编撰者](https://Joyenjoye.com)（内容创作者-数据科学家）
- [高立业](https://github.com/0-yy-0)（内容创作者-DataWhale成员-算法工程师）
- [魂兮](https://github.com/wisdom-pan)（内容创作者-前端工程师）
- [宋志学](https://github.com/KMnO4-zx)（内容创作者-Datawhale成员）
- [韩颐堃](https://github.com/YikunHan42)（内容创作者-Datawhale成员）
- [陈逸涵](https://github.com/6forwater29) (内容创作者-Datawhale意向成员-AI爱好者)
- [仲泰](https://github.com/ztgg0228)（内容创作者-Datawhale成员）
- [万礼行](https://github.com/leason-wan)（内容创作者-视频翻译者）
- [王熠明](https://github.com/Bald0Wang)（内容创作者-Datawhale成员）
- [邓宇文](https://github.com/GKDGKD)（内容创作者-Datawhale成员）
- [小饭同学](https://github.com/xinqi-fan)（内容创作者）
- [诸世纪](https://github.com/very-very-very)（内容创作者-算法工程师）
- [Zhang Yixin](https://github.com/YixinZ-NUS)（内容创作者-IT爱好者）
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

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=datawhalechina/prompt-engineering-for-developers&type=Date)](https://star-history.com/#datawhalechina/prompt-engineering-for-developers&Date)


## 关注我们

<div align=center>
<p>扫描下方二维码关注公众号：Datawhale</p>
<img src="figures/qrcode.jpeg" width = "180" height = "180">
</div>
Datawhale 是一个专注于数据科学与 AI 领域的开源组织，汇集了众多领域院校和知名企业的优秀学习者，聚合了一群有开源精神和探索精神的团队成员。微信搜索公众号Datawhale可以加入我们。

## LICENSE
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
