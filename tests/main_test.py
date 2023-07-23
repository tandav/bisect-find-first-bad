import pytest

from bisectlib import Bisect


class FirstGreaterThan3IsBad(Bisect):
    def is_bad(self, op) -> bool:
        return op > 3


class FirstGreaterThan3IsGood(Bisect):
    def is_good(self, op) -> bool:
        return op <= 3


@pytest.mark.parametrize(
    'cls, options, sort_order', [
        (FirstGreaterThan3IsBad, (1, 2, 3, 4, 5, 6), 'good-bad'),
        (FirstGreaterThan3IsGood, (6, 5, 4, 3, 2, 1), 'bad-good'),
    ],
)
def test_is_bad(cls, options, sort_order):
    assert cls(options, sort_order)() == 4


def test_all_bad():
    first_greater_than_3 = FirstGreaterThan3IsBad(options=(0, 1, 2, 3))
    with pytest.raises(ValueError):
        assert first_greater_than_3()


def test_mutually_exclusive():
    with pytest.raises(ValueError):
        class B(Bisect):
            def is_bad(self, op) -> bool:
                return op > 3

            def is_good(self, op) -> bool:
                return op <= 3

        B(options=(1, 2, 3, 4, 5, 6))
