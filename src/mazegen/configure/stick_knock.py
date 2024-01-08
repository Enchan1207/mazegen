#
# 棒倒し法によるコンフィギュレータ
#
import random
from typing import List, Optional, Union

from mazegen.field import Field, TileType

from ..position import Direction, Position
from . import FieldConfiguratorBase


class StickKnockConfigurator(FieldConfiguratorBase):
    """棒倒し法の実装"""

    def __init__(self, seed: Optional[Union[int, str, bytes, bytearray, float]] = None):
        random.seed(seed)

    def configure(self, field: Field):
        # 外壁と格子状の壁を構成
        self._initwall(field)

        # 各ポイントに設置された壁から棒を倒していく
        self._knockstick(field)

    def _initwall(self, field: Field):
        """壁の初期状態を設定する

        Args:
            field (Field): フィールド
        """
        for pos, _ in field.fetch_cells():
            # 上下端を壁にする
            if pos.y % (field.height - 1) == 0:
                field.set_tile(pos, TileType.Wall)

            # 左右端を壁にする
            if pos.x % (field.width - 1) == 0:
                field.set_tile(pos, TileType.Wall)

            # 偶数行の偶数列を壁にする
            if pos.y % 2 == 0 and pos.x % 2 == 0:
                field.set_tile(pos, TileType.Wall)

    def _knockstick(self, field: Field):
        """棒を倒す

        Args:
            field (Field): フィールド
        """

        def get_knockable_dirs(at: Position) -> List[Direction]:
            """指定した座標から棒を倒せる方向のリストを生成

            Args:
                at (Position): フィールド上の位置

            Returns:
                List[Direction]: 棒を倒せる方向
            """
            available_dirs: List[Direction] = [Direction.Up, Direction.Down, Direction.Left, Direction.Right]

            # 最上行以外なら上は選ばない
            if wy != 2:
                available_dirs.remove(Direction.Up)

            # 有効な方向に壁があるなら取り除く
            for dir in available_dirs:
                if field.get_tile(at.advanced(dir)) == TileType.Wall:
                    available_dirs.remove(dir)

            return available_dirs

        # 各壁について
        for wy in range(2, field.height - 1, 2):
            for wx in range(2, field.width - 1, 2):
                # 倒せる方向のリストを取得し
                pos = Position(wx, wy)
                direction_candidates = get_knockable_dirs(pos)
                if len(direction_candidates) == 0:
                    continue

                # ランダムに倒す
                knock_dir = random.choice(direction_candidates)
                field.set_tile(pos.advanced(knock_dir), TileType.Wall)
