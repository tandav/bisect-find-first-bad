import pytest
import subprocess
from bisect_find_first_bad import BisectFindFirstBad


class FirstGreaterThan3(BisectFindFirstBad):
    def is_bad(sel, op) -> bool:
        # kinda setup
        with open('some_file.txt', 'w') as f:
            f.write(str(op))
        v = int(subprocess.check_output('cat some_file.txt'.split(), text=True).strip())

        # check is_bad
        return v > 3


def test_main():
    first_greater_than_3 = FirstGreaterThan3(options=(1, 2, 3, 4, 5, 6))
    assert first_greater_than_3() == 4


def test_all_bad():
    first_greater_than_3 = FirstGreaterThan3(options=(0, 1, 2, 3))
    with pytest.raises(ValueError):
        assert first_greater_than_3()
