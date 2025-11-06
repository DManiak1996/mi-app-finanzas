---
name: ollama
description: Ollama local LLM management tool. Use for running local language models, model management, API integration, and offline AI inference.
---

# Ollama Skill

Comprehensive assistance with ollama development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Setting up or configuring Ollama locally or in the cloud
- Making API calls to generate text, chat, or embeddings
- Working with vision models or multimodal inputs
- Implementing streaming responses from language models
- Creating custom models or importing fine-tuned models
- Using tool calling or structured outputs with Ollama
- Implementing web search capabilities with Ollama
- Integrating Ollama with IDEs (VS Code, JetBrains, Xcode, etc.)
- Debugging Ollama API errors or model issues
- Setting up OpenAI-compatible endpoints with Ollama

## Quick Reference

### Basic Chat Generation

Generate a chat message using the API:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3",
  "prompt": "Why is the sky blue?"
}'
```

### Python Chat Example

```python
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)

chat_completion = client.chat.completions.create(
    messages=[
        {'role': 'user', 'content': 'Say this is a test'}
    ],
    model='llama3.2',
)
```

### CLI Usage

Run a model interactively:

```bash
ollama run gemma3
```

Pull a model:

```bash
ollama pull gemma3
```

Generate embeddings:

```bash
ollama run embeddinggemma "Hello world"
```

### Vision Model Example

Using a vision model to analyze images:

```bash
ollama run gemma3 "What's in this image? /Users/jmorgan/Desktop/smile.png"
```

### Streaming with Python

Enable streaming for real-time responses:

```python
from ollama import Client

client = Client()

for chunk in client.chat(
    model='gemma3',
    messages=[{'role': 'user', 'content': 'Tell me a story'}],
    stream=True
):
    print(chunk['message']['content'], end='')
```

### Creating Custom Models

Create a Modelfile:

```modelfile
FROM llama3.2:latest
SYSTEM You are Mario from Super Mario Bros, acting as an assistant.
```

Build the model:

```bash
ollama create mario-assistant -f ./Modelfile
```

### Structured Outputs with Python

```python
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

class FriendInfo(BaseModel):
    name: str
    age: int
    is_available: bool

class FriendList(BaseModel):
    friends: list[FriendInfo]

completion = client.beta.chat.completions.parse(
    temperature=0,
    model="llama3.1:8b",
    messages=[
        {"role": "user", "content": "I have two friends. Return a list in JSON format"}
    ],
    response_format=FriendList,
)
```

### Web Search Integration

```python
import requests

response = requests.post(
    'https://ollama.com/api/web_search',
    headers={'Authorization': f'Bearer {OLLAMA_API_KEY}'},
    json={'query': 'latest AI developments', 'max_results': 5}
)
```

### Authentication for Cloud Models

Sign in locally:

```bash
ollama signin
```

Use cloud models:

```bash
ollama run gpt-oss:120b-cloud
```

### Import GGUF Model

```modelfile
FROM ./my-model.gguf
```

Then create:

```bash
ollama create my-custom-model -f ./Modelfile
```

## Key Concepts

### Base URL
- **Local API**: `http://localhost:11434/api`
- **Cloud API**: `https://ollama.com/api`

### Model Types
- **Chat models**: For conversational AI (e.g., llama3.2, gemma3)
- **Vision models**: Accept images and text (e.g., llava)
- **Embedding models**: Generate vector embeddings (e.g., all-minilm, embeddinggemma)
- **Cloud models**: High-performance models (e.g., gpt-oss:120b-cloud)

### Streaming
- Enabled by default in REST API
- Disabled by default in SDKs
- Set `stream: true` parameter to enable
- Responses arrive as chunks in real-time

### Authentication
- **Local access**: No authentication required
- **Cloud access**: Sign in with `ollama signin` or use API keys
- **API keys**: Create at https://ollama.com/settings/keys

