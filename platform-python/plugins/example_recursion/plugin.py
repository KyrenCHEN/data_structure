"""示例插件：汉诺塔（递归）。

作为 E1.3 的参考实现，演示插件接口的最小可运行写法。
学生完成 E1.3 时应在 plugins/ 下新建自己的目录（如 plugins/hanoi_myname/），
不要直接修改本文件。
"""
from __future__ import annotations

from core.plugin_base import ParamSpec, Plugin


class HanoiPlugin(Plugin):
    name = "汉诺塔求解（示例）"
    category = "E1.3 递归算法"
    version = "1.0"
    author = "platform-team"

    def params(self) -> list[ParamSpec]:
        return [
            ParamSpec(name="n", label="盘子数量 n", type="int", default=4,
                      help="建议 1~15，n 越大步骤越多"),
        ]

    def run(self, **kwargs) -> str:
        n = int(kwargs["n"])
        if n < 1:
            return "n 必须 >= 1"

        moves: list[str] = []

        def hanoi(k: int, src: str, aux: str, dst: str) -> None:
            if k == 0:
                return
            hanoi(k - 1, src, dst, aux)
            moves.append(f"{src} -> {dst}")
            hanoi(k - 1, aux, src, dst)

        hanoi(n, "A", "B", "C")
        lines = [f"共 {len(moves)} 步（理论最少步数 2^n - 1 = {2 ** n - 1}）："]
        lines.extend(moves)
        return "\n".join(lines)
