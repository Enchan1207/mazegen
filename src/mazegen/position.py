#
#
#
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Tuple


class Direction(Enum):
    """方向"""

    Up = auto()
    """上"""

    Down = auto()
    """下"""

    Left = auto()
    """左"""

    Right = auto()
    """右"""

    @staticmethod
    def all() -> List[Direction]:
        """全方向のリストを取得

        Returns:
            List[Direction]: 方向リスト
        """
        return [Direction.Up, Direction.Right, Direction.Down, Direction.Left]

    def unit_vec(self) -> Tuple[int, int]:
        """方向が表す単位ベクトルを取得

        Returns:
            Tuple[int, int]: 方向に対応する単位ベクトル
        """
        match self:
            case Direction.Up:
                return (0, -1)

            case Direction.Down:
                return (0, 1)

            case Direction.Left:
                return (-1, 0)

            case Direction.Right:
                return (1, 0)


@dataclass
class Position:
    """座標"""

    x: int
    """x座標"""

    y: int
    """y座標"""

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def advance(self, dir: Direction, amplitude: int = 1):
        """指定方向に座標を移動する

        Args:
            dir (Direction): 方向
            amplitude (int, optional): 移動量. Defaults to 1.
        """
        self = self.advanced(dir, amplitude)

    def advanced(self, dir: Direction, amplitude: int = 1) -> Position:
        """指定方向に座標を移動したオブジェクトを返す

        Args:
            dir (Direction): 方向
            amplitude (int, optional): 移動量. Defaults to 1.

        Returns:
            Position: 移動先を値にもつ座標オブジェクト
        """
        # 移動量を計算
        dx, dy = dir.unit_vec()
        dx *= amplitude
        dy *= amplitude
        return Position(self.x + dx, self.y + dy)
