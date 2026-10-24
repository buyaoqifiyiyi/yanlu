# 上游与兼容说明

- 来源：[obra/superpowers](https://github.com/obra/superpowers)
- 快照：`b739a8af570e10a95898f2bdf6cec97467fa6c12`，2026-10-21 核对；上游配置版本 7.0.0。
- 本机版本：`0.1.0-local-pilot`，独立命名的精简改编，并非官方完整插件。
- 许可证：MIT，版权及许可原文随包保留于 `../LICENSE`。

## 采用的方法

| 来源 | 取用方法 | 本机适配 |
| --- | --- | --- |
| [subagent-driven-development](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/skills/subagent-driven-development/SKILL.md) | 文件台账、任务身份、续接、精确交接、需求及质量核对 | 按依赖与工作量委派，避免每个小任务固定创建子代理；不用上游 Bash 工作区脚本 |
| [verification-before-completion](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/skills/verification-before-completion/SKILL.md) | 用实际命令和产物支撑完成声明 | 绑定被验文件及相关变化；保留本次有效证据，不要求每条回复都重复运行 |
| [writing-plans](https://github.com/obra/superpowers/blob/b739a8af570e10a95898f2bdf6cec97467fa6c12/skills/writing-plans/SKILL.md) | 明确文件、依赖、可观察验收及交付 | 复用项目计划，按任务粒度记录，不把完整实现预写为长计划 |

## 保留的本机行为

方向明确就执行；测试按风险与项目方法选择；复用既有专业技能；阶段性汇报；只在当前授权范围工作。入口面向多步骤编码、计划续接及用户已请求的跨工具任务交接；普通问答、资料调研和孤立小改动沿用已有流程，不自动建立台账。3.1 的 ECC 增量来源及限定见[包来源](../../../references/upstream.md#310-ecc-评估与交接方法增量)。

## 更新与验证边界

此包是固定快照上的本机适配，不自动跟随上游。更新时先比较上述来源与本机差异，再用隔离任务验证。结构校验、显式调用实测、宿主发现、自动触发及长期效果是不同证据层级；安装本身不证明效果改善。
