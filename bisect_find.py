import bisect
import subprocess
import abc
from typing import Any


class color:
    RED       = lambda s: '\033[31m' + str(s) + '\033[0m'
    GREEN     = lambda s: '\033[32m' + str(s) + '\033[0m'


class BisectFind(abc.ABC):
    def __init__(self, options: tuple[Any, ...]):
        self.options = options

    def is_bad(self, op: Any) -> bool:
        """
        False/0 means good/old
        True/1 means bad/new
        """
        print(op, 'start')
        if op not in self.options:
            raise KeyError(f'{op}: unknown option')
        is_bad = self._is_bad(op)
        if is_bad:
            print(color.RED(f'{op}: BAD'))
        else:
            print(color.GREEN(f'{op}: GREEN'))
        return is_bad

    @abc.abstractmethod
    def _is_bad(sel, op: Any) -> bool: ...

    def find_first_bad(self):
        """
        https://docs.python.org/3/library/bisect.html#searching-sorted-lists
        Locate the leftmost value exactly equal to x
        """
        a = self.options
        x = True  # True means bad
        i = bisect.bisect_left(a, x, key=self.is_bad)
        if i != len(a) and self.is_bad(a[i]) == x:
            print('=' * 100)
            print(f'first bad option is: {a[i]}')
            return a[i]
        raise ValueError


class FindVersion(BisectFind):
    def _is_bad(sel, op: Any) -> bool:
        """some example is_bad
        you can subclass Find and write your own setup and check is bad implementation
        """

        # kinda setup
        with open('some_file.txt', 'w') as f:
            f.write(str(op))
        v = int(subprocess.check_output('cat some_file.txt'.split(), text=True).strip())

        # check is_bad
        return v > 3


if __name__ == '__main__':
    fv = FindVersion(options = (1, 2, 3, 4, 5, 6))
    # print(fv.is_bad(2))
    print(fv.find_first_bad())
