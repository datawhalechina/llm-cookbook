# 第二部分 搭建基于 ChatGPT 的问答系统

ChatGPT 的出现，使真正的智能问答成为可能。强大的指令理解能力、自然语言生成能力是 LLM 的核心，支持了 LLM 以类人的方式去思考、执行并完成用户任务。
基于 ChatGPT API，我们可以快速、便捷地搭建真正的智能问答系统，将“人工智障”真正升格为“人工智能“。
对于开发者来说，**如何能够基于 ChatGPT 搭建一个完整、全面的问答系统**，是极具实战价值与实践意义的。

要搭建基于 ChatGPT 的完整问答系统，除去上一部分所讲述的如何构建 Prompt Engineering 外，还需要完成多个额外的步骤。
例如，处理用户输入提升系统处理能力，使用思维链、提示链来提升问答效果，检查输入保证系统反馈稳定，对系统效果进行评估以实现进一步优化等。
**当 ChatGPT API 提供了足够的智能性，系统的重要性就更充分地展现在保证全面、稳定的效果之上。**

第二部分 搭建基于 ChatGPT 的问答系统，基于吴恩达老师发布的《Building Systems with the ChatGPT API》课程。
这部分在《第一部分 面向开发者的 Prompt Engineering》的基础上，指导开发者如何基于 ChatGPT 提供的 API 开发一个完整的、全面的智能问答系统。
通过代码实践，实现了基于 ChatGPT 开发问答系统的全流程，介绍了基于大模型开发的新范式，值得每一个有志于使用大模型开发应用程序的开发者学习。
如果说，《第一部分 面向开发者的 Prompt Engineering》是开发者入门大模型开发的理论基础，那么从这一部分就是**最有力的实践基础**。
学习这一部分，应当充分演练所提供的代码，做到自我复现并能够结合个人兴趣、特长对所提供的代码进行增添、更改，实现一个更个性化、定制化的问答系统。

本部分的主要内容包括：通过分类与监督的方式检查输入；思维链推理以及提示链的技巧；检查输入；对系统输出进行评估等。

**目录：**

1. 简介 Introduction @Sarai
2. 模型，范式和 token Language Models, the Chat Format and Tokens @仲泰
3. 检查输入-分类 Classification @诸世纪
4. 检查输入-监督 Moderation @诸世纪
5. 思维链推理 Chain of Thought Reasoning @万礼行
6. 提示链 Chaining Prompts @万礼行
7. 检查输出 Check Outputs @仲泰
8. 评估（端到端系统）Evaluation @邹雨衡
9. 评估（简单问答）Evaluation-part1 @陈志宏
10. 评估（复杂问答）Evaluation-part2 @邹雨衡
11. 总结 Conclusion @Sarai
