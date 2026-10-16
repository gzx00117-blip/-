# Electrocatalysis Evidence — 电催化证据库与 Skill

31 个独立 DOI 的论文分析、99 条可定位论断，用于论文写作、科学绘图和实验规划。以 NO3RR、Cu/Ni、供氢与分子微环境为主，包含富勒烯、CO2RR、尿素耦合和相邻反应作为有边界的设计参考。

**阅读范围**：前 5 篇阅读正文主要部分，后 26 篇按问题阅读重点段落；逐卡记录 PDF 页码与范围。不是全部 31 篇正文/SI 的逐字通读，不代表近三年全部顶刊，也不是模型权重训练。分析由 AI 完成，尚未经独立实验或人工逐项复核。

## 从这里开始

- [31 篇论文目录](analysis/31篇论文索引.md)：DOI、题目和卡片链接。
- [跨论文分析与使用框架](analysis/跨论文分析与使用框架.md)：机制、反例、证据边界、写作/图/实验路线。
- [Skill](skill/electrocatalysis-evidence/SKILL.md)：让代理检索、核查与应用知识。
- [机器可读卡片](cards/evidence_cards.json)：claim ID、PDF 页码、条件、解释、限制和迁移建议。

所有页码均为 **1 起始 PDF 文件页**，不一定是期刊印刷页码。DOI 在对应 PDF 首两页核对；最终卷页/出版日期未全部外部核验。

## 安装与调用

需要 Python 3.10+，核心脚本只用标准库。下载/克隆本仓库后，从仓库目录运行：

```powershell
python scripts/install_skill.py
python scripts/query_evidence.py "供氢"
python scripts/query_evidence.py "C60 electron"
python scripts/query_evidence.py --card E029
python scripts/validate_library.py
```

安装会把 skill 复制到当前用户 `.agents/skills/electrocatalysis-evidence`，先备份已有版本；只在本机生成库位置文件。可用 `--skills-dir` 指定其他技能目录。下一次会话可显式要求：

> 使用 $electrocatalysis-evidence，检索支持和反对“分子修饰促进有效供氢”的证据，逐条给出 DOI、claim ID 和 PDF 页码，并区分文献结果与我的样品假设。

## 可选：连接自己的本地全文

本仓库不含 PDF、提取全文或 Zotero 数据库。若已有配套本地语料（含 `inventory.json` 和 `texts/{doc_id}.json`），运行：

```powershell
python scripts/install_skill.py --corpus "你的本地语料目录"
python scripts/query_evidence.py --card E001 --source-pages 7-8
```

也可通过 `--corpus` 或 `ELECTROCATALYSIS_CORPUS` 指定路径。本地路径配置被 Git 忽略。缺少原文时只使用卡片已支持的论断，需核对的新数值/谱峰应回到合法获取的论文。检索是关键词和少量中英同义词扩展，不是向量语义检索。

## 使用边界

文献不能替实际样品补写合成条件、价态或机制。强度不等于速率，ΔG 不等于活化势垒，普通 CuNi 不等于 Ni4N/Cu，NO2RR 不等于 NO3RR。跨条件最优 FE、产率、槽压和寿命不可拼接。论文原图与逐字段落不包含在公开库中；源文件哈希仅用于追溯身份。

本库保存的是原创分析和调用规则；换电脑需要同步仓库与 skill。没有自动阅读/定期更新任务。新增或反证应更新阅读范围与具体 claim，保留历史记录，不把提取成功计为已读。

## GitHub 登录

打开 [GitHub 登录页](https://github.com/login)，输入用户名或注册邮箱与密码；开启双重验证时按页面完成。密码、验证码和恢复码只输入 GitHub，勿放入本仓库或聊天。[官方认证说明](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)。浏览器登录与本机 Git 推送认证是两回事，本库亦可使用已连接的 GitHub 工具同步。
