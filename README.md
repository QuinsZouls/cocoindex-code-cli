<p align="center">
  <img width="2310" height="558" alt="emoji (28)" src="https://github.com/user-attachments/assets/447d9c6b-0623-4464-ac0e-cd40b288679f" />
</p>

<h1 align="center">light weight CLI for semantic code search that just works</h1>


A super light-weight, effective CLI **(AST-based)** that understands and searches your codebase using semantic similarity. Built with [CocoIndex](https://github.com/cocoindex-io/cocoindex) — a Rust-based ultra performant data transformation engine. No blackbox.

- Instant token saving by 70%.
- **1 min setup** — install and run!

<div align="center">

[![GitHub](https://img.shields.io/github/stars/cocoindex-io/cocoindex?color=5B5BD6)](https://github.com/cocoindex-io/cocoindex)
[![Documentation](https://img.shields.io/badge/Documentation-394e79?logo=readthedocs&logoColor=00B9FF)](https://cocoindex.io/docs/getting_started/quickstart)
[![License](https://img.shields.io/badge/license-Apache%202.0-5B5BD6?logoColor=white)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://img.shields.io/pypi/v/cocoindex?color=5B5BD6)](https://pypi.org/project/cocoindex/)
[![PyPI Downloads](https://static.pepy.tech/badge/cocoindex/month)](https://pepy.tech/projects/cocoindex)
[![Discord](https://img.shields.io/discord/1314801574169673738?logo=discord&color=5B5BD6&logoColor=white)](https://discord.com/invite/zpA9S2DR7s)

🌟 Please help star [CocoIndex](https://github.com/cocoindex-io/cocoindex) if you like this project!
</div>

## Get Started

### Installation

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install the CLI directly from GitHub:

```bash
pip install git+https://github.com/QuinsZouls/cocoindex-code-cli.git
```

Or using `uv`:

```bash
uv pip install git+https://github.com/QuinsZouls/cocoindex-code-cli.git
```

## Usage

The CLI provides two commands: `index` and `search`.

### Build/Refresh the Index

Run the `index` command from the root of your codebase to build or refresh the index:

```bash
cocoindex-code index
```

This will scan your codebase, chunk the code, generate embeddings, and store everything in a local SQLite database under `.cocoindex_code/`. It will also print index statistics (number of chunks, files, and languages).

### Search the Codebase

Use the `search` command with a natural language query or code snippet:

```bash
cocoindex-code search "database connection handling"
```

#### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-l`, `--limit` | Maximum number of results (1-100) | `10` |
| `-o`, `--offset` | Number of results to skip (pagination) | `0` |
| `--no-refresh` | Skip index refresh before searching (faster for consecutive queries) | off |
| `--json` | Output results in JSON format | off |

#### Examples

```bash
# Basic search
cocoindex-code search "authentication logic"

# Limit results
cocoindex-code search "error handling" --limit 5

# Paginate results
cocoindex-code search "API endpoints" --limit 10 --offset 10

# Skip index refresh for faster consecutive queries
cocoindex-code search "user validation" --no-refresh

# Output as JSON (useful for piping to other tools)
cocoindex-code search "database query" --json

# Combine options
cocoindex-code search "config parsing" -l 5 --no-refresh --json
```

By default, `search` refreshes the index before querying to include recent changes. Use `--no-refresh` to skip this step for faster consecutive queries when the codebase hasn't changed.

Each result includes:

- **File path** — relative path to the matching file
- **Language** — detected programming language
- **Code content** — the matching code chunk
- **Line numbers** — start and end line numbers
- **Similarity score** — relevance score (0–1, higher is better)

## Features
- **Semantic Code Search**: Find relevant code using natural language queries when grep doesn't work well.
- **Ultra Performant to code changes**: ⚡ Built on top of ultra performant [Rust indexing engine](https://github.com/cocoindex-io/cocoindex). Only re-indexes changed files for fast updates.
- **Multi-Language Support**: Python, JavaScript/TypeScript, Rust, Go, Java, C/C++, C#, SQL, Shell
- **Embedded**: Portable and just works, no database setup required!
- **Flexible Embeddings**: By default, no API key required with local SentenceTransformers — totally free! You can customize 100+ cloud providers.


## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `COCOINDEX_CODE_ROOT_PATH` | Root path of the codebase | Auto-discovered (see below) |
| `COCOINDEX_CODE_EMBEDDING_MODEL` | Embedding model (see below) | `sbert/sentence-transformers/all-MiniLM-L6-v2` |


### Root Path Discovery

If `COCOINDEX_CODE_ROOT_PATH` is not set, the codebase root is discovered by:

1. Finding the nearest parent directory containing `.cocoindex_code/`
2. Finding the nearest parent directory containing `.git/`
3. Falling back to the current working directory

### Embedding model
By default this project uses a local SentenceTransformers model (`sentence-transformers/all-MiniLM-L6-v2`). No API key required and completely free!

Use a code-specific embedding model to achieve better semantic understanding. This project supports all models on Ollama and 100+ cloud providers.

Set `COCOINDEX_CODE_EMBEDDING_MODEL` to any [LiteLLM-supported model](https://docs.litellm.ai/docs/embedding/supported_embedding), along with the provider's API key:

<details>
<summary>Ollama (Local)</summary>

```bash
COCOINDEX_CODE_EMBEDDING_MODEL=ollama/nomic-embed-text cocoindex-code search "my query"
```

Set `OLLAMA_API_BASE` if your Ollama server is not at `http://localhost:11434`.

</details>

<details>
<summary>OpenAI</summary>

```bash
COCOINDEX_CODE_EMBEDDING_MODEL=text-embedding-3-small \
OPENAI_API_KEY=your-api-key \
cocoindex-code search "my query"
```

</details>

<details>
<summary>Azure OpenAI</summary>

```bash
COCOINDEX_CODE_EMBEDDING_MODEL=azure/your-deployment-name \
AZURE_API_KEY=your-api-key \
AZURE_API_BASE=https://your-resource.openai.azure.com \
AZURE_API_VERSION=2024-06-01 \
cocoindex-code search "my query"
```

</details>

<details>
<summary>Gemini</summary>

```bash
COCOINDEX_CODE_EMBEDDING_MODEL=gemini/text-embedding-004 \
GEMINI_API_KEY=your-api-key \
cocoindex-code search "my query"
```

</details>

<details>
<summary>Mistral</summary>

```bash
COCOINDEX_CODE_EMBEDDING_MODEL=mistral/mistral-embed \
MISTRAL_API_KEY=your-api-key \
cocoindex-code search "my query"
```

</details>

<details>
<summary>Voyage (Code-Optimized)</summary>

```bash
COCOINDEX_CODE_EMBEDDING_MODEL=voyage/voyage-code-3 \
VOYAGE_API_KEY=your-api-key \
cocoindex-code search "my query"
```

</details>

<details>
<summary>Cohere</summary>

```bash
COCOINDEX_CODE_EMBEDDING_MODEL=cohere/embed-english-v3.0 \
COHERE_API_KEY=your-api-key \
cocoindex-code search "my query"
```

</details>

<details>
<summary>AWS Bedrock</summary>

```bash
COCOINDEX_CODE_EMBEDDING_MODEL=bedrock/amazon.titan-embed-text-v2:0 \
AWS_ACCESS_KEY_ID=your-access-key \
AWS_SECRET_ACCESS_KEY=your-secret-key \
AWS_REGION_NAME=us-east-1 \
cocoindex-code search "my query"
```

</details>

<details>
<summary>Nebius</summary>

```bash
COCOINDEX_CODE_EMBEDDING_MODEL=nebius/BAAI/bge-en-icl \
NEBIUS_API_KEY=your-api-key \
cocoindex-code search "my query"
```

</details>

Any model supported by LiteLLM works — see the [full list of embedding providers](https://docs.litellm.ai/docs/embedding/supported_embedding).


## Supported Languages

| Language | Aliases | File Extensions |
|----------|---------|-----------------|
| c | | `.c` |
| cpp | c++ | `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp` |
| csharp | csharp, cs | `.cs` |
| css | | `.css`, `.scss` |
| dtd | | `.dtd` |
| fortran | f, f90, f95, f03 | `.f`, `.f90`, `.f95`, `.f03` |
| go | golang | `.go` |
| html | | `.html`, `.htm` |
| java | | `.java` |
| javascript | js | `.js` |
| json | | `.json` |
| kotlin | | `.kt`, `.kts` |
| markdown | md | `.md`, `.mdx` |
| pascal | pas, dpr, delphi | `.pas`, `.dpr` |
| php | | `.php` |
| python | | `.py` |
| r | | `.r` |
| ruby | | `.rb` |
| rust | rs | `.rs` |
| scala | | `.scala` |
| solidity | | `.sol` |
| sql | | `.sql` |
| swift | | `.swift` |
| toml | | `.toml` |
| tsx | | `.tsx` |
| typescript | ts | `.ts` |
| xml | | `.xml` |
| yaml | | `.yaml`, `.yml` |

Common generated directories are automatically excluded:

- `__pycache__/`
- `node_modules/`
- `target/`
- `dist/`
- `vendor/` (Go vendored dependencies, matched by domain-based child paths)

## Large codebase / Enterprise
[CocoIndex](https://github.com/cocoindex-io/cocoindex) is an ultra efficient indexing engine that also works on large codebases at scale for enterprises. In enterprise scenarios it is a lot more efficient to do index sharing with teammates when there are large repos or many repos. We also have advanced features like branch dedupe etc designed for enterprise users.

If you need help with remote setup, please email our maintainer linghua@cocoindex.io, happy to help!!

## License

Apache-2.0
