---
name: yanlu
description: 编码修复重构、性能诊断、TDD、正确性/复杂度审查、模块与领域设计、原型、PR、调研与证据综合、代码库导览、任务续接与跨工具交接、人工配置向导、方案质询、Agent文档、读者文案防御性措辞审查/改写，以及技能创建评估、Agent/提示词任务验收和资料蒸馏。兼容code-review/codebase-design/diagnosing-bugs/domain-modeling/grilling/pr/prototype/research/superpowers-workflow/tdd/wizard/writing-for-agents和Ponytail文字口令；只读所需模块，视觉设计用绘枢、剪辑用剪辑入口，普通任务不启动技能优化实验。
license: See LICENSE, NOTICE and source-specific licenses
metadata:
  version: "3.2.1"
---

# 衍炉 · Yanlu · 工程与技能方法单入口

先读 [共同原则](references/operating-principles.md)，只加载当前任务需要的分支。`SKILL_ROOT`为Yanlu包根；`MODULE_ROOT`为下表具体GUIDE.md所在目录。迁移模块的scripts/模板/局部引用从MODULE_ROOT解析，不能错用包根或当前工作目录。模块不是每次必跑的阶段。

| 任务/旧文字口令 | 读取模块 | 边界 |
|---|---|---|
| 普通编码、修复、重构；ponytail及lite/full/ultra/off | [编码](references/coding.md) | 默认full，仅编码档位在会话内持续 |
| code-review/yanlu code-review、审查指定改动的标准/需求/正确性 | [双轴审查](modules/code-review/GUIDE.md) | 只读；保留Standards和Spec，不退化成只看删代码 |
| ponytail-review/yanlu review/yanlu complexity、只审过度工程 | [diff复杂度](references/complexity-review.md) | 只读、单次；保留原`yanlu review`为复杂度审查；普通正确性审查按明确任务路由 |
| ponytail-audit/yanlu audit、全仓过度工程 | [仓库复杂度](references/complexity-audit.md) | 只读、单次 |
| 难复现/根因不明/性能回归、diagnosing-bugs | [诊断](modules/diagnosing-bugs/GUIDE.md) | 明确局部错误用编码短路径，不造固定假设数量 |
| 明确测试先行、集成行为测试、tdd | [TDD](modules/tdd/GUIDE.md) | 只在适用或明确要求时启用，不每次强制red-green |
| 模块接口/依赖接缝、codebase-design | [模块设计](modules/codebase-design/GUIDE.md) | 保留项目术语与有独有回归价值的旧测试 |
| 领域词汇、GLOSSARY、ADR、domain-modeling | [领域建模](modules/domain-modeling/GUIDE.md) | 按实际需要建文档，不做无关命名改造 |
| 原型验证逻辑/状态或UI方向、prototype | [原型](modules/prototype/GUIDE.md) | 默认为探索；不默认正式实现/commit/issue |
| PR正文、pr | [PR说明](modules/pr/GUIDE.md) | 写说明不等于创建/发布PR，仓库模板优先 |
| 事实/技术/项目来源调研、证据综合、代码库导览、research | [调研](modules/research/GUIDE.md) | 多源综合与只读导览按需加载；检索执行沿Web Access/专用连接器，按用户指定位置交付 |
| 多步跨模块任务/中断续接与跨工具交接、superpowers-workflow | [协调](modules/superpowers-workflow/GUIDE.md) | 小改不强制台账、TDD、访谈或子代理 |
| 需要人亲自做的账号/配置步骤、wizard | [人工向导](modules/wizard/GUIDE.md) | 只为无法代办步骤；验证目标.env解析器；不自动安装shell |
| 用户要求质询计划、grilling | [方案质询](modules/grilling/GUIDE.md) | 只问会影响决策的问题，不无限访谈 |
| 编写Agent指令、AGENTS/CLAUDE、writing-for-agents | [Agent文档](modules/writing-for-agents/GUIDE.md) | 作用是写法，不取代宿主包装和用户授权 |
| 面向读者的文案防御性措辞审查/改写；stss audit/rewrite | [读者文案](references/reader-prose.md) | audit只报意见，rewrite返回改写；普通编码和一般润色不加载，不改变编码档位 |
| 创建/维护/评估技能或内容蒸馏 | [技能工作流](references/skill-workflow.md) | 才进入来源、快照、相称验证或效果比较 |
| 评估Agent/提示词任务能力、回归或重复运行稳定性 | [验证](references/validate.md)、[记录口径](references/evaluation-records.md) | 按请求固定任务与判据；只评估不改目标，不给普通任务追加实验 |
| shortcut延期、命令帮助、作者实验 | [台账](references/shortcut-debt.md)、[帮助](references/ponytail-help.md)、[外部实验](references/external-benchmark.md) | 只读功能不改变编码档位 |
| 实际证据支持改本包 | [反馈迭代](references/feedback.md) | 不把每次交付扩成优化实验 |

## 组合与互调

模块正文中的旧技能名是本表的包内模式，不代表需要安装或启动已归档独立技能。需要codebase-design/TDD/code-review/research/Agent文档等时，从本表读取对应GUIDE，按原条件执行。复杂度审查、正确性审查、技能审查分别选择；要求“审查并修复”才进入明确授权的修改范围。

视觉UI的具体设计、已有截图实现、品牌板与图片参考可交由可选伴随技能 [绘枢](https://github.com/buyaoqifiyiyi/huishu)，先确认已安装；原型的逻辑/实验边界仍由本包保留。联网资料用实际可用Web Access；OpenAI产品先遵循宿主官方文档来源规则。系统skill-creator/installer及review-agent仍可按宿主职责调用，不删除系统/插件资源或伪造工具。

`yanlu off`、`ponytail off`、`stop ponytail`、`normal mode`关闭会话编码精简模式；普通任务、review/help、TDD、调研或技能维护都不自动恢复。明确启用编码模式或指定lite/full/ultra才恢复；其他明确请求的功能仍可运行。只有技能名无任务时简述模式，不启动维护。

旧文字口令仍可识别；宿主只注册Yanlu，不承诺旧独立$技能ID或选择器句柄。Stop That Shit、stss仅保留方法或文字意图兼容；Guard/Hook、审计、模式解析器和机器拦截不在本包内。

[记录比较器](references/evaluation-records.md)只比较已有记录，不自动执行或采用。[维护映射](references/maintenance.md)与[来源](references/upstream.md)定义本地维护源。
