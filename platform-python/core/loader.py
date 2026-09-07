"""插件加载器：扫描 plugins/ 下每个子目录的 plugin.py，
自动发现 Plugin 子类并注册。学生新增插件时无需修改本文件。
"""
from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

from .plugin_base import Plugin
from .registry import registry

PLUGINS_DIR = Path(__file__).resolve().parent.parent / "plugins"


def load_all(plugins_dir: Path = PLUGINS_DIR) -> list[str]:
    """返回本次加载成功的插件名列表；单个插件出错不影响其余插件。"""
    loaded: list[str] = []
    if not plugins_dir.exists():
        return loaded

    for entry in sorted(plugins_dir.iterdir()):
        module_file = entry / "plugin.py"
        if not entry.is_dir() or not module_file.exists():
            continue

        module_name = f"plugins.{entry.name}.plugin"
        spec = importlib.util.spec_from_file_location(module_name, module_file)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:  # noqa: BLE001 单个插件异常不应拖垮平台
            print(f"[loader] 加载插件目录 {entry.name} 失败: {exc}")
            continue

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Plugin) and obj is not Plugin and obj.__module__ == module_name:
                try:
                    instance = obj()
                    registry.register(instance)
                    loaded.append(instance.name)
                except Exception as exc:  # noqa: BLE001
                    print(f"[loader] 实例化/注册插件 {obj.__name__} 失败: {exc}")

    return loaded
