#
# 穴掘り法によるコンフィギュレータ
#
import random
from collections import deque
from typing import List, Optional, Tuple, Union

from ..field import Field, TileType
from ..position import Direction, Position
from . import FieldConfiguratorBase


class AisleDigConfigurator(FieldConfiguratorBase):
    """穴掘り法の実装"""

    def __init__(self, seed: Optional[Union[int, str, bytes, bytearray, float]] = None):
        self.seed = seed

    def configure(self, field: Field):
        random.seed(self.seed)

        # 一旦全部壁にする
        for pos, _ in field.fetch_cells():
            field.set_tile(pos, TileType.Wall)

        # 開始点を決めてキューに積む
        pos_stack: deque[Position] = deque()
        pos = Position(1, 1)
        pos_stack.append(pos)

        while len(pos_stack) > 0:
            # スタック先頭の値を取り出し、進める方向のリストを得る
            pos = pos_stack[-1]
            enterable_dirs = self._enterable_dirs(field, pos)

            # どこにも進めないなら要素を削除してもう一度
            if len(enterable_dirs) == 0:
                pos_stack.pop()
                continue

            # 方向を決定して掘り進め、新しい座標をスタックに積む
            dest_dir = random.choice(enterable_dirs)
            new_pos = self._dig_hole(field, pos, dest_dir)
            pos_stack.append(new_pos)

    def _dig_hole(self, field: Field, pos: Position, dir: Direction) -> Position:
        """位置と方向を指定して掘る

        Args:
            field (Field): フィールド
            pos (Position): 位置
            dir (Direction): 方向

        Returns:
            Position: 進んだ先の座標
        """
        field.set_tile(pos, TileType.Aisle)
        field.set_tile(pos.advanced(dir), TileType.Aisle)
        field.set_tile(pos.advanced(dir, 2), TileType.Aisle)
        return pos.advanced(dir, 2)

    def _enterable_dirs(self, field: Field, pos: Position) -> List[Direction]:
        """その位置から進める方向のリストを取得

        Args:
            field (Field): フィールド
            pos (Position): 位置

        Returns:
            List[Direction]: 方向リスト
        """
        # 2マス先が壁なら掘れる
        is_enterable = lambda d: field.get_tile(pos.advanced(d, 2)) == TileType.Wall
        enterable_dirs = list(filter(is_enterable, Direction.all()))
        return enterable_dirs
