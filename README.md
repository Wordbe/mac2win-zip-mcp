# mac2win-zip MCP Server

<p align="center">
  <img src="https://img.shields.io/pypi/v/mac2win-zip-mcp.svg" alt="PyPI Version">
  <img src="https://img.shields.io/pypi/pyversions/mac2win-zip-mcp.svg" alt="Python Versions">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-macOS-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/MCP-v1.9+-purple.svg" alt="MCP Version">
</p>

<p align="center">
  <strong>Create Windows-compatible ZIP files from macOS via MCP</strong>
</p>

> **An MCP (Model Context Protocol) server for creating Windows-compatible ZIP files.**
>
> This MCP server wraps the functionality of [mac2win-zip](https://github.com/Wordbe/mac2win-zip) to create ZIP files that work perfectly on Windows from macOS.

## Why mac2win-zip MCP Server?

### The Problem

macOS uses **NFD (Normalization Form Decomposed)** for Unicode filenames, while Windows uses **NFC (Normalization Form Composed)**. When you create a ZIP file on macOS containing files with Unicode characters (like Korean, Japanese, or special characters), Windows users often see garbled filenames.

| macOS (ZIP created)   | Windows (ZIP opened) |
| --------------------- | -------------------- |
| 📄 Hello?.pdf          | ❌ (removed)          |
| 📄 안녕하세요 세상.pdf | ❌ (removed)          |

### The Solution

This MCP server automatically:
1. Normalizes all filenames from NFD to NFC
2. Removes or replaces Windows-forbidden characters
3. Excludes macOS-specific files (`.DS_Store`, etc.)
4. Preserves the folder structure

**Result:** ZIP files that work perfectly on both macOS and Windows!

| macOS (ZIP created)   | Windows (ZIP opened)  |
| --------------------- | --------------------- |
| 📄 Hello.pdf          | ✅ Hello.pdf           |
| 📄 안녕하세요 세상.pdf | ✅ 안녕하세요 세상.pdf |

## Installation

### Quick Start - One Command! 🚀

The easiest way to add this MCP server to Claude Desktop:

```bash
claude mcp add --transport stdio mac2win-zip -- uvx mac2win-zip-mcp
```

**That's it!** Restart Claude Desktop and it's ready to use.

### For Developers

Contributing or developing? Clone and install in editable mode:

```bash
git clone https://github.com/Wordbe/mac2win-zip-mcp.git
cd mac2win-zip-mcp
uv pip install -e ".[dev]"
```

## Usage

### MCP Tools

This server provides the following tools:

#### `create_windows_compatible_zip`

Create a Windows-compatible ZIP file from files and/or folders.

**Parameters:**
- `paths` (array, required): List of file or folder paths to zip
- `output` (string, optional): Output ZIP filename (default: "archive.zip")
- `working_dir` (string, optional): Base directory for relative paths

**Example usage:**
```
Create a Windows-compatible ZIP of the current directory

Paths: ["."]
Output: "backup.zip"
```

#### `validate_zip_for_windows`

Validate if a ZIP file is Windows-compatible.

**Parameters:**
- `zip_path` (string, required): Path to the ZIP file to validate
- `working_dir` (string, optional): Base directory for relative path

**Example usage:**
```
Check if a ZIP file is Windows-compatible

ZIP Path: "archive.zip"
```

## Example Usage

Once configured in Claude Desktop, simply ask Claude in natural language:

**Create a Windows-compatible ZIP:**
```
Create a Windows-compatible ZIP of my Documents folder.
```

**Validate an existing ZIP:**
```
Check if backup.zip is Windows-compatible.
```

**Batch processing:**
```
Create Windows-compatible ZIPs for all folders in ~/Projects
```

Claude will automatically use the MCP tools to create properly formatted ZIP files that work perfectly on Windows!

## Features

- **Unicode Normalization**: Converts macOS NFD filenames to Windows-compatible NFC
- **Character Sanitization**: Removes Windows-forbidden characters (`<>:"|?*\`)
- **Auto Recursive**: Automatically includes all subdirectories when zipping folders
- **Smart Naming**: Creates `folder-name.zip` by default (no -o needed for single folder)
- **Structure Preservation**: Maintains original folder hierarchy in ZIP
- **Smart Filtering**: Excludes hidden files (`.DS_Store`, etc.)
- **Korean Support**: Perfect handling of Korean and other Unicode filenames
- **MCP Protocol**: Works with any MCP-compliant AI assistant (Claude, etc.)

## Requirements

- **uv** - Fast Python package runner
  - Install: `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Claude Desktop** (or any MCP-compatible AI assistant)

**Note:** Python is NOT required! `uvx` automatically downloads and manages Python 3.10+ for you.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Architecture

This MCP server is a thin wrapper around the [mac2win-zip](https://github.com/Wordbe/mac2win-zip) library, exposing its functionality via the Model Context Protocol. This means:

- **Single source of truth**: Core ZIP creation logic lives in `mac2win-zip`
- **Always in sync**: Updates to `mac2win-zip` automatically benefit this MCP server
- **Separation of concerns**: CLI tool and MCP server share the same battle-tested code

## Related Projects

- [mac2win-zip](https://github.com/Wordbe/mac2win-zip) - CLI tool for creating Windows-compatible ZIP files (core library)
- [Model Context Protocol](https://modelcontextprotocol.io/) - The protocol powering this server

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Bug Reports

If you discover any bugs, please create an issue on GitHub with:
- Your operating system and version
- Python version
- MCP client information
- Steps to reproduce the bug
- Expected vs actual behavior

## Show Your Support

If this project helped you, please give it a star!

---

<p align="center">
  Made with ❤️ by Wordbe for seamless macOS-Windows file sharing
</p>
