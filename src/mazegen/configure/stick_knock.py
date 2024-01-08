#
# 棒倒し法によるコンフィギュレータ
#
import random
from typing import Optional, Tuple, Union

from mazegen.field import Field, TileType

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
        for y in range(field.height):
            for x in range(field.width):
                # 上下端を壁にする
                if y % (field.height - 1) == 0:
                    field.set_tile(x, y, TileType.Wall)

                # 左右端を壁にする
                if x % (field.width - 1) == 0:
                    field.set_tile(x, y, TileType.Wall)

                # 偶数行の偶数列を壁にする
                if y % 2 == 0 and x % 2 == 0:
                    field.set_tile(x, y, TileType.Wall)

    def _knockstick(self, field: Field):
        """棒を倒す

        Args:
            field (Field): フィールド
        """

        # 各壁について
        for wy in range(2, field.height - 1, 2):
            for wx in range(2, field.width - 1, 2):
                # 有効な方向のリスト
                available_dirs = [0, 1, 2, 3]

                # 最上行以外なら上は選ばない
                if wy != 2:
                    available_dirs.remove(3)

                # 有効な方向から座標を生成し、壁があるなら方向から取り除く
                for dir in available_dirs:
                    dx, dy = self._id_to_dir(dir)
                    if field.get_tile(wx + dx, wy + dy) == TileType.Wall:
                        available_dirs.remove(dir)

                # 残りがなければ、この壁では何もしない
                if len(available_dirs) == 0:
                    continue

                # 選んで壁にする
                knock_dir = random.choice(available_dirs)
                knock_dx, knock_dy = self._id_to_dir(knock_dir)
                field.set_tile(wx + knock_dx, wy + knock_dy, TileType.Wall)

    def _id_to_dir(self, dir: int) -> Tuple[int, int]:
        """方向IDからdx, dyを生成

        Args:
            dir (int): 方向ID (0, 1, 2, 3)

        Returns:
            Tuple[int, int]: 座標

        Note:
            0, 1, 2, 3がそれぞれ 右, 下, 左, 上 に対応します。
        """
        # dd  x  y  D
        # -----------
        # 00  1  0  R
        # 01  0  1  D
        # 10 -1  0  L
        # 11  0 -1  U
        base = 1 - (dir >> 1) * 2
        return (base, 0) if (dir & 0x01) == 0 else (0, base)
