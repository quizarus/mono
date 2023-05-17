import re
from functools import wraps

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def integrity_error_handler(func, *args, **kwargs):
    # @wraps(func)
    async def inner(self, *args, **kwargs):
        try:
            result = await func(self, *args, **kwargs)
            return result
        except IntegrityError as e:
            orig_exc = e.orig.args[0]
            if re.search("insert or update on table .* violates foreign key constraint", orig_exc):
                pattern = r"Key \((\w+)\)=\((\d+)\).*table \"([^']+)\""
                match = re.search(pattern, orig_exc)
                key, value, table = match.group(1), match.group(2), match.group(3)
                raise HTTPException(status_code=404, detail=f'Object with "{key}={value}" in "{table}" does not exists')

        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        return inner

