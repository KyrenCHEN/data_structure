"""插件接口规范（Python 版）。

任何插件必须继承 Plugin 并实现 params() 与 run()。
run() 的返回值必须是 str，将原样显示在 UI 输出区。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParamSpec:
    """描述一个可在 UI 中生成输入控件的参数。"""
    name: str
    label: str
    type: str = "str"          # "int" | "float" | "str"
    default: Any = ""
    help: str = ""


class Plugin(ABC):
    name: str = "unnamed"
    category: str = "misc"     # 建议按实验编号命名，如 "E1.3 递归算法"
    version: str = "1.0"
    author: str = ""

    @abstractmethod
    def params(self) -> list[ParamSpec]:
        """声明本插件需要哪些输入参数，供 UI 自动生成表单。"""

    @abstractmethod
    def run(self, **kwargs: Any) -> str:
        """执行核心算法逻辑，kwargs 的 key 与 params() 中的 name 对应。"""

    def describe(self) -> str:
        return f"[{self.category}] {self.name} v{self.version}"
