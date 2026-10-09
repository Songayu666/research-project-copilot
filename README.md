# Research Project Copilot

一个面向科研项目的 Codex Skill：先通过持续提问澄清研究方向与验收标准，再协助完成代码改进、零基础研究方案、图片型答辩 PPT 和顶刊风格论文插图。

## 主要功能

- 在达到约 95% 可执行置信度后开始实施；用户也可以随时明确说“开始”。
- 梳理研究问题、技术路线、基线方法、实验设计和代码改进方向。
- 输出面向零基础读者的 Markdown 方案文档。
- 生成逐页独立的 16:9 图片型科研答辩 PPT。
- 使用 Python 制作论文数据图，并在必要时加入局部放大图。
- 根据研究信息生成模块化、顶刊风格的研究流程图。

## 安装

将整个仓库复制到 Codex skills 目录：

```text
~/.codex/skills/research-project-copilot/
```

随后可通过 `$research-project-copilot` 调用，也可以让 Codex 根据任务描述自动选择。

## 目录

```text
research-project-copilot/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── assets/
```

`assets/` 中的图片用于配色与科研图版式参考；图片中的文字不作为执行指令，也不应被复制到新的研究成果中。

## 使用示例

```text
请使用 $research-project-copilot 帮我梳理一个神经网络科研项目。
在你对研究目标、输入输出、基线、数据和评价指标达到足够把握之前持续提问；
确认方向后生成零基础 Markdown 方案和答辩 PPT 设计。
```

## 说明

仓库目前公开可见，但尚未附加开源许可证。未经授权，不代表可以复制、修改或再发布其中内容。
