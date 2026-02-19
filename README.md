# Python Base Libs Plugin

> 这是一个“Python 基础库插件”起始实现，用于给 NowChat 提供可选的 Python 科学计算能力。

## 插件功能说明
该插件当前提供以下能力：

1. 基础库环境占位
- 约定将 Python 相关基础库文件放入 `libs/` 目录。
- 插件安装后会把 `libs/` 加入 Python 运行路径（`pythonPathEntries`）。
- 该插件默认开启 `providesGlobalPythonPaths=true`，安装并启用后可为其他插件提供共享库路径。

2. 工具：`python_exec`（唯一对模型暴露的工具）
- 用于给大模型执行 Python 代码并返回 stdout/stderr。
- 插件只注册这一个工具，避免暴露多余工具干扰模型决策。

3. 插件配置页面
- 提供“检查 Python 环境”按钮（检查 Python/NumPy/Pandas 是否可用）。
- 提供 Python 代码输入框与“执行代码”按钮。
- 页面下方直接显示执行输出，方便手动调试环境。

## 目录结构
```text
python_base_libs_plugin/
  plugin.json
  README.md
  assets/
    .gitkeep
  hooks/
    app_start.py
  libs/
    .gitkeep
  runtime/
    .gitkeep
  tools/
    （可选扩展脚本目录；当前仅使用内置 `builtin_python_exec`）
  python_base_ui/
    __init__.py
    base.py
    schema.py
```

## plugin.json 关键字段
- `type`: `python`
- `pythonNamespace`: `python_base_ui`（插件配置页入口路径为 `python_base_ui/schema.py`）
- `providesGlobalPythonPaths`: `true`（安装后为其他插件提供共享 Python 路径）

## 使用方式
1. 将 `python_base_libs_plugin` 目录压缩为 zip（zip 根目录必须直接包含 `plugin.json`）。
2. 在应用中进入“插件中心”并导入该 zip。
3. 安装后在插件配置页先点“检查 Python 环境”，再输入代码点击“执行代码”验证。

## 后续计划
- 把基础库打包为可下载聚合包，并接入远程清单分发。
- 在配置页增加代码模板快捷插入（如 NumPy / Pandas 示例）。
- 增加更多常见原生依赖（如 `scipy` 所需底层依赖）的兼容方案。
