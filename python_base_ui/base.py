"""Python 基础库插件的 UI DSL 基类。

说明：
- 该文件给插件作者提供稳定的组件协议封装，减少手写 dict 错误。
- 宿主会读取 `to_dict()` 输出并渲染对应的 Flutter 组件。
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


class UiComponent:
    """通用组件基类。"""

    def __init__(
        self,
        component_id: str,
        component_type: str,
        label: str = "",
        description: str = "",
        enabled: bool = True,
        visible: bool = True,
    ) -> None:
        # 在基类统一清洗字段，避免子类重复处理输入。
        self.id = str(component_id).strip()
        self.type = str(component_type).strip()
        self.label = str(label).strip()
        self.description = str(description).strip()
        self.enabled = bool(enabled)
        self.visible = bool(visible)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为宿主可消费的组件结构。"""
        return {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "description": self.description,
            "enabled": self.enabled,
            "visible": self.visible,
        }


class UiButton(UiComponent):
    """按钮组件。"""

    def __init__(
        self,
        component_id: str,
        label: str,
        description: str = "",
        style: str = "primary",
        enabled: bool = True,
        visible: bool = True,
    ) -> None:
        super().__init__(
            component_id=component_id,
            component_type="button",
            label=label,
            description=description,
            enabled=enabled,
            visible=visible,
        )
        self.style = str(style).strip() if str(style).strip() else "primary"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["style"] = self.style
        return data


class UiSwitch(UiComponent):
    """开关组件。"""

    def __init__(
        self,
        component_id: str,
        label: str,
        description: str = "",
        value: bool = False,
        enabled: bool = True,
        visible: bool = True,
    ) -> None:
        super().__init__(
            component_id=component_id,
            component_type="switch",
            label=label,
            description=description,
            enabled=enabled,
            visible=visible,
        )
        self.value = bool(value)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["value"] = self.value
        return data


class UiTextInput(UiComponent):
    """文本输入组件。"""

    def __init__(
        self,
        component_id: str,
        label: str,
        description: str = "",
        value: str = "",
        placeholder: str = "",
        multiline: bool = False,
        enabled: bool = True,
        visible: bool = True,
    ) -> None:
        super().__init__(
            component_id=component_id,
            component_type="text_input",
            label=label,
            description=description,
            enabled=enabled,
            visible=visible,
        )
        self.value = str(value)
        self.placeholder = str(placeholder).strip()
        self.multiline = bool(multiline)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["value"] = self.value
        data["placeholder"] = self.placeholder
        data["multiline"] = self.multiline
        return data


class UiPage:
    """插件页面基类。"""

    def build(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """页面初次加载时返回 UI 结构。"""
        return {
            "title": "插件配置",
            "subtitle": "",
            "components": [],
            "state": {},
        }

    def on_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """页面事件回调，默认行为是按 build 返回。"""
        payload = event.get("payload", {}) if isinstance(event, dict) else {}
        return self.build({"payload": payload})

    def to_page(
        self,
        title: str = "",
        subtitle: str = "",
        components: Optional[Iterable[UiComponent]] = None,
        state: Optional[Dict[str, Any]] = None,
        message: str = "",
    ) -> Dict[str, Any]:
        """组装统一页面协议，避免子类重复拼装结构。"""
        return {
            "title": str(title).strip(),
            "subtitle": str(subtitle).strip(),
            "components": [item.to_dict() for item in (components or [])],
            "state": state or {},
            "message": str(message).strip(),
        }
