from urllib.parse import parse_qs, urlparse


def get_query_param(url: str, param: str) -> str:
    return parse_qs(urlparse(url).query)[param][0]


def send_from(generator, fn):
    r = yield next(generator)
    while True:
        try:
            r = yield generator.send(r)
        except StopIteration as e:
            return fn(e.value)
