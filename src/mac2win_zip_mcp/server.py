#!/usr/bin/env python3
"""mac2win-zip MCP Server - Create Windows-compatible ZIP files from macOS via MCP"""

import os
import unicodedata
import zipfile
from typing import List, Optional

from mac2win_zip import create_windows_compatible_zip as create_zip_core
from mcp.server import FastMCP

mcp = FastMCP("mac2win-zip-mcp")


@mcp.tool()
def create_windows_compatible_zip(
    paths: List[str], output: str = "archive.zip", working_dir: Optional[str] = None
) -> dict:
    """Create Windows-compatible ZIP file from files and/or folders.

    Args:
        paths: List of file or folder paths to zip
        output: Output ZIP filename
        working_dir: Base directory for relative paths
    """
    try:
        original_cwd = None
        if working_dir:
            original_cwd = os.getcwd()
            if not os.path.isdir(working_dir):
                return {"status": "error", "message": f"Working directory not found: {working_dir}"}
            os.chdir(working_dir)

        try:
            if not create_zip_core(paths, output):
                return {"status": "error", "message": "Failed to create ZIP file"}

            if not os.path.exists(output):
                return {"status": "error", "message": f"ZIP file was not created: {output}"}

            with zipfile.ZipFile(output, "r") as zipf:
                files_list = [info.filename for info in zipf.filelist]
                file_count = len(files_list)

            file_size_mb = round(os.path.getsize(output) / 1024 / 1024, 2)

            return {
                "status": "success",
                "message": f"Created Windows-compatible ZIP: {output}",
                "output_path": os.path.abspath(output),
                "file_count": file_count,
                "file_size_mb": file_size_mb,
                "files": files_list,
            }
        finally:
            if original_cwd:
                os.chdir(original_cwd)
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {e}"}


@mcp.tool()
def validate_zip_for_windows(zip_path: str, working_dir: Optional[str] = None) -> dict:
    """Validate if a ZIP file is Windows-compatible.

    Args:
        zip_path: Path to the ZIP file to validate
        working_dir: Base directory for relative path
    """
    try:
        original_cwd = None
        if working_dir:
            original_cwd = os.getcwd()
            if not os.path.isdir(working_dir):
                return {"status": "error", "message": f"Working directory not found: {working_dir}"}
            os.chdir(working_dir)

        try:
            if not os.path.exists(zip_path):
                return {"status": "error", "message": f"ZIP file not found: {zip_path}"}

            issues = []
            forbidden = '<>:"|\\?*'

            with zipfile.ZipFile(zip_path, "r") as zipf:
                for info in zipf.filelist:
                    if unicodedata.normalize("NFC", info.filename) != info.filename:
                        issues.append({
                            "type": "nfc_normalization",
                            "severity": "error",
                            "filename": info.filename,
                            "message": "Filename is not NFC normalized",
                        })

                    for part in info.filename.split("/"):
                        forbidden_chars = [c for c in part if c in forbidden]
                        if forbidden_chars:
                            issues.append({
                                "type": "forbidden_character",
                                "severity": "error",
                                "filename": part,
                                "message": f"Contains forbidden characters: {forbidden_chars}",
                            })

            return {
                "status": "success",
                "is_windows_compatible": len(issues) == 0,
                "total_files": len(zipfile.ZipFile(zip_path, "r").filelist),
                "issues": issues,
                "message": "ZIP file is Windows-compatible" if not issues else f"Found {len(issues)} issue(s)",
            }
        finally:
            if original_cwd:
                os.chdir(original_cwd)
    except Exception as e:
        return {"status": "error", "message": f"Validation failed: {e}"}


def main():
    mcp.run()
