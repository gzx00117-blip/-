# Electrocatalysis Evidence — 电催化证据库与 Skill

121个独立论文身份、369条可定位论断，用于论文写作、科学绘图和实验规划。本轮新增30篇：8篇JACS、6篇Angew、16篇Nature Communications，均为2024–2026首发记录；其中1篇为理论研究，2篇主要目标为NH2OH。新增每篇含正文重点句段和一幅指定原图分析，记录软件披露、复现路线及边界。

**阅读范围**：5篇阅读正文主要部分，116篇为重点段落/句段阅读；不等于全正文/SI通读、近三年全部顶刊覆盖或模型权重训练。E032继承的2027刊期/首发日期仍待核。新30篇来源为PMC结构化正文和原始图像，图像只存本地，公开库只含原创分析与模板。

## 从这里开始

- [121篇论文目录](analysis/121篇论文索引.md)与[新增30篇读图索引](analysis/新增30篇论文与读图索引.md)。
- [新增30篇学习总结](analysis/新增30篇学习总结.md)：论证设计、工作态与复核项。
- [软件绘图与期刊风格实操](analysis/软件绘图与期刊风格实操.md)：Origin、Matplotlib、ChemDraw、VESTA、Fiji与矢量组版步骤。
- [可编辑训练图](figure_examples/README.md)：3个期刊参数版本、原创SVG、合成CSV与生成脚本。
- [新增60篇目录](analysis/新增60篇论文索引.md)与[本轮学习总结](analysis/新增60篇学习总结.md)：新增证据、相反结果和复核项。
- [跨论文分析与使用框架](analysis/跨论文分析与使用框架.md)：机制、反例、证据边界、写作/图/实验路线。
- [Skill](skill/electrocatalysis-evidence/SKILL.md)：让代理检索、核查与应用知识。
- [机器可读卡片](cards/evidence_cards.json)：claim ID、PDF页码或JATS单元、条件、解释、限制和迁移建议。

E001–E091的页码为**1起始PDF文件页**；E092–E121的U编号为**JATS段落/图注单元**，不是PDF页码。两种定位字段分别校验。旧卡DOI在PDF、新卡DOI在JATS article-id中核对；E077印刷DOI定位为p.11，并以Crossref核验身份。最终卷页/出版日期未全部外部核验。

## 安装与调用

需要 Python 3.10+，核心检索脚本只用标准库；训练绘图依赖见`figure_examples/requirements.txt`。下载/克隆本仓库后，从仓库目录运行：

```powershell
python scripts/install_skill.py
python scripts/query_evidence.py "供氢"
python scripts/query_evidence.py "C60 electron"
python scripts/query_evidence.py --card E029
python scripts/query_evidence.py "软件 VESTA"
python scripts/check_faraday.py --substrate NO3 --rate-mmol 1 --current-ma 214.41
python scripts/validate_library.py
```

安装会把 skill 复制到当前用户 `.agents/skills/electrocatalysis-evidence`，先备份已有版本；只在本机生成库位置文件。可用 `--skills-dir` 指定其他技能目录。下一次会话可显式要求：

> 使用 $electrocatalysis-evidence，检索支持和反对“分子修饰促进有效供氢”的证据，逐条给出 DOI、claim ID 和PDF页码或JATS单元，并区分文献结果与我的样品假设。

## 可选：连接自己的本地全文

本仓库不含 PDF、提取全文或 Zotero 数据库。若已有配套本地语料（含 `inventory.json` 和 `texts/{doc_id}.json`），运行：

```powershell
python scripts/install_skill.py --corpus "你的本地语料目录"
python scripts/query_evidence.py --card E001 --source-pages 7-8
python scripts/query_evidence.py --card E096 --source-units 19,45
```

可重复使用`--corpus`配置多个日期批次，或通过`ELECTROCATALYSIS_CORPUS`指定一个路径。本地路径配置被Git忽略。缺少原文时只使用卡片已支持的论断，新数值/谱峰回到合法获取的论文。检索是关键词和少量中英同义词扩展，不是向量语义检索。

## 使用边界

文献不能替实际样品补写合成条件、价态或机制。强度不等于速率，ΔG 不等于活化势垒，普通 CuNi 不等于 Ni4N/Cu，NO2RR 不等于 NO3RR。跨条件最优 FE、产率、槽压和寿命不可拼接。论文原图与逐字段落不包含在公开库中；源文件哈希仅用于追溯身份。

本库保存的是原创分析和调用规则；换电脑需要同步仓库与 skill。没有自动阅读/定期更新任务。新增或反证应更新阅读范围与具体 claim，保留历史记录，不把提取成功计为已读。

## GitHub 登录

打开 [GitHub 登录页](https://github.com/login)，输入用户名或注册邮箱与密码；开启双重验证时按页面完成。密码、验证码和恢复码只输入 GitHub，勿放入本仓库或聊天。[官方认证说明](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)。浏览器登录与本机 Git 推送认证是两回事，本库亦可使用已连接的 GitHub 工具同步。
