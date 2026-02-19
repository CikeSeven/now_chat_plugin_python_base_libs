"""Python 代码执行工具（python_exec）。

该工具作为插件脚本运行，不依赖宿主内置 runtime，便于后续完全插件化扩展。
"""

from __future__ import annotations

import contextlib
import io
import traceback
from typing import Any, Dict


def _build_success_result(stdout_text: str, stderr_text: str) -> Dict[str, Any]:
    """构造成功返回对象。"""
    return {
        "ok": True,
        "summary": "python_exec 执行成功",
        "stdout": stdout_text,
        "stderr": stderr_text,
    }


def _build_error_result(stdout_text: str, stderr_text: str) -> Dict[str, Any]:
    """构造失败返回对象。"""
    first_line = stderr_text.strip().splitlines()[0] if stderr_text.strip() else "执行失败"
    return {
        "ok": False,
        "summary": "python_exec 执行失败",
        "error": first_line,
        "stdout": stdout_text,
        "stderr": stderr_text,
    }


def main(payload: Dict[str, Any]) -> Dict[str, Any]:
    """工具入口。

    参数:
        payload: 模型传入参数，至少应包含 `code` 字段。

    返回:
        dict: 结构化执行结果，宿主会直接回填给模型。
    """
    code = str(payload.get("code", "") or "")
    if not code.strip():
        return {
            "ok": False,
            "summary": "python_exec 缺少 code 参数",
            "error": "missing code",
            "stdout": "",
            "stderr": "",
        }

    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    namespace: Dict[str, Any] = {"__name__": "__main__"}

    try:
        # 捕获用户代码输出，避免污染宿主 JSON 通道。
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(
            stderr_buffer
        ):
            exec(code, namespace, namespace)
    except Exception:
        traceback.print_exc(file=stderr_buffer)
        return _build_error_result(
            stdout_text=stdout_buffer.getvalue(),
            stderr_text=stderr_buffer.getvalue(),
        )

    return _build_success_result(
        stdout_text=stdout_buffer.getvalue(),
        stderr_text=stderr_buffer.getvalue(),
    )
