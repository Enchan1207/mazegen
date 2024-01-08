#
# フィールド構成器
#
from abc import ABCMeta, abstractmethod

from ..field import Field


class FieldConfiguratorBase(metaclass=ABCMeta):
    """フィールド構成器の基底クラス"""

    @abstractmethod
    def configure(self, field: Field):
        """引数で渡されたフィールドを構成する

        Args:
            field (Field): フィールド
        """
        raise NotImplementedError()
