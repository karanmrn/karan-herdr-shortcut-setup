---
name: openrouter
description: 'Work with OpenRouter API integrations or Karan’s local model launcher. Use when selecting or running models through the desktop proxy, or when changing application model routing, media, tools, cost, or reliability.'
---

# OpenRouter

## This desktop's terminal launcher

The user's macOS terminal has a local `cli-proxy-api` endpoint at
`http://127.0.0.1:8317`. The `openrouter` shell command reads model IDs from
that endpoint and starts a new Claude Code process with the selected model.
The `aim <model>` shell function starts the same kind of process without the
picker. These commands do not change the model in the current Codex session.

Use the launchers only when the user asks to start a terminal session or names
one as the intended execution path. For discovery, use `openrouter --list` or
`openrouter --refresh`. Do not assume that a model ID exists. Do not print,
copy, or inspect the key stored in the local secret file. Do not assume that a
model visible through the proxy uses an OpenRouter route unless the proxy
configuration or a request confirms it.

This local launcher is separate from application integrations described below.
For application work, inspect the real SDK and request path before changing
model routing.

## SDK-specific guidance

OpenRouter can be called through different SDKs. If the app uses TanStack AI, read `~/.agents/skills/tanstack-ai/SKILL.md` and its adapter configuration skill before writing adapter code. If the task migrates an existing Vercel AI SDK or raw HTTP path, also read `~/.agents/skills/tanstack-ai-migration/SKILL.md`. Keep this skill's model, routing, cost, privacy, and reliability checks in either SDK.

Make model behavior explicit. Preserve the user's quality, cost, privacy, and reliability requirements across every route and retry.

## Before changing configuration

1. Inspect the actual outgoing request, SDK version, existing configuration, and user preferences. Redact credentials and content. A setting in a UI or config file does not prove the SDK sends it.
2. Verify exact model IDs and live capabilities through the [models API](https://openrouter.ai/api/v1/models). Inspect the selected model's provider endpoints too. Check input/output modalities, context and output limits, supported parameters, reasoning options, prices, and provider availability for **both primary and fallback models**.
3. Choose and record an explicit reasoning setting for each reasoning model. Use the user's requested effort. If unspecified, choose a supported value for the task and state the choice; do not silently inherit a provider default or impose one effort on every model. Read [reasoning and output](references/reasoning-and-output.md) before setting these fields.
4. Set an output ceiling, total deadline, bounded retry policy, and cost limits appropriate to the workload. Reasoning uses output tokens too. A model's context window is not its maximum output length.
5. Read the relevant reference below. Consult current official docs for unfamiliar fields; do not invent model IDs, provider slugs, parameter support, or SDK syntax.

## Rules that prevent expensive mistakes

- Use the unified `reasoning` object. `reasoning.exclude: true` hides reasoning; it does **not** turn reasoning off or make it free. Mandatory reasoning models cannot be disabled.
- Check every fallback against the same required capabilities and privacy/cost constraints. A single `models` request shares configuration across candidates. If models need different efforts or budgets, implement bounded application-level attempts with separate configs.
- Separate provider failover from model fallback. `provider.order` is a preference; `only` restricts providers; `ignore` excludes them. Use `provider.require_parameters: true` when silently dropping requested parameters would break correctness. Recheck endpoint support; this is not a semantic guarantee.
- Match routing to the real goal: `provider.sort: "price"` for price, `"latency"` for TTFT, `"throughput"` for tokens/second. `:nitro` also permits priority tiers; `:floor` also permits flex tiers. They can change price or availability beyond plain sorting.
- HTTP 200 is not application success. Check errors, finish reason, expected output type, schema, and task-specific validity. Null text may be a valid tool call. A truncated or unreviewed answer must not become a successful artifact.
- Do not repeat a deterministic failure unchanged. On a confirmed output-limit failure, consider a supported lower effort, smaller task, or compatible fallback within the quality budget. Increasing the cap is one option, not the automatic answer. Preserve fail-closed validation on every attempt.
- Keep keys server-side. Log diagnostic metadata, not prompts, attachments, raw reasoning, or provider errors that may contain private content. Never weaken safety/privacy restrictions just to get a successful response.

## Read only what the task needs

- [Reasoning and output](references/reasoning-and-output.md): effort selection, token budgets, schemas, empty answers, adaptive retries, Python request example.
- [Routing, cost, and speed](references/routing-cost-speed.md): model fallbacks, provider filters, suffixes, tiers, performance thresholds, caching.
- [Images, other media, and tools](references/media-and-tools.md): image generation and aspect ratios, URL/base64 attachments, PDFs/audio/video, tool loops, reasoning preservation.
- [Reliability and observability](references/reliability.md): error handling, SSE, deadlines, billing, telemetry, privacy, deployment checks.
- [API field map and sources](references/api-field-map.md): endpoint selection, request parameter families, SDK passthrough, live schemas and authoritative sources.

## Verify the integration

Capture the serialized request in a redacted local test. Verify explicit reasoning, output limits, fallbacks, and routing constraints survive SDK serialization. Test the actual failure boundary: limit reached, null/tool output, malformed JSON, missing required capability, or mid-stream error. Run a small real smoke test when inference is authorized; do not describe mock validation as a production test.

For tuning, compare representative tasks using **valid-result rate, cost per valid result, time to first visible answer, and total duration**. Include retries and failed attempts. Lower effort or a faster route is acceptable only if required quality and safety still pass.

Report the chosen primary/fallback models, explicit effort and caps, routing goal, and what was verified. Distinguish confirmed API evidence from hypotheses.
