from typing import Annotated


def double(x: Annotated[int, (0, 100)]) -> int:
    return 2 * x


result = double(2)
print(result)
