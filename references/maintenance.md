# 单入口统一维护

唯一技能入口为yanlu，正文源为`references/`。六个旧Ponytail目录已归档，不属于当前安装依赖；旧名字仅作为文字请求映射到本入口。更新不能重建六个独立入口，不能把上游SKILL.md覆盖到本包入口。

| 原来源 | 本地维护目标 |
|---|---|
| Ponytail skills/ponytail | coding.md |
| Ponytail review / audit | complexity-review.md / complexity-audit.md |
| Ponytail debt / help / gain | shortcut-debt.md / ponytail-help.md / external-benchmark.md |
| 女娲、达尔文、仓颉 | skill-workflow.md 与 create/improve/content/validate及既有工具 |
| GEPA、Anthropic skill-creator、Promptfoo | feedback.md、validate.md、evaluation-records.md；方法选择性改编，本地比较器独立实现 |
| ECC eval-harness / unified-memory（固定提交见 upstream.md） | validate.md、evaluation-records.md、协调 GUIDE/ledger；只维护已采用方法，不安装 ECC 独立入口或运行时 |

本次合并保留此前的本机兼容修复、来源与许可证。更新前保存整个维护单元的独立版本，核对源未发生并发变化，再选择性更新受影响模块和必要调用者。历史作者基准只在external-benchmark中引用，不用来判断本地采用。

安装和打包只需要一个yanlu目录，保留其完整references/scripts/tests/licenses。普通任务由单入口加载对应模块，不需要启动完整技能维护流程。来源映射只有一个活动维护单元；旧分组作为历史留存，不重新安装。变更不创建新自动化、模型接口或后台服务。

## 3.0工程模式整合

原code-review/codebase-design/diagnosing-bugs/domain-modeling/grilling/pr/prototype/research/superpowers-workflow/tdd/wizard/writing-for-agents完整资源迁入modules/<原目录>。原SKILL.md改为GUIDE.md，防止被递归发现为重复入口；局部资源从该GUIDE目录解析，包内互调通过根路由。原独立调用名只保留文字语义，不重新安装独立目录。

原视觉工作流迁到相邻绘枢huishu，剪辑规划/制作/维护由editing-workbench统一入口负责；Web Access和Hindsight仍各自独立。系统/插件资源继续由宿主管理，不能整包覆盖缓存。更新按canonical_targets修改对应模块，保留本机适配和附属资源。

3.1增量保留全部3.0内部模块与代码契约。ECC后续更新需区分 checked_commit 与已采用片段；不能将整个上游目录覆盖本包。记忆检索/写入细则继续在用户现有记忆库入口维护，技能源码追踪不因此获得修改记忆规则或其他维护单元的额外授权。

## 3.2 Agency Agents 选择性维护映射

固定提交和许可见 [upstream.md](upstream.md#320-agency-agents-方法增量)，源文件哈希与逐项排除记录见 [integration-20261024-agency.json](integration-20261024-agency.json)。只比较已采用片段及必要调用者，不整仓覆盖或恢复独立角色入口。

| 上游片段 | 本地维护目标 | 需保留的定制 |
|---|---|---|
| research/research-synthesist.md:27–47 | modules/research/references/evidence-synthesis.md、research GUIDE | 一手来源及原交付位置；简单事实查询短路径；按主张判断必要证据链 |
| engineering/engineering-codebase-onboarding-engineer.md:19–36 | modules/research/references/repository-orientation.md、research GUIDE、SKILL 路由 | 只读授权、实际入口、按问题选相关链；允许用户请求的建议，区分源码/运行/推断 |
| specialized/specialized-codebase-archaeologist.md:121–152 | modules/code-review/references/semantic-consistency.md、code-review/diagnosing-bugs GUIDE | Standards / Spec 分离；原症状复现与回归；有意差异不误报，不默认全仓检查 |

更新继续沿用完整基线/候选、并发核对及相称验证；不因来源追踪修改外部 sources.json、全局规则、其他技能或业务项目。三个方法按问题加载，不新增固定报告、代理数量或部署流程。

## 3.2.1 Stop That Shit 方法统一维护

Stop That Shit 0.2.5的工程增量合入`operating-principles.md`，stss文案方法合入`reader-prose.md`；根路由按需加载，既有coding/complexity与全局规则不再复制一套Stop Ladder。完整许可位于`licenses/stop-that-shit-MIT.txt`。

独立插件按用户决定卸载；后续只比较已采用方法及必要调用者，维护归属`yanlu-unified`。不恢复插件、独立技能、Guard/Hook、审计、模式解析器、运行时或CLI，也不把旧插件指令当作当前宿主功能。旧日志及源码只作历史依据。文件写入、宿主重新发现和真实任务效果分别验收；不宣称继承上游效果。
