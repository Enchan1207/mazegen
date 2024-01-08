#
# 迷路自動生成
#
import sys

from mazegen.configure.stick_knock import StickKnockConfigurator
from mazegen.field import Field


def main() -> int:
    # フィールドを初期化
    field = Field(71, 23)

    # シードを渡して棒倒し構成器を初期化
    seed = "ラブライブ!虹ヶ咲学園スクールアイドル同好会"
    configurator = StickKnockConfigurator(seed)

    # 生成
    configurator.configure(field)

    # フィールドをテキストにダンプ
    print("Field:")
    print(field.dump())
    return 0


if __name__ == "__main__":
    sys.exit(main())
