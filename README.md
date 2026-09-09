<p align="center">
  <img src="assets/freemodels-proxy-logo.png" alt="FreeModels Proxy" width="420">
</p>

<p align="center"><strong>OpenAI-compatible local proxy for Cherry Studio</strong></p>

# FreeModels Proxy

English | [فارسی](README.fa.md)

A polished Windows desktop launcher for a local OpenAI-compatible proxy.

## End users (recommended)

Download **FreeModels Proxy.exe** from GitHub Releases and double-click it.

- No Python
- No pip
- No PowerShell
- No dependency installation

The executable is built with PyInstaller and bundles the Python runtime and application dependencies.


## Standalone EXE

The recommended distribution is `FreeModels Proxy.exe`. It includes the application runtime and dependencies, starts the proxy automatically, and requires no Python, pip, PowerShell, or manual dependency installation.

## Source version

For contributors or users running from source:

1. Download and extract the repository.
2. Double-click `FreeModels Proxy.bat`.
3. On first run, the launcher creates a local `.venv` and installs dependencies automatically.
4. Future runs open the application directly.

## Developer

**Reza Kazemi**

GitHub: https://github.com/rkfcode

## Support

- IRR: https://daramet.com/RKFi
- USD / Crypto: https://donatr.ee/rkfcode/

## Build EXE

Run `build_windows.bat` on Windows.

The output is:

`dist/FreeModels Proxy.exe`

For distribution, upload the EXE to a GitHub Release.

## Cherry Studio

Base URL:

`http://127.0.0.1:8000/v1`
