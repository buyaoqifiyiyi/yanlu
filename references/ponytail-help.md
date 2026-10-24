# Yanlu功能与旧口令帮助

本功能组只提供Yanlu一个技能定义，旧Ponytail功能都在本包内。这里保留任务语义和档位，不承诺已移除技能ID仍存在于宿主选择器。

## 编码档位

| 请求 | 行为 |
|---|---|
| `$yanlu lite` 或文字ponytail lite | 完成要求，并简述适用的更小方案 |
| `$yanlu full` 或文字ponytail full | 最小完整实现，保留验证、必要调用方及错误处理；首次默认 |
| `$yanlu ultra` 或文字ponytail ultra | 质疑无依据扩展，仍完成明确责任 |
| `$yanlu off`、文字ponytail off、stop ponytail、normal mode | 关闭本会话编码精简；不会关闭其他明确请求的能力 |

档位持续到明确切换或会话结束。关闭后普通编码/审查/help/技能维护不恢复；明确启用编码模式或指定lite/full/ultra恢复。

## 全部原功能

| 当前用法 | 仍识别的文字口令 | 对应功能 |
|---|---|---|
| `$yanlu` 加编码任务 | ponytail加编码任务 | [最小完整实现](coding.md) |
| `$yanlu review` 加改动范围 | ponytail-review | [diff复杂度审查](complexity-review.md)，只读 |
| `$yanlu audit` 加仓库范围 | ponytail-audit | [全仓复杂度审计](complexity-audit.md)，只读 |
| `$yanlu debt` | ponytail-debt | [shortcut及旧ponytail延期标记](shortcut-debt.md) |
| `$yanlu gain` | ponytail-gain | [作者外部实验](external-benchmark.md)，非本机收益 |
| `$yanlu help` | ponytail-help | 本帮助，不改档位 |
| `$yanlu` 加技能维护任务 | 原Yanlu技能创建/更新请求 | [技能工作流](skill-workflow.md) |

代码复杂度审查与普通正确性/安全审查职责不同；发现其它重要问题可指出，不能默认扩大审查。已有写入授权仍有效，单纯只读任务不自行实施。本包只提供yanlu技能定义，界面以宿主重新扫描为准；旧`$ponytail`选择器句柄不再保留，使用`$yanlu`或将旧名直接写作文字请求。

来源、许可、快照、评估器、内容蒸馏与`shortcut:`/旧`ponytail:`标记支持都保留。没有导入原Ponytail插件hooks、band UI、配置加载器或自动捕获服务。

## 工程模式扩展

新增code-review、diagnose、tdd、architecture、domain、prototype、pr、research、workflow、wizard、grilling和Agent文档模式，根入口给出触发和按需读取路径。`yanlu review`仍为原复杂度审查；普通代码正确性/标准/需求审查用`yanlu code-review`或明确任务描述。所有已归档旧名仅作文字口令，不恢复独立宿主ID。
