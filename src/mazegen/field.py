#
# フィールド
#
from enum import Enum, auto
from typing import Any, Generator, List

from .position import Position


class TileType(Enum):
    """タイルタイプ"""

    Wall = auto()
    """壁"""

    Aisle = auto()
    """通路"""

    def __str__(self) -> str:
        match self:
            case TileType.Wall:
                return "█"

            case TileType.Aisle:
                return " "

            case _:
                return "?"


class Field:
    """迷路のフィールド"""

    def __init__(self, width: int, height: int) -> None:
        """幅と高さを指定して迷路のフィールドを生成

        Args:
            width (int): 横幅
            height (int): 縦幅

        Raises:
            ValueError: パラメータがフィールド生成条件を満たさない場合

        Note:
            各パラメータは5以上の奇数でなければなりません。
        """

        # 5以上?
        if width < 5 or height < 5:
            raise ValueError("parameter width and height must be 5 or more")

        # 偶数?
        if width % 2 == 0 or height % 2 == 0:
            raise ValueError("parameter width and height must be an odd number")

        # フィールド生成
        self._width = width
        self._height = height
        self._field: List[TileType] = [TileType.Aisle] * (width * height)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def get_tile(self, at: Position) -> TileType:
        """指定座標のタイル種別を返す

        Args:
            at (Position): 座標

        Returns:
            TileType: 指定座標のタイル種別
        """
        if self._is_valid_pos(at):
            return TileType.Wall

        return self._field[at.y * self._width + at.x]

    def set_tile(self, at: Position, tiletype: TileType):
        """指定座標のタイル種別を設定する

        Args:
            at (Position): 座標
            tiletype (TileType): 設定する値

        Raises:
            ValueError: 範囲外の座標が渡された場合
        """
        if self._is_valid_pos(at):
            raise ValueError(f"index out of range (field size:{self._width}x{self._height}, but specified {at})")

        self._field[at.y * self._width + at.x] = tiletype

    def _is_valid_pos(self, at: Position) -> bool:
        return at.x < 0 or at.y < 0 or at.x >= self._width or at.y >= self._height

    def fetch_cells(self) -> Generator[tuple[Position, TileType], Any, None]:
        """全セルを走査するジェネレータを返す

        Yields:
            Generator[tuple[Position, TileType], Any, None]: セル走査ジェネレータ
        """
        for index, tile in enumerate(self._field):
            x, y = (index % self.width, index // self.width)
            pos = Position(x, y)
            yield (pos, tile)

    def dump(self) -> str:
        """フィールドの構造をダンプする

        Returns:
            str: _description_
        """
        str_reprs = []
        for y in range(self._height):
            line_tile = self._field[y * self._width : (y + 1) * self._width]
            line_str = "".join([str(t) for t in line_tile])
            str_reprs.append(line_str)
        return "\n".join(str_reprs)
