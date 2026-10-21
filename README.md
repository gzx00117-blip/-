# Electrocatalysis Evidence — 电催化证据库与 Skill

151个独立DOI、459条可定位论断，用于论文写作、科学绘图和实验规划。2026-10-21新增30篇：JACS 5、Angew 3、Nature Communications 12、Communications Chemistry 2、Science Advances 1、Chemical Science 7。此轮强化定量、统计、可比性、机理反证、失活及系统边界；包含2篇综述/观点和1篇理论研究，分别标记类型。

**阅读范围**：累计5篇阅读正文主要部分，146篇为重点段落/句段阅读；本轮30篇各看一幅指定原图，6篇额外核查24个SI物理页。不等于全正文/SI通读、近三年全部顶刊覆盖或模型权重训练。E032继承的2027刊期/首发日期仍待核。原文、图像和SI只存本地，公开库仅含原创分析、引用元数据和工具。

## 从这里开始

- [151篇论文目录](analysis/151篇论文索引.md)与[本轮综合文献能力总结](analysis/新增30篇综合文献能力学习总结_2026-10-21.md)。
- [综合阅读与核查工作流](skill/electrocatalysis-evidence/references/critical-reading.md)：反例检索、条件对比、质量基准/电荷/空白计算和引用导出。
- [本轮30幅读图记录](analysis/methods_visual_receipts.json)、[6篇SI核查范围](analysis/methods_si_reading_receipts.json)、[30篇引用元数据](analysis/methods_bibliography.json)。
- [此前121篇目录](analysis/121篇论文索引.md)与[此前读图索引](analysis/新增30篇论文与读图索引.md)，作为历史批次保留。
- [新增30篇学习总结](analysis/新增30篇学习总结.md)：论证设计、工作态与复核项。
- [软件绘图与期刊风格实操](analysis/软件绘图与期刊风格实操.md)：Origin、Matplotlib、ChemDraw、VESTA、Fiji与矢量组版步骤。
- [可编辑训练图](figure_examples/README.md)：3个期刊参数版本、原创SVG、合成CSV与生成脚本。
- [新增60篇目录](analysis/新增60篇论文索引.md)与[本轮学习总结](analysis/新增60篇学习总结.md)：新增证据、相反结果和复核项。
- [跨论文分析与使用框架](analysis/跨论文分析与使用框架.md)：机制、反例、证据边界、写作/图/实验路线。
- [Skill](skill/electrocatalysis-evidence/SKILL.md)：让代理检索、核查与应用知识。
- [机器可读卡片](cards/evidence_cards.json)：claim ID、PDF页码或JATS单元、条件、解释、限制和迁移建议。

E001–E091的页码为**1起始PDF文件页**；E092–E151的U编号为**JATS段落/图注单元**，不是PDF页码。新批次SI以独立PDF物理页定位，三类选择器分开校验。旧卡DOI在PDF、新卡DOI在JATS article-id中核对；E122–E151另经Crossref核验身份/引用元数据。历史记录最终卷页/出版日期未全部外部核验，元数据核验不等于完整撤稿/更正排查。

## 安装与调用

需要 Python 3.10+，核心检索脚本只用标准库；训练绘图依赖见`figure_examples/requirements.txt`。下载/克隆本仓库后，从仓库目录运行：

```powershell
python scripts/install_skill.py
python scripts/query_evidence.py "供氢"
python scripts/query_evidence.py "C60 electron"
python scripts/query_evidence.py --card E029
python scripts/query_evidence.py "软件 VESTA"
python scripts/query_evidence.py --capability counterexample
python scripts/compare_conditions.py --a E151-performance --b E151-raman
python scripts/quant_checks.py concentration --mg-l 14.0067 --basis N
python scripts/export_citations.py --card E144
python scripts/check_faraday.py --substrate NO3 --rate-mmol 1 --current-ma 214.41
python scripts/validate_library.py
python scripts/test_capabilities.py
```

安装会把 skill 复制到当前用户 `.agents/skills/electrocatalysis-evidence`，先备份已有版本；只在本机生成库位置文件。可用 `--skills-dir` 指定其他技能目录。下一次会话可显式要求：

> 使用 $electrocatalysis-evidence，检索支持和反对“分子修饰促进有效供氢”的证据，逐条给出 DOI、claim ID 和PDF页码或JATS单元，并区分文献结果与我的样品假设。

## 可选：连接自己的本地全文

本仓库不含 PDF、提取全文或 Zotero 数据库。若已有配套本地语料（含 `inventory.json` 和 `texts/{doc_id}.json`），运行：

```powershell
python scripts/install_skill.py --corpus "你的本地语料目录"
python scripts/query_evidence.py --card E001 --source-pages 7-8
python scripts/query_evidence.py --card E096 --source-units 19,45
python scripts/query_evidence.py --card E134 --si-pages 3-4
```

可重复使用`--corpus`配置多个日期批次，或通过`ELECTROCATALYSIS_CORPUS`指定一个路径。本地路径配置被Git忽略。缺少原文时只使用卡片已支持的论断，新数值/谱峰回到合法获取的论文。检索是关键词和少量中英同义词扩展，不是向量语义检索。

## 使用边界

文献不能替实际样品补写合成条件、价态或机制。强度不等于速率，ΔG 不等于活化势垒，普通 CuNi 不等于 Ni4N/Cu，NO2RR 不等于 NO3RR。跨条件最优 FE、产率、槽压和寿命不可拼接。论文原图与逐字段落不包含在公开库中；源文件哈希仅用于追溯身份。

本库保存的是原创分析和调用规则；换电脑需要同步仓库与 skill。没有自动阅读/定期更新任务。新增或反证应更新阅读范围与具体 claim，保留历史记录，不把提取成功计为已读。

后续正式科学图按用户要求默认用图形软件创建并交付原生可编辑工程：数据图Origin `.opju`，结构与组图PowerPoint/矢量图层，按需保留ChemDraw、VESTA、Fiji或Blender源文件。历史Python训练图仅保留为既有示例，不是后续成图默认流程。

## GitHub 登录

打开 [GitHub 登录页](https://github.com/login)，输入用户名或注册邮箱与密码；开启双重验证时按页面完成。密码、验证码和恢复码只输入 GitHub，勿放入本仓库或聊天。[官方认证说明](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)。浏览器登录与本机 Git 推送认证是两回事，本库亦可使用已连接的 GitHub 工具同步。
