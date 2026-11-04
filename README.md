# DVFS 论文精读

面向零基础读者的 CPU / RISC-V / 嵌入式 DVFS 图文阅读项目，基于 [Futuresxy/paper_read](https://github.com/Futuresxy/paper_read)。来源与提交见 [UPSTREAM.md](UPSTREAM.md)，原许可保留。

## 已经能用的内容

- `reviewed/jsa2023-temporal-dvfs/`：依据 21 页原文整理的第一份完整精读，先从频率、能量与控制闭环入门，再逐式推导状态、奖励与 DDQN；重要图表在正文对应位置，并有符号表、代入算例、中英文摘要、实验比较与改进。
- 四个报告：`paper_notes.md`、`ELI5_notes.md`、`figs_notes.md`、`translation_notes.md`，附原文重要图表、八组公式与自绘闭环辅助图；图片可点击放大。
- `preview/index.html`：可直接用浏览器打开的静态阅读入口，无需模型 API 或 Node。
- `content/DVFS/`：同一份笔记已导入 Quartz 内容目录。
- `reading_template.md`：后续每篇论文统一使用的阅读模板。

当前精读由 Codex 根据本地原文整理，未宣称已经运行外部付费模型流水线。双语摘要是明确标注的改写概述，第四份报告是摘要与章节导读，不是全文翻译。

## 本地重新生成阅读网页

在本目录使用 Python 3.10+，建议 3.12：

```powershell
python scripts/build_reviewed_site.py
```

然后打开 `preview/index.html`。命令仅用 Python 标准库，不调用模型，不下载依赖。需要确认使用的 Python 版本：`python --version`。

验证与导入新报告包：

```powershell
python scripts/import_blablapaper.py --source reviewed/jsa2023-temporal-dvfs --content-root content --collection DVFS --tags DVFS,CPU
python -m unittest discover -s scripts -p test_import_blablapaper.py
```

## 师兄的自动生成流程

PDF → MinerU 解析正文与图像 → 文本/视觉模型 → 技术解析、通俗解释、图表解析、翻译 → 校验导入 → Quartz 发布。

核心代码在 `BlaBlaPaper/main.py` 和 `BlaBlaPaper/src/`；提示词在 `prompts.py`；发布校验在 `scripts/import_blablapaper.py`。阶段缓存和部分结果用于中断后继续。完整自动流水线保留原有分块翻译，因此可能比只生成摘要花费更多。

自动读新 PDF 需要你自己的模型 API 和 MinerU 配置。复制 `.env.example` 到 `.env`，填写文字模型、视觉模型、兼容服务地址、API 密钥和 MinerU 令牌。不要把真实 `.env` 上传到 GitHub。

Windows 上可安装依赖后从项目目录运行：

```powershell
python -m pip install -r BlaBlaPaper/requirements.txt
python BlaBlaPaper/main.py C:/path/to/paper.pdf
```

BlaBlaPaper 也支持已解析的正文目录，详见原模块 README；这可以减少对 PDF 解析服务的依赖，但仍需配置模型。当前交付没有运行这些需要凭据的 API 步骤。

## GitHub 发布准备

仓库：[zzxwhu/dvfs-paper-read](https://github.com/zzxwhu/dvfs-paper-read)。Pages 是否发布成功以 Actions 的部署结果为准；源码上传不等于网站已经上线。

在 Settings → Pages 选择 GitHub Actions。`deploy.yml` 保留 Quartz 发布流程，需要 Node 22、依赖安装及 Quartz 插件；本地尚未完成 Quartz 构建验证。`reviewed-static.yml` 可无模型凭据生成静态预览下载包。

要在线自动分析 PDF，使用 Actions 的 `Generate and publish paper notes` 工作流，配置：

| 配置位置 | 名称 | 内容 |
| --- | --- | --- |
| Secret | OPENAI_API_KEY | 所选兼容服务的模型密钥，变量名不限定供应商 |
| Secret | MINERU_API_TOKEN | PDF 解析服务令牌 |
| Variable | MODEL_PROVIDER | 供应商标识 |
| Variable | TEXT_MODEL、IMAGE_MODEL | 文字模型、具备视觉能力的模型 |
| Variable | LLM_BASE_URL、LLM_WIRE_API | 服务地址，接口类型如 chat_completions |

如视觉模型使用另一服务，可设置 IMAGE_API_KEY、IMAGE_BASE_URL、IMAGE_WIRE_API。提交模型生成结果前，仍需核对原文数字、图号和实验参照。

本仓库不包含论文原始 PDF，也不包含你的 SoC 工程、账号凭据或邮箱。原文图表已标注作者和来源，转发时应保留署名。

## Quartz 大资源与教学修订

为便于初始化，仓库不重复提交上游 15 MB 的表情图资源，CI 会从固定上游提交下载并校验 Git blob 哈希；本地完整工具包保留该文件。手工构建前运行 `python scripts/prepare_quartz_assets.py`。省略的是通用 Quartz 文档截图与这个可恢复资源，不省略你的论文图表。

当前学习顺序：从零入门 → 图文技术精读 → 图表回查 → 双语摘要与章节导读。入口显著提供原文页面、PDF 和 DOI。公式源码见 reviewed 中的 equations_source.md；重排符号、教学假设与作者实验均有标注。
