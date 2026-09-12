# API configuration for GPT-6 variants

Read this for API configuration advice. Resolve the exact requested variant through current official documentation. Verify its API identifier, endpoints, reasoning settings, output controls, and tool compatibility independently. Family names and Codex model-picker options do not establish API support. If a target such as a future GPT-6 Sol, Terra, or Luna lacks documentation, state what remains unverified and omit unsupported settings; do not substitute Astra's configuration.

Preserve an existing output schema exactly, including field types and nullability. Choose supported settings through evaluation against the user's quality, latency, and cost priorities. A request for quality does not establish that the highest effort is optimal. Keep configuration advice separate from the system prompt, and label illustrative configuration as unexecuted until tested.

## Astra reference

The remaining notes apply to GPT-6 Astra and were checked on 2026-09-12. Refresh the linked official pages before use. They are not defaults for other GPT-6 variants.

### Model and request compatibility

For Astra, use `model: "gpt-6-astra"`. Its [model reference](https://developers.openai.com/api/docs/models/gpt-6-astra) lists `low`, `medium`, `high`, `xhigh`, and `max` for `reasoning.effort`, and supports Structured Outputs.

Apply the [migration quickstart](https://developers.openai.com/api/docs/guides/latest-model#migration-quickstart):

- Tool use requires Responses. Chat Completions remains available for requests without tools.
- Map prior `none` or `minimal` effort to `low` for comparison; otherwise retain effective effort. Responses uses `reasoning.effort`; Chat Completions uses `reasoning_effort`.
- Remove `temperature`, `top_p`, and `top_logprobs`. Remove Chat Completions `logprobs`, or Responses `include` entry `message.output_text.logprobs`, as applicable.

### Conversation reasoning

The [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) documents `configuration_update` for standard, single-agent Astra requests. Keep request-level effort unchanged and insert an update before the next user message to preserve the cached prefix. The new effort persists until another update. Check the guide's current compatibility limits before combining this with other modes.

For tool continuations, preserve reasoning, tool call, and tool result items through `previous_response_id` or the documented history flow. Prompt wording cannot repair dropped conversation state. See [reasoning with function calls](https://developers.openai.com/api/docs/guides/reasoning#keeping-reasoning-items-in-context).

### Conditional checks

For deployments using Fast mode, review [Fast mode compatibility](https://developers.openai.com/api/docs/guides/fast-mode). For migrations from GPT-5.5 or earlier that use caching, review [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching). Consult the migration quickstart for the applicable parameter changes. Do not carry old settings forward solely because the prompt still works.
