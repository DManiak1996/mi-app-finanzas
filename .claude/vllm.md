---
name: vllm
description: vLLM high-performance LLM inference engine from GitHub README and docs
---

# vllm

vLLM high-performance LLM inference engine - fast, memory-efficient inference and serving for Large Language Models

## Description

A high-throughput and memory-efficient inference and serving engine for LLMs, originally developed at UC Berkeley's Sky Computing Lab. vLLM provides state-of-the-art serving throughput with efficient attention key-value memory management using PagedAttention, continuous batching, and optimized CUDA kernels.

**Repository:** [vllm-project/vllm](https://github.com/vllm-project/vllm)
**Language:** Python (86.2%), CUDA (8.0%), C++ (4.1%)
**Stars:** 62,275
**License:** Apache License 2.0
**Homepage:** https://docs.vllm.ai

## When to Use This Skill

Use this skill when you need to:

### Core Use Cases
- **Deploy LLM inference servers** with OpenAI-compatible API endpoints
- **Optimize LLM serving throughput** and reduce memory usage for production deployments
- **Implement offline batch inference** for processing multiple prompts efficiently
- **Set up distributed inference** using tensor, pipeline, data, or expert parallelism
- **Use quantization** (GPTQ, AWQ, INT4, INT8, FP8) to reduce model size and speed up inference
- **Enable speculative decoding** to accelerate generation speed
- **Serve multimodal models** (vision-language models like LLaVA, audio models)
- **Configure LoRA adapters** for serving multiple fine-tuned variants

### Specific Scenarios
- Setting up **prefix caching** to accelerate repeated prompt prefixes
- Implementing **structured outputs** (JSON, regex-constrained generation)
- Deploying models on **NVIDIA GPUs, AMD GPUs, Intel GPUs, or TPUs**
- Configuring **disaggregated serving** (separate prefill and decode clusters)
- Understanding **PagedAttention**, **continuous batching**, or **CUDA graphs**
- Troubleshooting **model loading**, **quantization errors**, or **distributed issues**
- Checking **supported models**, **recent releases**, or **known issues**

### When NOT to Use This Skill
- Training or fine-tuning models (use frameworks like PyTorch, HuggingFace Transformers instead)
- Text generation with minimal requirements (consider using HuggingFace directly)
- Non-LLM deep learning tasks

## Quick Reference

### 1. Basic Installation

```bash
# Install from PyPI
pip install vllm

# For ROCm (AMD GPUs)
pip install vllm --extra-index-url https://download.pytorch.org/whl/rocm

# For TPU
pip install vllm[tpu]

# From source (for latest features)
pip install git+https://github.com/vllm-project/vllm.git
```

### 2. Offline Inference - Basic Usage

```python
from vllm import LLM, SamplingParams

# Initialize the model
llm = LLM(model="facebook/opt-125m")

# Define prompts and sampling parameters
prompts = [
    "Hello, my name is",
    "The president of the United States is",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

# Generate outputs
outputs = llm.generate(prompts, sampling_params)

# Print results
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated: {generated_text!r}")
```

### 3. OpenAI-Compatible API Server

```bash
# Start the server (basic)
python -m vllm.entrypoints.openai.api_server \
    --model facebook/opt-125m

# With specific GPU and port
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3-8B-Instruct \
    --port 8000 \
    --gpu-memory-utilization 0.9

# Query the server
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "facebook/opt-125m",
        "prompt": "San Francisco is a",
        "max_tokens": 50,
        "temperature": 0
    }'
```

### 4. Distributed Inference (Tensor Parallelism)

```python
from vllm import LLM

# Tensor parallel across 4 GPUs
llm = LLM(
    model="meta-llama/Llama-3-70B-Instruct",
    tensor_parallel_size=4,
    gpu_memory_utilization=0.9
)

outputs = llm.generate("Write a poem about AI")
```

### 5. Quantization (GPTQ/AWQ/FP8)

```python
from vllm import LLM, SamplingParams

# Load AWQ-quantized model (4-bit)
llm = LLM(
    model="TheBloke/Llama-2-13B-chat-AWQ",
    quantization="awq",
    dtype="half"
)

# Load GPTQ-quantized model
llm = LLM(
    model="TheBloke/Llama-2-13B-chat-GPTQ",
    quantization="gptq"
)

# Enable FP8 quantization
llm = LLM(
    model="meta-llama/Llama-3-70B",
    quantization="fp8"
)
```

### 6. Vision-Language Model (Multimodal)

```python
from vllm import LLM, SamplingParams

# Initialize vision-language model
llm = LLM(model="llava-hf/llava-1.5-7b-hf")

# Single image
outputs = llm.generate({
    "prompt": "What is shown in this image?",
    "multi_modal_data": {
        "image": "https://example.com/image.jpg"
    }
})

# Multiple images
outputs = llm.generate({
    "prompt": "Describe the differences between these images",
    "multi_modal_data": {
        "image": [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg"
        ]
    }
})
```

### 7. Prefix Caching (Automatic)

```python
from vllm import LLM, SamplingParams

# Enable automatic prefix caching
llm = LLM(
    model="meta-llama/Llama-3-8B-Instruct",
    enable_prefix_caching=True
)

# Shared prefix will be cached automatically
prompts = [
    "You are a helpful assistant. User: What is the capital of France?",
    "You are a helpful assistant. User: What is the capital of Germany?",
    "You are a helpful assistant. User: What is the capital of Italy?",
]

outputs = llm.generate(prompts, SamplingParams(temperature=0))
```

### 8. Structured Outputs (JSON Mode)

```python
from vllm import LLM, SamplingParams
import json

llm = LLM(model="meta-llama/Llama-3-8B-Instruct")

# Define JSON schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "city": {"type": "string"}
    },
    "required": ["name", "age", "city"]
}

# Generate with structured output
sampling_params = SamplingParams(
    temperature=0.7,
    guided_decoding_backend="outlines",
    guided_json=schema
)

outputs = llm.generate(
    "Generate a person profile",
    sampling_params
)

result = json.loads(outputs[0].outputs[0].text)
print(result)  # {"name": "John", "age": 30, "city": "NYC"}
```

### 9. LoRA Adapters (Multi-LoRA Serving)

```python
from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest

# Initialize base model
llm = LLM(
    model="meta-llama/Llama-3-8B",
    enable_lora=True,
    max_lora_rank=64
)

# Serve multiple LoRA adapters
lora1 = LoRARequest("sql_adapter", 1, "/path/to/sql_lora")
lora2 = LoRARequest("math_adapter", 2, "/path/to/math_lora")

# Generate with specific adapters
outputs1 = llm.generate("Write a SQL query", lora_request=lora1)
outputs2 = llm.generate("Solve this equation", lora_request=lora2)
```

### 10. Speculative Decoding

```python
from vllm import LLM, SamplingParams

# Target model + draft model for speculative decoding
llm = LLM(
    model="meta-llama/Llama-3-70B-Instruct",
    speculative_model="meta-llama/Llama-3-8B-Instruct",
    num_speculative_tokens=5,
    tensor_parallel_size=4
)

# Generates faster with speculative decoding
outputs = llm.generate("Write a story", SamplingParams(max_tokens=512))
```

## Key Concepts

### PagedAttention
vLLM's core innovation that manages attention key-value memory using non-contiguous paging (similar to OS virtual memory). This allows:
- **Near-zero waste** in KV cache memory
- **Flexible sharing** of KV cache across sequences (prefix sharing)
- **Dynamic allocation** as sequences grow

Traditional systems allocate fixed KV cache blocks, wasting memory. PagedAttention allocates memory in pages on-demand.

### Continuous Batching
Unlike static batching (waiting for all sequences to finish), vLLM uses **continuous batching** (also called "iteration-level scheduling"):
- New requests added immediately when slots become available
- Higher throughput and GPU utilization
- Lower latency for individual requests

### CUDA Graphs
vLLM uses CUDA graphs to reduce kernel launch overhead:
- **PIECEWISE mode**: Graph per batch size
- **FULL_AND_PIECEWISE mode**: Single full graph + fallback graphs (default in v0.11.0+)
- Significantly faster for small batch sizes

### V1 Engine (Current Default)
As of v0.11.0, vLLM uses the **V1 engine exclusively** (V0 engine removed):
- Cleaner architecture
- 1.7x speedup on average
- Zero-overhead prefix caching
- Enhanced multimodal support
- Better async scheduling

### Quantization Methods

| Method | Bits | Speed | Quality | Use Case |
|--------|------|-------|---------|----------|
| **FP8** | 8-bit | Fastest | High | Large models, Hopper GPUs |
| **AWQ** | 4-bit | Very Fast | High | General purpose |
| **GPTQ** | 4-bit | Very Fast | High | General purpose |
| **INT8** | 8-bit | Fast | Good | Compatibility |
| **INT4** | 4-bit | Fastest | Lower | Maximum compression |

### Parallelism Strategies

- **Tensor Parallelism (TP)**: Split model layers across GPUs (low latency, high bandwidth)
- **Pipeline Parallelism (PP)**: Split model stages across GPUs (larger models)
- **Data Parallelism (DP)**: Replicate model across GPUs (higher throughput)
- **Expert Parallelism (EP)**: For Mixture-of-Experts models (e.g., Mixtral, DeepSeek)

### Supported Hardware

- **NVIDIA GPUs**: Full support (CUDA, Hopper, Blackwell)
- **AMD GPUs**: ROCm support
- **Intel GPUs**: XPU support
- **Google TPU**: TPU support
- **CPUs**: Intel/AMD/ARM CPUs (AVX2/AVX512/NEON optimizations)

## Available Reference Files

The `references/` directory contains comprehensive documentation organized by topic:

### Core Documentation
- **`references/README.md`** - Complete README with project overview, features, installation, getting started, sponsors, and contact information
- **`references/file_structure.md`** - Full repository structure (3,643 items) showing all source files, tests, benchmarks, and documentation

### Release Information
- **`references/releases.md`** - Detailed release notes for v0.11.0 and previous versions, including:
  - Model support updates (DeepSeek-V3.2, Qwen3-VL, OLMo3, etc.)
  - Engine improvements (KV cache offloading, hybrid allocator, FlashInfer optimizations)
  - Hardware support (RISC-V, ARM, ROCm 7.0)
  - Quantization features (FP8, FP4, W4A8)
  - API enhancements (reasoning streaming, tool calling)
  - V0 deprecation timeline

### Navigation Tips
- Start with **README.md** for high-level overview and installation
- Check **releases.md** for version-specific features and breaking changes
- Use **file_structure.md** to locate specific source files or tests

## Working with This Skill

### For Beginners

**Start Here:**
1. Read the installation examples in Quick Reference section
2. Try the "Offline Inference - Basic Usage" example (simplest)
3. Explore the OpenAI-compatible API server setup
4. Check `references/README.md` for official documentation links

**Common First Steps:**
```bash
# Install vLLM
pip install vllm

# Run a simple model
python -c "from vllm import LLM; llm = LLM('facebook/opt-125m'); print(llm.generate('Hello'))"

# Start API server
python -m vllm.entrypoints.openai.api_server --model facebook/opt-125m
```

### For Intermediate Users

**Key Areas to Explore:**
1. **Quantization**: Reduce model size with AWQ/GPTQ/FP8 (see Quick Reference #5)
2. **Distributed Inference**: Use tensor parallelism for larger models (Quick Reference #4)
3. **Prefix Caching**: Speed up repetitive prompts (Quick Reference #7)
4. **Structured Outputs**: Constrain generation to JSON schemas (Quick Reference #8)

**Optimization Checklist:**
- [ ] Set `--gpu-memory-utilization 0.9` for better throughput
- [ ] Enable `--enable-prefix-caching` for repeated prompts
- [ ] Use `--tensor-parallel-size N` for large models
- [ ] Consider quantization for memory-constrained environments
- [ ] Enable CUDA graphs (default) for faster inference

### For Advanced Users

**Advanced Topics:**
1. **Disaggregated Serving**: Separate prefill and decode clusters for scale
2. **Expert Parallelism**: Optimize MoE models (Mixtral, DeepSeek-V3)
3. **Custom Kernels**: Understand FlashAttention, FlashInfer, and custom CUDA kernels
4. **Multi-LoRA**: Serve multiple fine-tuned variants simultaneously (Quick Reference #9)
5. **Speculative Decoding**: Use draft models for faster generation (Quick Reference #10)

**Performance Tuning:**
- Review `references/releases.md` for hardware-specific optimizations
- Check CUDA graph modes (FULL_AND_PIECEWISE vs PIECEWISE)
- Optimize for specific hardware (DeepGEMM for Hopper GPUs, FlashInfer for MLA)
- Use NCCL symmetric memory for distributed setups
- Enable async scheduling with uniprocessor executor

**Troubleshooting:**
- Check GitHub issues: 3,144 open (as of 2025-11-06)
- Join Slack: https://slack.vllm.ai
- Forum: https://discuss.vllm.ai

## Common Use Patterns

### Pattern: Production API Server with Monitoring

```bash
# Start vLLM server with production settings
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3-8B-Instruct \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.95 \
    --enable-prefix-caching \
    --max-model-len 4096 \
    --trust-remote-code
```

### Pattern: Batch Processing with Offline Inference

```python
from vllm import LLM, SamplingParams

# Process large batch efficiently
llm = LLM(model="meta-llama/Llama-3-8B-Instruct", max_model_len=2048)

# Load 10,000 prompts
prompts = load_prompts_from_file("prompts.txt")

# Process in one shot with continuous batching
sampling_params = SamplingParams(temperature=0.7, max_tokens=256)
outputs = llm.generate(prompts, sampling_params)

# Save results
save_outputs(outputs, "results.jsonl")
```

### Pattern: Model Comparison with Same Prefix

```python
from vllm import LLM, SamplingParams

# Enable prefix caching
llm = LLM(model="meta-llama/Llama-3-8B", enable_prefix_caching=True)

# Shared system prompt
system_prompt = "You are a helpful AI assistant. Always be concise and accurate.\n\n"

# Multiple user queries with shared prefix
queries = [
    system_prompt + "What is quantum computing?",
    system_prompt + "Explain neural networks.",
    system_prompt + "What is machine learning?",
]

# Prefix cached automatically - much faster!
outputs = llm.generate(queries, SamplingParams(temperature=0.7))
```

## Recent Updates (v0.11.0 - October 2025)

### Major Changes
- **V1 Engine Only**: V0 engine completely removed, V1 is now the sole engine
- **CUDA Graph Default**: `FULL_AND_PIECEWISE` mode now default (better performance)
- **New Models**: DeepSeek-V3.2-Exp, Qwen3-VL, OLMo3, LongCat-Flash, Ling2.0
- **KV Cache Offloading**: CPU offloading with LRU management for larger contexts
- **Performance**: FlashInfer RoPE 2x speedup, fused Q/K RoPE 11% improvement
- **Quantization**: FP8 per-token-group quantization, NVFP4 for dense models

### Breaking Changes
- V0 APIs removed (AsyncLLMEngine, LLMEngine, MQLLMEngine)
- `--async-scheduling` has bugs in v0.11.0 (fixed in next version)
- C++17 now required for building from source
- PyTorch 2.8 required for CPU deployments

### Deprecation Notices
- TPU: `xm.mark_step` deprecated in favor of `torch_xla.sync`

## Community Resources

- **Documentation**: https://docs.vllm.ai
- **Blog**: https://blog.vllm.ai
- **Paper**: https://arxiv.org/abs/2309.06180 (SOSP 2023)
- **Twitter/X**: https://x.com/vllm_project
- **User Forum**: https://discuss.vllm.ai
- **Developer Slack**: https://slack.vllm.ai
- **GitHub Issues**: https://github.com/vllm-project/vllm/issues

## Citation

If you use vLLM for research, cite:

```bibtex
@inproceedings{kwon2023efficient,
  title={Efficient Memory Management for Large Language Model Serving with PagedAttention},
  author={Woosuk Kwon and Zhuohan Li and Siyuan Zhuang and Ying Sheng and Lianmin Zheng and Cody Hao Yu and Joseph E. Gonzalez and Hao Zhang and Ion Stoica},
  booktitle={Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles},
  year={2023}
}
```

---

**Generated by Skill Seeker** | GitHub Repository Scraper
**Last Updated**: 2025-11-06 | **Version**: v0.11.0
