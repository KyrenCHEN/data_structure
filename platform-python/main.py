"""平台入口：扫描 plugins/ 下每个子目录的 plugin.py，找出其中的 Plugin
子类、创建实例，然后启动界面。新增插件目录后不用改这个文件，重新运行即可。
"""

import importlib.util
import inspect
from pathlib import Path

from plugin_base import Plugin
from app import PlatformApp

PLUGINS_DIR = Path(__file__).resolve().parent / "plugins"


def load_plugins():
    """扫描并加载所有插件，返回插件实例列表。
    某一个插件写错了不会影响其他插件正常加载。
    """
    plugins = []
    if not PLUGINS_DIR.exists():
        return plugins

    for entry in sorted(PLUGINS_DIR.iterdir()):
        module_file = entry / "plugin.py"
        if not entry.is_dir() or not module_file.exists():
            continue

        # 把 plugin.py 当作一个 Python 模块动态导入进来
        module_name = f"plugin_{entry.name}"
        spec = importlib.util.spec_from_file_location(module_name, module_file)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:
            print(f"[main] 加载插件目录 {entry.name} 失败: {exc}")
            continue

        # 在这个模块里找出所有继承了 Plugin 的类，逐个创建实例
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Plugin) and obj is not Plugin and obj.__module__ == module_name:
                try:
                    plugins.append(obj())
                except Exception as exc:
                    print(f"[main] 实例化插件 {obj.__name__} 失败: {exc}")

    return plugins


def main() -> None:
    plugins = load_plugins()
    print(f"[main] 已加载插件: {[p.name for p in plugins]}")
    app = PlatformApp(plugins)
    app.mainloop()


if __name__ == "__main__":
    main()
