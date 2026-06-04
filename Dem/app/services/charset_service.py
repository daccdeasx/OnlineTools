import codecs
from typing import Tuple


SUPPORTED_ENCODINGS = frozenset({
    "utf-8", "gbk", "gb2312", "gb18030", "big5",
    "iso-8859-1", "latin-1", "utf-16", "utf-16le", "utf-16be",
    "shift_jis", "euc-jp", "euc-kr",
    "ascii", "windows-1252", "cp1252",
})


def convert_encoding(text: str, from_enc: str, to_enc: str) -> Tuple[str, str]:
    """Convert text between encodings. Returns (result, error_message)."""
    from_enc_norm = from_enc.lower().replace("-", "").replace("_", "")
    to_enc_norm = to_enc.lower().replace("-", "").replace("_", "")

    # Map aliases to canonical names
    alias_map = {
        "latin1": "iso-8859-1",
        "utf16": "utf-16",
        "shiftjis": "shift_jis",
        "eucjp": "euc-jp",
        "euckr": "euc-kr",
        "cp1252": "windows-1252",
        "gb2312": "gbk",
    }

    from_enc = alias_map.get(from_enc_norm, from_enc)
    to_enc = alias_map.get(to_enc_norm, to_enc)

    try:
        encoded = text.encode(from_enc, errors="strict")
        result = encoded.decode(to_enc, errors="strict")
        return result, ""
    except UnicodeEncodeError as e:
        return "", f"编码转换失败 ({from_enc} -> {to_enc}): 字符无法映射 - {e}"
    except LookupError as e:
        return "", f"不支持的编码: {e}"


def get_supported_encodings() -> "list[str]":
    return sorted(SUPPORTED_ENCODINGS)

