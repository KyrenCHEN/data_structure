"""平台入口：加载 plugins/ 下所有插件后启动 UI。"""
from core.loader import load_all
from ui.app import main as launch_ui


def main() -> None:
    loaded = load_all()
    print(f"[main] 已加载插件: {loaded}")
    launch_ui()


if __name__ == "__main__":
    main()
