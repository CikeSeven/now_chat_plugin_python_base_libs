"""Python 基础库插件启动 Hook。

该 Hook 仅用于记录插件已完成加载，避免在启动阶段执行重逻辑。
"""


def main(payload):
    """处理 `app_start` 事件。

    参数:
        payload: Hook 上下文，由宿主注入，包含 event/payload/timestamp。

    返回:
        dict: 轻量调试信息，不影响主流程。
    """
    return {
        "ok": True,
        "hook": "app_start",
        "plugin": "now_chat_plugin_python_base_libs",
        "event": payload.get("event"),
    }
