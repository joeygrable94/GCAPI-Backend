import inspect
from functools import partial, wraps
from typing import Any

import asyncer
from typer import Typer


class AsyncTyper(Typer):
    @staticmethod
    def maybe_run_async(decorator: Any, f: Any) -> Any:
        if inspect.iscoroutinefunction(f):

            @wraps(f)
            def runner(*args: Any, **kwargs: Any) -> Any:
                return asyncer.runnify(f)(*args, **kwargs)

            decorator(runner)
        else:
            decorator(f)
        return f

    def callback(self, *args: Any, **kwargs: Any) -> Any:
        decorator = super().callback(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)

    def command(self, *args: Any, **kwargs: Any) -> Any:
        decorator = super().command(*args, **kwargs)
        return partial(self.maybe_run_async, decorator)
