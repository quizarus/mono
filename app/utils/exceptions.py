import re

from fastapi import Request, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse


def integrity_error_handler(request: Request, exc: IntegrityError):
    orig_exc = exc.orig.args[0]
    if re.search("insert or update on table .* violates foreign key constraint", orig_exc):
        pattern = r"Key \((\w+)\)=\((\d+)\).*table \"([^']+)\""
        match = re.search(pattern, orig_exc)
        key, value, table = match.group(1), match.group(2), match.group(3)
        return JSONResponse(status_code=404, content={'message': f'Object with "{key}={value}" in "{table}" does not exists'})
    raise exc


exceptions = {
    IntegrityError: integrity_error_handler
}