### Context Length
- Important for agents and web search
- Recommended: at least ~32,000 tokens
- Cloud models run at full context length

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Complete API reference including:
  - Streaming concepts and implementation
  - Web search and web fetch APIs
  - Vision model usage
  - Integration with Codex, Cline, Goose

- **customization.md** - Model customization including:
  - Modelfile instructions (FROM, PARAMETER, TEMPLATE, SYSTEM, ADAPTER, etc.)
  - Creating custom models
  - Fine-tuning and adapter support

- **getting_started.md** - Getting started guides:
  - Quickstart tutorial for CLI, Python, and JavaScript
  - Integration guides for Goose (Desktop and CLI)
  - API introduction and basic usage

- **models.md** - Model management:
  - Pulling, pushing, and deleting models
  - Listing and managing running models
  - CLI reference for all commands
  - Modelfile reference
  - Importing models (Safetensors, GGUF)
  - Quantization options
  - Sharing models on ollama.com

- **other.md** - Additional documentation including:
  - OpenAI API compatibility
  - Error handling and status codes
  - Authentication methods
  - Usage tracking
  - Platform-specific guides (Linux, macOS, Windows, Docker)

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with **getting_started.md** for:
- Installing Ollama
- Running your first model
- Basic CLI commands (`ollama run`, `ollama pull`)
- Simple API examples

Then explore **api.md** for:
- Making your first API call
- Understanding request/response formats
- Basic streaming implementation

### For Intermediate Users
Review **models.md** for:
- Creating custom models with Modelfiles
- Model management (list, copy, delete)
- Understanding different model types
- Importing community models

Check **api.md** for:
- Vision model implementation
- Tool calling and structured outputs
- Web search integration
- OpenAI compatibility layer

### For Advanced Users
Deep dive into **customization.md** for:
- Fine-tuning with adapters (Safetensors, GGUF)
- Custom templates and parameters
- Model quantization strategies
- Advanced Modelfile configurations

Explore **models.md** for:
- Importing fine-tuned models
- Publishing models to ollama.com
- Building from Safetensors weights
- Quantization levels and performance tuning

### For Integration Projects
Use **api.md** for:
- IDE integrations (VS Code, JetBrains, Xcode, Zed)
- MCP server setup for Cline, Codex, Goose
- OpenAI-compatible client configuration
- Multi-modal applications with vision

## Common Patterns

### Running Models Locally
1. Pull the model: `ollama pull <model-name>`
2. Run interactively: `ollama run <model-name>`
3. Or use the API for programmatic access

### Using Cloud Models
1. Sign in: `ollama signin`
2. Run cloud model: `ollama run gpt-oss:120b-cloud`
3. Or use API with authentication headers

### Creating Custom Models
1. Create a Modelfile with FROM, SYSTEM, and PARAMETER instructions
2. Build: `ollama create <model-name> -f ./Modelfile`
3. Test: `ollama run <model-name>`
4. Share: `ollama push <username>/<model-name>`

### Building Search Agents
1. Set up web search API with authentication
2. Use models with large context windows (32K+ tokens)
3. Implement tool calling for web_search and web_fetch
4. Handle streaming responses for real-time updates

## Error Handling

### Status Codes
- `200`: Success
- `400`: Bad Request (invalid parameters or JSON)
- `404`: Not Found (model doesn't exist)
- `429`: Rate limit exceeded
- `500`: Internal Server Error
- `502`: Bad Gateway (cloud model unreachable)

### Error Response Format
```json
{
  "error": "the model failed to generate a response"
}
```

### Streaming Errors
Errors during streaming appear as JSON objects with an `error` property in the stream.

## Resources

### Official Links
- Documentation: https://docs.ollama.com
- GitHub: https://github.com/ollama/ollama
- Model Library: https://ollama.com/library
- Python Library: https://github.com/ollama/ollama-python
- JavaScript Library: https://github.com/ollama/ollama-js

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- OpenAI API compatibility allows easy integration with existing applications
- Local API requires no authentication; cloud API requires sign-in or API keys
- Most models work best with increased context length for complex tasks

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
