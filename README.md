# bisectlib
array bisection algorithm helper

## install
```
pip install bisectlib
```

## usage
you should subclass from `Bisect` and implement 1 method `is_bad` or `is_good`.
This method should return `True/False` which indicates is option good or bad.
When instantiating your class you should provide a sequence of options to check. They should be sorted by `is_bad`. By default, left side of options are considered good options and on the right are bad ones. (You can change this by passing `sort_order='bad-good'` argument)


## simple example
```py
from bisectlib import Bisect

class FirstGreaterThan3(Bisect):
    def is_bad(self, op) -> bool:
        return op > 3

# or you can use is_good:
class FirstGreaterThan3(Bisect):
    def is_good(self, op) -> bool:
        return op <= 3

first_greater_than_3 = FirstGreaterThan3(options = (1, 2, 3, 4, 5, 6))
```

```py
>>> first_greater_than_3.is_bad(2)
False

>>> first_greater_than_3.is_bad(5)
True

>>> first_greater_than_3()
4 start
4: BAD
2 start
2: GOOD
3 start
3: GOOD
====================================================================================================
first bad option is: 4
4
```


## more complex example - find first bad version of poetry dependency
```py
import subprocess
from bisectlib import Bisect

class FirstBadDependencyVersion(Bisect):
    def is_bad(self, op) -> bool:
        # kinda setup
        subprocess.check_call(f'git checkout HEAD -- poetry.lock pyproject.toml && poetry add "my_library=={op}"', shell=True)

        # check is_bad
        return bool(subprocess.run('make test', shell=True).returncode)

first_bad_dependency_version = FirstBadDependencyVersion(options='''\
v0.0.1
v0.0.2
v0.0.3
v0.1.0
v0.1.1
v0.1.2
v0.2.0
v0.2.1
'''.splitlines())
```

```py
>>> first_bad_dependency_version()
v0.1.1 start
v0.1.1: GOOD
v0.2.0 start
v0.2.0: BAD
v0.1.2 start
v0.1.2: BAD
====================================================================================================
first bad option is: v0.1.2
'v0.1.2'
```
