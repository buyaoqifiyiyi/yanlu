# 离线版本工具

`scripts/skill_snapshot.py` 使用 Python 3.11+ 标准库。解释器命令可为宿主核实的 `python`、`python3` 或绝对路径；含空格路径按当前 shell 正确引用。

PowerShell 示例：

```powershell
python "C:\skills\yanlu\scripts\skill_snapshot.py" capture "D:\skills\target" "D:\task\work\round-01"
python "C:\skills\yanlu\scripts\skill_snapshot.py" verify "D:\task\work\round-01" --source
python "C:\skills\yanlu\scripts\skill_snapshot.py" diff "D:\task\work\round-01"
```

示例路径须替换为本任务实际路径；脚本不会寻找或安装技能。`RUN_DIR` 的父目录需要先建立，目标目录尚不存在且在源目录之外。

捕获前检查源文件清单：本工具不会过滤 `.env`、token 或个人材料。按入口的敏感资料分支确定复制范围和授权；未知范围时先做受限审阅，不把完整 capture 当作安全扫描。

## 输出及保证

- `capture SOURCE RUN_DIR`：读取含 `SKILL.md` 的源目录，复制 `baseline/` 和 `candidate/`，产生包含相对路径、目录与 SHA256 的 `manifest.json`。忽略 `.git`、`__pycache__` 目录，保留其他资源和空目录；源目录只读。
- `verify RUN_DIR`：核对基线的文件/目录集合与哈希。`--source` 同时核对当初的源目录是否仍一致。
- `diff RUN_DIR`：先验证基线，再输出候选相对基线的文件新增/修改/删除及前后哈希。目录变化由 verify 的基线检查覆盖；diff 不单列候选空目录变化。

标准输出为 JSON，`ok: true` 且退出码 0 表示该命令通过。`ok: false` 或非零退出表示失败；保留 `.incomplete` 的工作目录不能用于比较。复制失败后换新的目录重做，不自动清理残留证据。

拒绝已有工作目录、源内工作目录、链接/junction/reparse 和非普通文件。若合法目标使用链接，先明确实际目标及授权范围，再对明确的普通目录处理；不要自动跟随链接扩大范围。

## 多轮及限制

首轮对原技能 capture；接受候选后，下一轮对该候选 capture 到另一个全新的工作目录。每轮 manifest 独立，原始版本始终可追溯。快照不依赖 Git，也不会初始化仓库、提交或回滚。

SHA256 是变更检测，不是访问控制或数字签名；同时修改基线与 manifest 可以伪造一致。工具没有文件系统锁，不提供抵御并发恶意替换的事务保证。测试和交付前重跑 verify；它不保证候选质量，也不执行复制回正式目录。

离线自检：在本技能目录执行 `python -B tests/test_snapshot.py`，覆盖复制、原件不变、差异、篡改、不完整快照及链接拒绝；测试数据仅使用临时目录。它验证辅助工具，不验证优化效果。
