from functools import wraps
from typing import get_type_hints, get_origin, get_args, Annotated


def check_value_range(func):
    @wraps(func)
    def wrapped(x):
        type_hints = get_type_hints(double, include_extras=True)
        x_hint = type_hints.get('x')

        if get_origin(x_hint) is Annotated:
            hint_type, *hint_args = get_args(x_hint)
            low, high = hint_args[0]
            if not (low <= x <= high):
                raise ValueError(
                    f"x falls outside of the boundary between {low} and {high}")

        return func(x)

    return wrapped


@check_value_range
def double(x: Annotated[int, (0, 100)]) -> int:
    return x * 2


try:
    result = double(100)
    print(result)
except ValueError as e:
    print(e)
