# 上游溯源与合并决定

衍炉 Yanlu 1.1.0 是独立改编，2026-10-21 整合以下 MIT 项目的方法与指令。它不是上游联合发布，也未合并 Git 历史；不声称获得上游评审分数或继承其效果证明。1.0.0 整合女娲与达尔文，1.1.0 新增仓颉内容蒸馏方法。

| 项目 | 固定来源版本 | 使用内容 |
|---|---|---|
| [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill) | `7812110bf7e5a2b01b6aa5a738568044121bbfa2` | 多源研究、心智模型验证、人物/主题分流、来源及诚实边界 |
| [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill) | `8a8b66258e3c45d6ae4aea39719468c6428fcb0a` | 基线与候选测试、独立配对评审、有限轮次、保留或回退 |
| [kangarooking/cangjie-skill](https://github.com/kangarooking/cangjie-skill) | `a28de55ba881b9928956a55048f743f7a9e3b23e` | 任务优先的内容筛选、RIA++ 能力卡、独立入口筛选、来源覆盖与压力测试 |

主要参考：[女娲入口](https://github.com/alchaincyf/nuwa-skill/blob/7812110bf7e5a2b01b6aa5a738568044121bbfa2/SKILL.md)、[提炼框架](https://github.com/alchaincyf/nuwa-skill/blob/7812110bf7e5a2b01b6aa5a738568044121bbfa2/references/extraction-framework.md)、[人物模板](https://github.com/alchaincyf/nuwa-skill/blob/7812110bf7e5a2b01b6aa5a738568044121bbfa2/references/skill-template.md)、[达尔文入口](https://github.com/alchaincyf/darwin-skill/blob/8a8b66258e3c45d6ae4aea39719468c6428fcb0a/SKILL.md)。上游版权声明见本包 LICENSE。

## 合并与调整

1. 创建、优化、更新共享验证流程，删除重复的精炼与评分环节。
2. 固定目录快照和 SHA256 取代依赖可变 HEAD 的版本对照，避免先 commit 后把新 HEAD 当旧版的问题。
3. 以用户实际目标与工具定位目录，移除工作流中的 `.claude/skills` 固定路径；保留目标自身合理的宿主限制。
4. 用实际任务结果及匿名独立评审决定采用；结构维度辅助诊断，去掉固定总分、作者风格和符号加分。
5. 来源按可核实的独立材料记录，不用关键词计数认证一手资料，不按发布平台排除本人原文。
6. 允许修复必要脚本和参考资料，避免只改文案而留下实现缺陷；默认在完整候选副本操作。
7. 尊重已有授权，去掉固定的重复确认；保留目标方向、外部副作用和正式采用边界。
8. 调研规模和评委数量由任务、风险及预算决定；没有真实任务和独立比较时不宣称效果提升。

没有打包上游宣传图片、人物示例全集、截图依赖、自动版本检查或任何模型接口。辅助快照脚本为本次新增，纯标准库。

## 1.1.0 仓颉适配

参考其固定版本的 [任务优先三关](https://github.com/kangarooking/cangjie-skill/blob/a28de55ba881b9928956a55048f743f7a9e3b23e/methodology/03-stage1.5-triple-verify.md)、[晋级门](https://github.com/kangarooking/cangjie-skill/blob/a28de55ba881b9928956a55048f743f7a9e3b23e/methodology/03b-stage1.6-promotion-gate.md)、[能力卡](https://github.com/kangarooking/cangjie-skill/blob/a28de55ba881b9928956a55048f743f7a9e3b23e/methodology/04-stage2-ria-plus.md) 和 [压力测试](https://github.com/kangarooking/cangjie-skill/blob/a28de55ba881b9928956a55048f743f7a9e3b23e/methodology/06-stage4-pressure-test.md)。

- 人物归因与内容方法分别筛选；完整的 SOP/公式不因只出现一次或不独特而被误删。
- 将其知识验证的 verified 改记为 eligible，并单列实际效果 validation，避免纸面演练被误认为宿主实测。
- 默认单入口管理能力卡，需要独立调用才拆分；合并到衍炉现有快照和验收，不重复引入五路代理或固定确认。
- 保留原文、解释、案例、触发、执行、边界及稳定 ID；使用衍炉的运行记录，不冒充仓颉 Bundle/schema 兼容。
- 只整合方法和文档，未复制仓颉 scripts/schemas，也未实现其确定性编译、事务发布、注册表、回滚或语义更新引擎；快照脚本与 1.0.0 一致。

## 2.0.0 统一维护与评估方法

2026-10-21将本机已适配Ponytail六项正文迁入本包，保留旧名作为轻量入口；不是重新覆盖上游原版。Ponytail固定来源：`DietrichGebert/ponytail@09c434ab73ca43761c5d8b0c5d341926c2fba710`，MIT，完整notice见licenses/ponytail-MIT.txt。

| 新参考 | 固定提交 | 选择性吸收 | 未引入 |
|---|---|---|---|
| [GEPA](https://github.com/gepa-ai/gepa) | 8f287de942f41a6d1e0e7e5b2d576247c4bedee9 | 具体失败反馈定位责任模块；明确提案、复测与最终验收预算 | SDK、外部模型调用、Pareto搜索与远端eval服务 |
| [Anthropic skill-creator](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator) | dbd4588f9e1033efb41dad4bef2f7947c8993d44 | 检查断言自身的区分度、缺失终点和不可核查证据 | Claude CLI执行器、test集选优当holdout、跳过缺失结果或字符充token的聚合 |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | 6af5a87acb6ed4f20d7541e8de3677d911b1d7f0 | 固定案例、显式判据、逐项指标与回归对照 | npm运行库、云端服务、外部provider和可执行配置 |

GEPA和Promptfoo为MIT；所读Anthropic skill-creator组件为Apache-2.0，不将其仓库所有目录一概称同许可证。完整文本随包保留。这里是方法改编及本地工具独立实现，不是三个项目代码或效果的移植。

另外核查SkillsBench、mcollina/skills、Hermes和autoresearch以及ECC：已有重复方法只作交叉参考；容器/独立agent/训练依赖或无限外循环不合入；ECC会话hooks不接线。项目宣传、外部基准和静态发现不转成本机增益。

## 2.1.0 单入口融合

用户明确要求全部功能完整融合到Yanlu，不保留六个独立UI入口。Ponytail六项正文、模式、来源与许可保留；旧名改为本入口识别的文字口令，宿主只注册yanlu，无法承诺旧独立技能ID的选择器句柄仍可用。编码自动触发范围迁入Yanlu description与全局指引，普通编码仍只读轻量模块；归档原入口供恢复，来源追踪不重新安装它们。

## 3.1.0 ECC 评估与交接方法增量

2026-10-24 按用户授权，从 [affaan-m/ECC 固定提交](https://github.com/affaan-m/ECC/tree/90606c8315ee09cafc303515c5f33024db6b9882)选择性改编下列方法；MIT，Copyright (c) 2026 Affaan Mustafa，完整文本见 `licenses/ecc-MIT.txt`。本节补充并限定此前“ECC 只作参考、Hooks 不接线”的记录；不改变其他来源及已保留定制。

| 来源 | 本地采用 | 保留的边界 |
|---|---|---|
| [eval-harness](https://github.com/affaan-m/ECC/blob/90606c8315ee09cafc303515c5f33024db6b9882/skills/eval-harness/SKILL.md) | validate.md 的能力/回归分类；evaluation-records.md 的可选重复试验口径；现有入口按需路由 | 沿用本地快照、冻结套件、独立评审、保留集、缺失项和逐项回归规则；不照搬固定阈值或示例成功率 |
| [unified-memory](https://github.com/affaan-m/ECC/blob/90606c8315ee09cafc303515c5f33024db6b9882/skills/unified-memory/SKILL.md) 与 [Memory Vault 设计](https://github.com/affaan-m/ECC/blob/90606c8315ee09cafc303515c5f33024db6b9882/docs/design/ecc-memory-vault.md) | 协调模块/台账补交接来源、时间和证据；现有记忆库规则补检索完整性、状态与替代关系 | 沿用用户已授权的记忆入口、分类、自动保存及纠正流程；不要求为既有授权重复审批，不把 ECC 的人工晋升要求移植成新的统一门禁 |

源码核查显示：该提交 eval-harness 的候选执行 Gate 明确禁用，pass@k/pass^k 没有配套重复试验调度或计算器；记忆运行时为有界词法检索，搜索返回不完整诊断，ID 读取会拒绝部分扫描。只借鉴与本地缺口对应的方法，不把这些运行能力写成本机已安装。

本次没有移植 ECC CLI、MCP、schema、Hooks、数据库、候选执行器或后台采集，也没有修改 compare_runs.py 的数据契约。记忆规则仍在现有记忆库 AGENTS.md 维护；本包只链接当前记忆入口与任务台账，不维护第二套规则正文。结构、隔离案例与宿主新会话自动加载/长期效果分别验收。

## 3.2.0 Agency Agents 方法增量

2026-10-24 从 [msitarzewski/agency-agents 固定提交](https://github.com/msitarzewski/agency-agents/tree/4e3ac3ca6604c75113f52c695dbddcc7af928b46)选择性中文改编三项方法。MIT，Copyright (c) 2025 AgentLand Contributors，逐字许可见 [agency-agents-MIT.txt](../licenses/agency-agents-MIT.txt)。源文件 SHA-256、采用位置与排除项见 [integration-20261024-agency.json](integration-20261024-agency.json)。本节追加来源映射，保留上述历史记录。

| 固定来源及段落 | 本地采用 | 调整和排除 |
|---|---|---|
| [Research Synthesist，27–47 行](https://github.com/msitarzewski/agency-agents/blob/4e3ac3ca6604c75113f52c695dbddcc7af928b46/research/research-synthesist.md#L27-L47) | research/references/evidence-synthesis.md；research GUIDE 按需分支 | 同源转述去重、分歧与缺口、必要证据链及检索边界；不强制每个来源打分、完整综述或把无关弱材料变成全篇置信度下限 |
| [Codebase Onboarding Engineer，19–36 行](https://github.com/msitarzewski/agency-agents/blob/4e3ac3ca6604c75113f52c695dbddcc7af928b46/engineering/engineering-codebase-onboarding-engineer.md#L19-L36) | research/references/repository-orientation.md；research GUIDE 和根路由 | 实际入口、代表性执行链、文件职责与已读范围；不强制三层长报告、全仓阅读或一律禁止用户已请求的建议；推断显式标记 |
| [Codebase Archaeologist，121–152 行](https://github.com/msitarzewski/agency-agents/blob/4e3ac3ca6604c75113f52c695dbddcc7af928b46/specialized/specialized-codebase-archaeologist.md#L121-L152) | code-review/references/semantic-consistency.md；code-review 与 diagnosing-bugs 按需引用 | 单位/表示、默认值、状态先后及共同职责；保留 Standards / Spec 两轴和诊断复现；不强制检查所有 handler、四视图台账、默认判缺陷或额外角色复核 |

以上是方法改编，不安装 Agency 角色入口、安装器、插件、运行时或模型服务；不继承人设中的记忆、经验、精度和收益宣称。首批不修改 Prompt Craft、剪辑工作台、全局 AGENTS、自动化或业务项目。候选构建、静态可达、实际任务效果和宿主重新发现分别取证；文档增量不等于效果已提升。

## 3.2.1 Stop That Shit 方法吸收

2026-10-24按用户授权，选择性改编[lennney/stop-that-shit](https://github.com/lennney/stop-that-shit)，固定本机0.2.5提交`8bc1ac558167121e7f28d9fb0bec05c039952206`。本机源文件与Git提交一致；不是上游新发布。完整MIT许可见[stop-that-shit-MIT.txt](../licenses/stop-that-shit-MIT.txt)，源哈希和排除项见[integration-20261024-sts.json](integration-20261024-sts.json)。

| 采用方法 | 本地位置及去重 |
|---|---|
| Stop Ladder中防御效果、支持承诺、等待与最终状态证据 | `operating-principles.md`只补缺失判断；复用既有coding/complexity/global规则，不复制完整阶梯或固定检查流程 |
| stss事实记录、句子用途、删除/校准/移位/保留及事实差异核对 | `reader-prose.md`按需路由；保留audit/rewrite、归因、不确定性及输出边界 |

未迁入Guard/Hook、状态恢复、审计、文件锁、代理容量、模式解析器、CLI、宿主执行拒绝与测试运行时。来源中安装、模式和工具接线说明不成为Yanlu功能；旧文字名不代表旧独立技能ID。采用是去重整合，静态和内容审查不等于业务质量或成本提升。
