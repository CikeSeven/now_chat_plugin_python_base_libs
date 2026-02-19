"""Python 基础库插件配置页。

页面目标：
1. 提供“检查 Python 环境”按钮，快速确认核心模块可导入。
2. 提供 Python 代码输入与执行按钮，直接在页面内试跑代码。
"""

from __future__ import annotations

import contextlib
import io
import traceback
from typing import Any, Dict

from python_base_ui import UiButton
from python_base_ui import UiPage
from python_base_ui import UiTextInput


class PythonBaseLibsConfigPage(UiPage):
    """基础库插件配置页实现。"""

    def _default_state(self) -> Dict[str, Any]:
        """默认页面状态。"""
        return {
            "python_code": "print('hello nowchat')",
            "exec_output": "",
        }

    def _check_environment(self) -> str:
        """执行环境检查并返回可读文本。"""
        lines = []
        try:
            import sys

            lines.append(f"Python: {sys.version.split()[0]}")
        except Exception as error:
            lines.append(f"Python版本读取失败: {error}")

        for module_name in ("numpy", "pandas"):
            try:
                module = __import__(module_name)
                version = getattr(module, "__version__", "unknown")
                lines.append(f"{module_name}: OK ({version})")
            except Exception as error:
                lines.append(f"{module_name}: FAIL ({error})")
        return "\n".join(lines)

    def _execute_python_code(self, code: str) -> str:
        """在页面内执行 Python 代码并返回标准输出/错误。

        约定：
        - 支持通过 `_result` 变量回传最终对象；
        - 标准输出和异常栈都写入输出面板。
        """
        text = (code or "").strip()
        if not text:
            return "请输入 Python 代码。"

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        local_scope: Dict[str, Any] = {"_result": None}
        try:
            with contextlib.redirect_stdout(stdout_buffer):
                with contextlib.redirect_stderr(stderr_buffer):
                    exec(text, {}, local_scope)
        except Exception:
            traceback.print_exc(file=stderr_buffer)

        stdout_text = stdout_buffer.getvalue().strip()
        stderr_text = stderr_buffer.getvalue().strip()
        result_text = ""
        if "_result" in local_scope and local_scope["_result"] is not None:
            result_text = f"_result = {local_scope['_result']}"

        sections = []
        if stdout_text:
            sections.append(f"[stdout]\n{stdout_text}")
        if result_text:
            sections.append(f"[result]\n{result_text}")
        if stderr_text:
            sections.append(f"[stderr]\n{stderr_text}")
        if not sections:
            sections.append("执行完成，无输出。")
        return "\n\n".join(sections)

    def _components(self, state: Dict[str, Any]):
        """根据当前状态生成 UI 组件列表。"""
        return [
            UiButton(
                component_id="check_environment",
                label="检查 Python 环境",
                description="检查 Python / NumPy / Pandas 是否可用。",
            ),
            UiTextInput(
                component_id="python_code",
                label="Python 代码",
                description="输入后点击“执行代码”。可使用 `_result` 返回最终结果。",
                placeholder="例如：import numpy as np\n_result = np.arange(5).tolist()",
                value=str(state.get("python_code", "")),
                multiline=True,
            ),
            UiButton(
                component_id="execute_code",
                label="执行代码",
                description="在当前 Python 环境执行轻量代码（不建议长时或高负载任务）。",
            ),
            UiTextInput(
                component_id="exec_output",
                label="执行输出",
                description="显示环境检查结果或代码执行输出。",
                value=str(state.get("exec_output", "")),
                multiline=True,
                enabled=False,
            ),
        ]

    def build(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """首屏渲染。"""
        state = self._default_state()
        return self.to_page(
            title="Python 基础库插件配置",
            subtitle="检查环境并试运行 Python 代码",
            components=self._components(state),
            state=state,
        )

    def on_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """处理页面交互并返回下一帧页面。"""
        event = event or {}
        state = dict(event.get("state") or {})
        event_type = str(event.get("type", "")).strip()
        component_id = str(event.get("componentId", "")).strip()
        value = event.get("value")

        message = ""
        if event_type == "input_submit" and component_id == "python_code":
            state["python_code"] = "" if value is None else str(value)
            message = "代码已更新"
        elif event_type == "button_click" and component_id == "check_environment":
            state["exec_output"] = self._check_environment()
            message = "环境检查已完成"
        elif event_type == "button_click" and component_id == "execute_code":
            code = str(state.get("python_code", ""))
            state["exec_output"] = self._execute_python_code(code)
            message = "代码执行完成"

        return self.to_page(
            title="Python 基础库插件配置",
            subtitle="检查环境并试运行 Python 代码",
            components=self._components(state),
            state=state,
            message=message,
        )


def create_page() -> UiPage:
    """插件 UI 工厂入口。"""
    return PythonBaseLibsConfigPage()
