# AI agent compatibility

Brand Soul uses the portable Agent Skills layout: one `SKILL.md` entrypoint plus optional scripts, references, and assets. Its core methodology is model-independent.

## Native Agent Skills support

| Agent | Install or discovery path | Invocation |
|---|---|---|
| Codex | Clone or copy to `~/.codex/skills/brand-soul` | Ask for Brand Soul or invoke `$brand-soul` where supported |
| Claude Code | Clone or copy to `~/.claude/skills/brand-soul` or `.claude/skills/brand-soul` | Ask naturally or invoke `/brand-soul` |
| Gemini CLI | `gemini skills install https://github.com/CacaoWebStudio/brand-soul` | Ask naturally, then approve activation |
| Grok | Clone or copy to `~/.grok/skills/brand-soul` or `.grok/skills/brand-soul` | Ask naturally or invoke `/brand-soul` |

## Other agents

For agents that understand `AGENTS.md`, clone the repository into the working project and ask the agent to follow `AGENTS.md`. For any document-capable model, attach or expose the repository and instruct it to read `SKILL.md` first, then only the references routed for the requested mode.

Compatibility means the framework instructions and repository contract are portable. Tool permissions, filesystem access, automatic Skill discovery, and script execution still depend on the host agent.

## Design constraints

- Keep the technical name `brand-soul`.
- Keep standard Skill frontmatter portable.
- Avoid vendor-specific dynamic prompt syntax in `SKILL.md`.
- Keep Python scripts optional; the methodology remains usable without executing them.
- Treat `agents/openai.yaml` as optional Codex UI metadata, not a core dependency.

## Official implementation references

- [Claude Code Agent Skills](https://code.claude.com/docs/en/skills)
- [Gemini CLI Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/creating-skills.md)
- [Grok skills and AGENTS.md compatibility](https://docs.x.ai/build/features/skills-plugins-marketplaces)
