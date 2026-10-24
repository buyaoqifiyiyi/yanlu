# 衍炉 · Yanlu

当前版本：**3.2.1**。

工程方法与技能维护的单入口技能，按需加载编码、诊断、测试、审查、调研、任务交接和技能迭代模块，并包含面向读者的文案防御性措辞审查与改写。

## 安装

本仓库根目录就是一个完整技能包，`SKILL.md`是入口，`modules/`和`references/`按任务加载。以 Codex 的用户技能目录为例，将整个仓库克隆到技能目录中的`yanlu`文件夹；已有同名目录时先备份并比较，不直接覆盖。

```powershell
New-Item -ItemType Directory -Force "$HOME/.codex/skills" | Out-Null
git clone https://github.com/buyaoqifiyiyi/yanlu.git "$HOME/.codex/skills/yanlu"
```

也可以下载仓库 ZIP，解压后将包含`SKILL.md`的整个文件夹放入宿主的技能目录。刷新技能列表或重新打开会话后使用`$yanlu`；其他支持同类技能结构的宿主按其实际技能目录安装。

## 使用示例

- “使用 Yanlu 修复这个问题，只改必要范围并验证。”
- “审查这份 diff 的正确性和不必要复杂度。”
- “stss audit：只指出这段文案中影响表达的防御性措辞。”

只加载当前任务需要的模块。明确的用户要求、只读限制、现有项目规则及宿主工具权限优先；技能文档本身不授予外部操作权限。

## 资源与验证边界

技能快照与记录比较脚本需要 Python 3.11+。方法正文可独立使用；视觉工作可另装 [Huishu](https://github.com/buyaoqifiyiyi/huishu)。已吸收 Stop That Shit/stss 的方法，未包含 Guard、Hook、审计存储或机器强制拦截。

发布副本保留模块、数据、脚本、模板与来源许可。历史记录中的私人绝对路径以`<local-evidence>`替代；对应历史快照未随仓库发布，原有提交和哈希仍用于来源追溯。历史校验不是当前业务效果证明；能读取技能、宿主自动选择以及真实任务完成需分别验证。

## 来源与许可

这是多源改编包，原始内容与引入内容按各自许可分发。请同时阅读 [LICENSE](LICENSE)、[NOTICE](NOTICE)、[上游溯源](references/upstream.md) 与 [licenses/](licenses/)，保留源作者归属和许可；不表示上游参与或认可本地整合。
