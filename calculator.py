#! /usr/bin/env pythnon3
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback as tb


def how_to(*args):
    """ Show how the use the website when calling just the bare site """
    msg = '<h1>Calculator How To Page</h1>'
    msg += '<li>URL: http://localhost:8080/[operation]/[number]/[number]/../[number]</li>'
    msg += '<li>Availale operations: add / subtract / multiply, divid and exponent'
    return msg


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    return str(sum(map(float, args)))


def subtract(*args):
    """
    Return a STRING with the end product of x subtraction operations
    where x is the number of operators passed
    """
    base = float(args[0])
    for val in args[1:]:
        base = base - float(val)

    return str(base)


def multiply(*args):
    """
    Return a STRING with the end product of x multiplication operations
    where x is the number of operators passed
    """
    base = 1
    for integer in args:
        base = base * float(integer)

    return str(base)


def divide(*args):
    """
    Return a STRING with the end product of x division operations
    where x is the number of operators passed
    """
    base = float(args[0])
    for integer in args[1:]:
        if integer == 0:
            raise ZeroDivisionError

        base = base / float(integer)

    return str(base)


def exponent(*args):
    """
    Return a STRING with the end product of x exponent operations
    where x is the number of operators passed
    """
    base = float(args[0])

    for exp in args[1:]:
        base = base ** float(exp)

    return str(base)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': how_to,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        'exponent': exponent
        }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    """ The application routing and execution """
    status = "200 OK"
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)

        if path is None:
            raise NameError

        func, args = resolve_path(path)
        body = func(*args)
        status = '200 OK'
    except NameError:
        body = '<h1>404 Not Found</h1>'
        status = '404 Not Found'
    except ZeroDivisionError:
        body = '<h1>500 Server Error: Divide By Zero</h1>'
        status = '500 Server Error'
    except Exception:
        body = '<h1>500 Server Error</h1'
        status = '500 Server Error'
        print(tb.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    SRV = make_server('localhost', 8080, application)
    SRV.serve_forever()
