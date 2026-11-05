"""插件加载器：启动时自动扫描 plugins/ 下每个子目录的 plugin.py，
把里面继承了 Plugin 的类找出来、创建实例、注册进平台。

这个文件的作用就是让你"新增插件目录后，不用改任何其他代码"。
一般不需要修改这个文件。
"""

import importlib.util
import inspect
from pathlib import Path

from .plugin_base import Plugin
from .registry import registry

PLUGINS_DIR = Path(__file__).resolve().parent.parent / "plugins"


def load_all(plugins_dir=PLUGINS_DIR):
    """扫描并加载所有插件，返回加载成功的插件名列表。
    某一个插件写错了不会影响其他插件正常加载。
    """
    loaded = []
    if not plugins_dir.exists():
        return loaded

    for entry in sorted(plugins_dir.iterdir()):
        module_file = entry / "plugin.py"
        if not entry.is_dir() or not module_file.exists():
            continue

        # 把 plugin.py 当作一个 Python 模块动态导入进来
        module_name = f"plugins.{entry.name}.plugin"
        spec = importlib.util.spec_from_file_location(module_name, module_file)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:
            print(f"[loader] 加载插件目录 {entry.name} 失败: {exc}")
            continue

        # 在这个模块里找出所有继承了 Plugin 的类，逐个创建实例并注册
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Plugin) and obj is not Plugin and obj.__module__ == module_name:
                try:
                    instance = obj()
                    registry.register(instance)
                    loaded.append(instance.name)
                except Exception as exc:
                    print(f"[loader] 实例化/注册插件 {obj.__name__} 失败: {exc}")

    return loaded
