"""Tests for filename sanitization."""

from mac2win_zip import sanitize_windows_filename


def test_sanitize_basic():
    """Test basic filename sanitization."""
    assert sanitize_windows_filename("hello.txt") == "hello.txt"


def test_sanitize_forbidden_chars():
    """Test removal of Windows forbidden characters."""
    assert sanitize_windows_filename("file<name>.txt") == "filename.txt"
    assert sanitize_windows_filename("file:name.txt") == "filename.txt"
    assert sanitize_windows_filename('file"name.txt') == "filename.txt"
    assert sanitize_windows_filename("file|name.txt") == "filename.txt"
    assert sanitize_windows_filename("file?name.txt") == "filename.txt"
    assert sanitize_windows_filename("file*name.txt") == "filename.txt"


def test_sanitize_backslash():
    """Test removal of backslash."""
    assert sanitize_windows_filename("file\\name.txt") == "filename.txt"


def test_sanitize_null_bytes():
    """Test removal of null bytes."""
    assert sanitize_windows_filename("file\x00name.txt") == "filename.txt"


def test_sanitize_whitespace():
    """Test whitespace normalization."""
    assert sanitize_windows_filename("file  name.txt") == "file name.txt"
    assert sanitize_windows_filename("file\t\tname.txt") == "file name.txt"


def test_sanitize_path():
    """Test path preservation."""
    assert sanitize_windows_filename("folder/file.txt") == "folder/file.txt"
    assert sanitize_windows_filename("folder/sub:folder/file?.txt") == "folder/subfolder/file.txt"


def test_sanitize_unicode():
    """Test Unicode filename handling."""
    assert sanitize_windows_filename("파일.txt") == "파일.txt"
    assert sanitize_windows_filename("안녕하세요.txt") == "안녕하세요.txt"
    assert sanitize_windows_filename("こんにちは.txt") == "こんにちは.txt"


def test_sanitize_empty_parts():
    """Test handling of empty path parts."""
    assert sanitize_windows_filename("./file.txt") == "file.txt"
    assert sanitize_windows_filename("../file.txt") == "file.txt"
    assert sanitize_windows_filename("folder//file.txt") == "folder/file.txt"
