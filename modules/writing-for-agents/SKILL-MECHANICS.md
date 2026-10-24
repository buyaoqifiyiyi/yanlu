# Skill mechanics for Codex

The skill-specific branch of [writing-for-agents](GUIDE.md): packaging and discovery for the current Codex host. Keep the document-writing principles in the parent skill.

## Invocation

Keep automatic selection enabled by default. A concise `description` states the task branches the skill handles. Explicit `$skill-name` invocation remains available. Preserve the existing policy unless the user asks to change it.

When the user explicitly requests a skill that is available only by explicit invocation, put this in `agents/openai.yaml`:

```yaml
policy:
  allow_implicit_invocation: false
```

Do not add `disable-model-invocation` to Codex frontmatter; that is another host's setting. Use the current host's skill-creator instructions and validator for supported fields. Invocation policy governs automatic selection, not whether an authorized agent can read a referenced file by path.

## Shared references and routers

Put shared reference material in one maintained file and link it from callers with a clear reading condition. It can live within a skill or outside the skill system; it does not need a separate discoverable skill just to be readable.

Split out a discoverable skill only when it has a distinct task trigger worth the permanent description cost. A router can list related workflows and their reading conditions when that makes a real group easier to use; it need not force-load every related skill.

For another host, verify its actual invocation mechanism instead of copying these Codex settings. Discovery, a model's routing choice, file reading, and successful business execution are separate checks.

Current mechanism: [official skill documentation](https://learn.chatgpt.com/docs/build-skills).
