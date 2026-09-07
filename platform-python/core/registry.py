"""插件注册表：全局单例，负责持有已加载插件实例。"""
from __future__ import annotations

from .plugin_base import Plugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        key = plugin.name
        if key in self._plugins:
            raise ValueError(f"插件名重复: {key}")
        self._plugins[key] = plugin

    def get(self, name: str) -> Plugin:
        return self._plugins[name]

    def all(self) -> list[Plugin]:
        return sorted(self._plugins.values(), key=lambda p: (p.category, p.name))

    def by_category(self) -> dict[str, list[Plugin]]:
        groups: dict[str, list[Plugin]] = {}
        for p in self.all():
            groups.setdefault(p.category, []).append(p)
        return groups


registry = PluginRegistry()
