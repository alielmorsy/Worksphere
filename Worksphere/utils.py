import json


def check_parameters(fields=None):
    def wrap(func):
        def wrapper(*args, **kwargs):
            request = args[1]
            if request is not None:
                check_body_internal(request.body)
            func(*args, **kwargs)

        return wrapper

    def check_body_internal(body):
        if type(body) == bytes:
            body = body.decode("UTF-8")
        body = json.load(body)
        for field in fields:

            if field not in body:
                raise FieldError("Cannot Find Field %s" % field)

    return wrap


class FieldError(Exception):
    pass


if __name__ == "__main__":
   import  sqlparse
   sqlparse.parse('SELECT %s AS "a" FROM "userAuth_user" WHERE "userAuth_user"."username" = %s LIMIT 1')