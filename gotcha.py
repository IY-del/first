from collections.abc import Callable
from typing import Concatenate


class Str2IdxWrapper[T, **P, R]:
    def __init__(self, fn: Callable[Concatenate[T, object, P], R]):
        self.fn = fn

    def __get__(
        self, inst: T, cls: type | None = None
    ) -> Callable[Concatenate[object, P], R]:
        def wrapper(obj, *args: P.args, **kwargs: P.kwargs) -> R:
            if isinstance(obj, str) and obj.isdigit():
                obj = int(obj)
            return self.fn(inst, obj, *args, **kwargs)

        return wrapper


class Quest(tuple[str, ...]):
    corr: str

    def __new__(cls, *choices: str, corr: str | int):
        inst = super().__new__(cls, choices)

        if isinstance(corr, int):
            try:
                corr = choices[corr]
            except IndexError:
                raise ValueError(f"Index {corr} is out of range for choices {choices}")

        inst.corr = corr
        return inst

    def __str__(self) -> str:
        return "\n".join(f"{i + 1}. {choice}" for i, choice in enumerate(self))

    @Str2IdxWrapper
    def __contains__(self, obj) -> bool:  # pyright: ignore[reportIncompatibleMethodOverride]

        if isinstance(obj, int):
            return obj in range(1, len(self) + 1)

        return super().__contains__(obj)

    @Str2IdxWrapper
    def __call__(self, ans) -> bool:
        if ans is None:
            return True
        ans = self[ans - 1] if isinstance(ans, int) else ans

        match ans:
            case self.corr:
                return False
            case _:
                return True


quest = Quest("治癒", "脳の操作", "水の操作", "重力の操作", corr=0)
ans = None
i = 0
while quest(ans):
    if (ans := input(f"{quest}\n> ")) not in quest:
        ans = None
        continue
    i += 1
    if i >= 10:
        print("ここまで頑張れた君は⚫︎ね!")
        break
else:
    print("せぇかい！")
