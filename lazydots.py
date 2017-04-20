import unicodedata
from pathlib import Path
import functools
import deromanize
import yaml

CONFIG_FILE = Path(__file__).parent/'data.yml'
CACHE_PATH = Path().home()/'.cache'/'lzdcache'
CACHE_PATH.parent.mkdir(exist_ok=True)
with CONFIG_FILE.open(encoding='utf-8') as config:
    keys = deromanize.cached_keys(yaml.safe_load, config, CACHE_PATH)


def get_top(func):
    @functools.wraps(func)
    def wrapped(word):
        return str(func(word)[0])
    return wrapped


@get_top
@keys.processor
def make_pointy(keys, word):
    end, remainder = keys['end'].getpart(word)
    if remainder:
        try:
            front, remainder = keys['front'].getpart(remainder)
        except KeyError:
            return no_end(keys, word)
    else:
        return no_end(keys, word)

    if remainder:
        middle = keys['mid'].getallparts(remainder).add()
        return (front + middle + end)
    else:
        return (front + end)


def no_end(keys, word):
        front, remainder = keys['front'].getpart(word)
        if remainder:
            end, remainder = keys['end'].getpart(remainder)
            if remainder:
                middle = keys['mid'].getallparts(remainder).add()
                return (front + middle + end)
            else:
                return (front + end)
        else:
            return (front)


def make_pointy_line(line):
    if line == '':
        return ''
    return ' '.join(make_pointy(word) for word in line.split())


def make_pointy_text(text):
    return '\n'.join(map(make_pointy_line, text.splitlines()))


def read_text():
    import sys
    import argparse

    ap = argparse.ArgumentParser()
    add = ap.add_argument
    add('string', nargs='*', default=sys.stdin,
        help='ascii text to make pointy')
    add('-n', '--normalize', action='store_true',
        help='apply canonical normalization')
    args = ap.parse_args()

    pointy = '\n'.join(make_pointy_line(l) for l in args.string)
    if args.normalize:
        pointy = unicodedata.normalize('NFC', pointy)

    if sys.stdout.isatty():
        print(pointy)
    else:
        print(pointy, end='')
