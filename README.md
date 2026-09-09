<div align="center">

<img src="assets/freemodels-proxy-logo.png" alt="FreeModels Proxy" width="150" />

# FreeModels Proxy

**A local OpenAI-compatible bridge between FreeModels Chat and Cherry Studio — with streaming and MCP/tool-call support.**

Run the proxy on Windows, point Cherry Studio at one local Base URL, and use the proxy as the compatibility layer between your client and the FreeModels upstream service.

[![Release](https://img.shields.io/github/v/release/rkfcode/FreeModels-Proxy?display_name=tag&sort=semver)](https://github.com/rkfcode/FreeModels-Proxy/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/rkfcode/FreeModels-Proxy/total)](https://github.com/rkfcode/FreeModels-Proxy/releases)
[![License: MIT](https://img.shields.io/github/license/rkfcode/FreeModels-Proxy)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Platform](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6?logo=windows&logoColor=white)](#requirements)

**English** · [فارسی](README.fa.md)

> ### ⭐ The main advantage
> **Use Claude Sonnet 5 through FreeModels Proxy for free, with the service's available high-speed access, and connect it to your favorite AI coding/agent clients through a local OpenAI-compatible API.**
>
> The same local endpoint can be used as a bridge for **Cherry Studio, Claude Code, OpenCode, Codex, Jan, and other OpenAI-compatible clients and agent environments**.
>
> **Important:** availability, speed, model access and usage limits are controlled by the upstream FreeModels service and can change at any time. FreeModels Proxy itself does not remove or guarantee upstream limits.


### [⬇️ Download FreeModels Proxy](https://github.com/rkfcode/FreeModels-Proxy/releases/latest)

**Standalone Windows executable. No Python, pip, PowerShell, or manual dependency installation is required for the release build.**

</div>

---

## Table of contents

- [Why it exists](#why-it-exists)
- [Features](#features)
- [Download](#download)
- [Install](#install)
- [Quick start](#quick-start)
- [Cherry Studio](#cherry-studio)
- [API](#api)
- [MCP and tool calls](#mcp-and-tool-calls)
- [Configuration](#configuration)
- [Testing](#testing)
- [Privacy and security](#privacy-and-security)
- [Requirements](#requirements)
- [Build from source](#build-from-source)
- [Project structure](#project-structure)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Author & support](#author--support)

---

## Why it exists

Cherry Studio is designed to work with OpenAI-compatible APIs, while FreeModels Chat exposes its own upstream service.

FreeModels Proxy sits between them:

```text
Cherry Studio
     │
     │ OpenAI-compatible API
     ▼
┌─────────────────────────┐
│    FreeModels Proxy     │
│       127.0.0.1:8000    │
│                         │
│  • API compatibility    │
│  • streaming            │
│  • tool/MCP bridging    │
│  • request normalization│
└────────────┬────────────┘
             │
             ▼
     FreeModels Chat
```

The goal is simple: **keep Cherry Studio as the client and agent environment, while using FreeModels Proxy as the local compatibility layer.**

---

## Features

| | |
|---|---|
| 🪟 **Windows desktop launcher** | A dedicated graphical launcher for starting, stopping, restarting and monitoring the proxy. |
| 🚀 **Automatic startup** | The launcher can start the proxy automatically when the application opens. |
| 🔌 **OpenAI-compatible API** | Exposes the local API in the format expected by OpenAI-compatible clients. |
| 🤖 **Cherry Studio ready** | Use `http://127.0.0.1:8000/v1` as the Base URL in Cherry Studio. |
| ⭐ **Claude Sonnet 5 access** | Designed to make the available FreeModels Claude Sonnet 5 access usable from OpenAI-compatible clients and agent workflows. |
| 🆓 **Free upstream access** | The proxy is intended to use the free access provided by FreeModels; the proxy itself does not charge for API requests. |
| ⚡ **High-speed upstream access** | Requests are streamed through the local proxy, while actual upstream speed depends on the FreeModels service and network conditions. |
| 🧩 **Works with agent ecosystems** | Use the local OpenAI-compatible endpoint with Cherry Studio, Claude Code, OpenCode, Codex, Jan and other compatible tools. |
| 🌊 **Streaming responses** | Supports Server-Sent Events for streamed chat responses. |
| 🧰 **MCP / tool-call bridge** | Reads tool definitions from Cherry Studio and converts model-side tool-call formats back into OpenAI-style `tool_calls`. |
| 🔄 **Tool-call history handling** | Preserves assistant tool calls and tool results so agent workflows can continue across turns. |
| 🧠 **Model routing** | Requests are forwarded using the selected model ID exposed by the proxy. |
| 📋 **One-click Base URL copy** | Copy the Cherry Studio Base URL directly from the launcher. |
| 🧪 **Built-in test / docs access** | Quickly open the API documentation and test the local service. |
| 📊 **Runtime information** | Shows host, port, runtime state and connection information in the launcher. |
| 📝 **Live logs** | Displays useful proxy activity and request information while the service is running. |
| 🌐 **Configurable host and port** | Change the listening host and port without editing the source code. |
| 🌍 **English / Persian UI** | The launcher includes English and Persian interface modes. |
| 📦 **Standalone EXE** | Release builds are packaged as a Windows executable with PyInstaller. |
| 🎨 **Modern launcher UI** | Dark, polished interface with FreeModels Proxy branding. |
| 🔒 **Local-first listener** | The default listener is `127.0.0.1:8000`, keeping the API local unless you explicitly change the host. |

---

## Download

### Recommended — Windows release

Download the latest release:

**[⬇️ FreeModels Proxy — Latest Release](https://github.com/rkfcode/FreeModels-Proxy/releases/latest)**

For normal users, download:

```text
FreeModels Proxy.exe
```

Run the executable directly.

The release build is self-contained from the user's perspective: **Python and project dependencies do not need to be installed manually.**

### Source version

Developers can clone the repository and run the source version with Python and the dependencies listed in `requirements.txt`.

---

## Install

### Release build

1. Open the [latest GitHub Release](https://github.com/rkfcode/FreeModels-Proxy/releases/latest).
2. Download `FreeModels Proxy.exe`.
3. Run it.
4. The launcher starts the local proxy automatically.
5. Copy the displayed Base URL into Cherry Studio.

Default Base URL:

```text
http://127.0.0.1:8000/v1
```

### Important

The standalone EXE is the recommended option for end users.

The source workflow is intended for developers who want to inspect or modify the project.

---

## Quick start

Once the launcher is open:

1. Make sure the proxy status is **Running**.
2. Confirm the host is `127.0.0.1` and the port is `8000`.
3. Copy the Base URL:

```text
http://127.0.0.1:8000/v1
```

4. Open Cherry Studio.
5. Create or edit an OpenAI-compatible provider.
6. Set **Base URL** to `http://127.0.0.1:8000/v1` and **API Key** to `rkfcode` (or `free`).
7. Select a model exposed by the proxy.
8. Send a test message.

You can also open the API documentation from the launcher:

```text
http://127.0.0.1:8000/docs
```

---

## AI clients and agent environments

FreeModels Proxy is not limited to Cherry Studio.

Because it exposes an **OpenAI-compatible local API**, it can be used as a local bridge for compatible AI clients, coding assistants and agent environments.

### Examples

| Client / environment | Typical role |
|---|---|
| **Cherry Studio** | Chat, Agent and MCP workflows |
| **Claude Code** | AI coding / terminal agent |
| **OpenCode** | Open-source coding agent |
| **Codex** | AI coding agent / CLI |
| **Jan** | Local AI client with OpenAI-compatible connections |
| **Other compatible clients** | Any application that can target an OpenAI-compatible Base URL |

The common idea is:

```text
AI Client / Agent
       │
       │ OpenAI-compatible API
       ▼
http://127.0.0.1:8000/v1
       │
       ▼
FreeModels Proxy
       │
       ▼
FreeModels upstream
```

This means you do not need a separate custom integration for every supported client when that client already understands OpenAI-compatible APIs.

### About "free and unlimited"

The project is designed around the **free access made available by the FreeModels upstream service**. If that service currently provides Claude Sonnet 5 without a paid API key or a practical request limit, the proxy can make that access available to compatible clients through the local API.

However, **FreeModels Proxy cannot guarantee unlimited usage, permanent free access, a specific speed, or uninterrupted availability**. Those properties are determined by the upstream service, its policies, capacity and network conditions.

## Cherry Studio

Use the following configuration as the starting point:

| Setting | Value |
|---|---|
| Provider type | OpenAI-compatible |
| Base URL | `http://127.0.0.1:8000/v1` |
| API key | `rkfcode` or `free` |
| Model | Select one of the models exposed by `/v1/models` |

### Recommended connection settings

Use these values when a client asks for an OpenAI-compatible provider:

```text
Base URL: http://127.0.0.1:8000/v1
API Key:  rkfcode
```

If the client does not accept `rkfcode`, use:

```text
API Key: free
```

The API key here is used as the client-side credential value expected by the compatible client/proxy setup; it is not an OpenAI billing key.

The important part is the **Base URL**. OpenAI-compatible clients normally expect the API root, while the client adds operation paths such as `/chat/completions` itself. citeturn0search1turn0search7

### Why `/v1`?

The proxy exposes its primary chat endpoint under the OpenAI-compatible path:

```text
POST /v1/chat/completions
```

So Cherry Studio should use:

```text
http://127.0.0.1:8000/v1
```

as its Base URL rather than adding `/chat/completions` manually.

---

## API

### List models

```http
GET /v1/models
```

### Get a single model

```http
GET /v1/models/{model_id}
```

### Chat completions

```http
POST /v1/chat/completions
```

The endpoint supports streamed responses using Server-Sent Events.

### Compatibility alias

```http
POST /chat/completions
```

This route is provided as a compatibility alias for clients that do not include `/v1`.

### Interactive API documentation

FastAPI documentation is available locally at:

```text
http://127.0.0.1:8000/docs
```

---

## MCP and tool calls

One of the main reasons this proxy exists is to keep Cherry Studio's agent/tool workflow usable instead of reducing the interaction to plain text chat.

The proxy can:

1. Receive tool definitions from Cherry Studio.
2. Map MCP-style tool names to the names expected by the upstream model format.
3. Convert the model's textual tool-call representations back into OpenAI-compatible `tool_calls`.
4. Preserve assistant tool-call messages and tool results for subsequent turns.
5. Stream the resulting response back to Cherry Studio.

In other words:

```text
Cherry Studio
    │
    │ tools + messages
    ▼
FreeModels Proxy
    │
    ├── normalize messages
    ├── map MCP tool names
    ├── send model-readable tool format
    ├── parse returned tool calls
    └── restore OpenAI tool_calls
    │
    ▼
Cherry Studio Agent
    │
    └── executes the actual MCP tool
```

**Cherry Studio remains the tool executor.** The proxy acts as the compatibility/translation layer between the client and the upstream model service.

---

## Configuration

### Default listener

```text
Host: 127.0.0.1
Port: 8000
Base URL: http://127.0.0.1:8000/v1
```

The source application also supports environment variables for the direct Python start mode:

```text
FREEMODELS_HOST
FREEMODELS_PORT
```

Example:

```powershell
$env:FREEMODELS_HOST="127.0.0.1"
$env:FREEMODELS_PORT="8001"
python main.py
```

### Launcher configuration

The Windows launcher lets you manage:

- Host
- Port
- Start / Stop
- Restart
- Automatic startup
- Base URL
- API docs / test access
- Language
- Live runtime information
- Live logs

---

## Testing

### Browser check

After starting the proxy, open:

```text
http://127.0.0.1:8000/docs
```

If FastAPI documentation loads, the local server is running.

### Models check

Open:

```text
http://127.0.0.1:8000/v1/models
```

You should receive an OpenAI-style model list.

### AI clients and agent environments

FreeModels Proxy is not limited to Cherry Studio.

Because it exposes an **OpenAI-compatible local API**, it can be used as a local bridge for compatible AI clients, coding assistants and agent environments.

### Examples

| Client / environment | Typical role |
|---|---|
| **Cherry Studio** | Chat, Agent and MCP workflows |
| **Claude Code** | AI coding / terminal agent |
| **OpenCode** | Open-source coding agent |
| **Codex** | AI coding agent / CLI |
| **Jan** | Local AI client with OpenAI-compatible connections |
| **Other compatible clients** | Any application that can target an OpenAI-compatible Base URL |

The common idea is:

```text
AI Client / Agent
       │
       │ OpenAI-compatible API
       ▼
http://127.0.0.1:8000/v1
       │
       ▼
FreeModels Proxy
       │
       ▼
FreeModels upstream
```

This means you do not need a separate custom integration for every supported client when that client already understands OpenAI-compatible APIs.

### About "free and unlimited"

The project is designed around the **free access made available by the FreeModels upstream service**. If that service currently provides Claude Sonnet 5 without a paid API key or a practical request limit, the proxy can make that access available to compatible clients through the local API.

However, **FreeModels Proxy cannot guarantee unlimited usage, permanent free access, a specific speed, or uninterrupted availability**. Those properties are determined by the upstream service, its policies, capacity and network conditions.

## Cherry Studio check

Configure:

```text
http://127.0.0.1:8000/v1
```

Then send a short test message.

### Tool / MCP check

For an agent test, use a Cherry Studio workflow that exposes at least one MCP tool. The proxy should receive the tool definitions, return model tool calls in OpenAI-compatible form, and allow Cherry Studio to continue the tool execution loop.

---

## Privacy and security

FreeModels Proxy is designed around a **local-first architecture**.

- The local API listens on `127.0.0.1` by default.
- Requests from Cherry Studio first reach the local proxy.
- The proxy forwards the required request data to the configured/embedded FreeModels upstream service.
- The proxy does not require a separate local database or account system.
- Changing the host from `127.0.0.1` can expose the API to other machines, so do this only when you understand the network implications.

### Important

This project is a compatibility proxy, not a security boundary.

If you expose the listener beyond localhost, add the appropriate network controls before using it on an untrusted network.

---

## Requirements

### For end users

**Windows 10 or Windows 11** is the target platform for the packaged desktop application.

For the standalone release:

- Python is not required.
- pip is not required.
- PowerShell is not required.
- FastAPI/httpx/uvicorn do not need to be installed manually.

### For source development

You need:

- Windows
- Python 3.x
- pip
- The packages listed in `requirements.txt`

---

## Build from source

Clone the repository:

```powershell
git clone https://github.com/rkfcode/FreeModels-Proxy.git
cd FreeModels-Proxy
```

Create and use the isolated source environment:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the launcher:

```powershell
.venv\Scripts\pythonw.exe launcher.py
```

### Build the Windows EXE

The repository includes:

```text
build_windows.bat
```

Run:

```powershell
.\build_windows.bat
```

The release executable is produced at:

```text
dist\FreeModels Proxy.exe
```

The build uses PyInstaller and includes the application assets and required Python packages.

---

## Project structure

```text
FreeModels-Proxy/
├── launcher.py
├── main.py
├── requirements.txt
├── FreeModels Proxy.bat
├── build_windows.bat
├── README.md
├── README.fa.md
├── .gitignore
└── assets/
    ├── freemodels-proxy-logo.png
    └── freemodels-proxy.ico
```

### Main components

| File | Purpose |
|---|---|
| `main.py` | FastAPI proxy, request normalization, model routing, streaming and tool-call handling |
| `launcher.py` | Windows desktop launcher and runtime controls |
| `requirements.txt` | Python dependencies for source development |
| `FreeModels Proxy.bat` | Source-version launcher |
| `build_windows.bat` | PyInstaller release build |
| `assets/` | Application logo and Windows icon |

---

## Documentation

At the moment, the repository keeps the primary user documentation in the two README files and the API documentation generated by FastAPI.

| Resource | Purpose |
|---|---|
| [English README](README.md) | Main project overview and setup |
| [راهنمای فارسی](README.fa.md) | Persian documentation |
| `http://127.0.0.1:8000/docs` | Interactive FastAPI documentation |
| `/v1/models` | OpenAI-compatible model discovery endpoint |
| `/v1/chat/completions` | OpenAI-compatible chat endpoint |

As the project grows, dedicated `docs/` pages can be added for installation, usage, architecture, troubleshooting and release engineering without changing the main README structure.

---

## Troubleshooting

| Symptom | What to check |
|---|---|
| Cherry Studio cannot connect | Confirm the proxy is running and use `http://127.0.0.1:8000/v1`. |
| `/docs` does not open | Check the launcher status, host and port. |
| `/v1/models` is empty or unavailable | Check the local proxy logs and the upstream connection. |
| A model request fails | Check the selected model ID and the live logs for an upstream error. |
| Agent/tool workflow stops | Make sure Cherry Studio is actually sending `tools` and that the selected model supports the required workflow. |
| Port 8000 is already in use | Change the launcher port, then update the Cherry Studio Base URL accordingly. |
| EXE does not start | Try the latest release build and check whether Windows security software is blocking the executable. |
| Source version fails to start | Recreate `.venv` and reinstall `requirements.txt`. |

For debugging, the launcher's live log area is the first place to look.

---

## Contributing

Issues, suggestions and pull requests are welcome.

Before submitting a change:

1. Keep the existing project structure and coding style.
2. Avoid unnecessary changes to the proxy's request/response compatibility logic.
3. Test both normal chat and tool/MCP workflows when changing message handling.
4. Keep user-facing documentation synchronized with actual behavior.
5. Do not add credentials, tokens or local secrets to commits.

---

## License

This project is released under the **MIT License**.

See [LICENSE](LICENSE) for the full license text.

Third-party packages keep their own licenses.

---

## Author & support

Built by **Reza Kazemi Fathi**.

[![GitHub](https://img.shields.io/badge/GitHub-rkfcode-181717?logo=github)](https://github.com/rkfcode)
[![Instagram](https://img.shields.io/badge/Instagram-rkfcode-E4405F?logo=instagram)](https://instagram.com/rkfcode)
[![YouTube](https://img.shields.io/badge/YouTube-rkfcode-FF0000?logo=youtube)](https://youtube.com/rkfcode)

Project:

**[github.com/rkfcode/FreeModels-Proxy](https://github.com/rkfcode/FreeModels-Proxy)**

If FreeModels Proxy is useful to you, a ⭐ on the repository helps the project.

### Support the project

- [Daramet — IRR support](https://daramet.com/RKFi)
- [Donatr.ee — USD / crypto](https://donatr.ee/rkfcode/)

<div align="center">

**FreeModels Proxy**  
*Local API compatibility for FreeModels Chat and Cherry Studio.*

</div>
