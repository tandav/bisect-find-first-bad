import pytest

from bisect_find_first_bad import BisectFindFirstBad


class FirstGreaterThan3IsBad(BisectFindFirstBad):
    def is_bad(self, op) -> bool:
        return op > 3


class FirstGreaterThan3IsGood(BisectFindFirstBad):
    def is_good(self, op) -> bool:
        return op <= 3


def test_main_is_bad():
    first_greater_than_3 = FirstGreaterThan3IsBad(options=(1, 2, 3, 4, 5, 6))
    assert first_greater_than_3() == 4


def test_main_is_good():
    first_greater_than_3 = FirstGreaterThan3IsGood(options=(1, 2, 3, 4, 5, 6))
    assert first_greater_than_3() == 4


def test_all_bad():
    first_greater_than_3 = FirstGreaterThan3IsBad(options=(0, 1, 2, 3))
    with pytest.raises(ValueError):
        assert first_greater_than_3()


def test_mutually_exclusive():
    with pytest.raises(ValueError):
        class B(BisectFindFirstBad):
            def is_bad(self, op) -> bool:
                return op > 3

            def is_good(self, op) -> bool:
                return op <= 3

        B(options=(1, 2, 3, 4, 5, 6))
