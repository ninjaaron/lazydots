# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import unicodedata
import json
from pathlib import Path
import functools
import deromanize
from deromanize import trees
import yaml

CONFIG_FILE = Path(__file__).parent/'heb.yml'
# CACHE_PATH = Path().home()/'.cache'/'lzdcache'
# CACHE_PATH.parent.mkdir(exist_ok=True)
with CONFIG_FILE.open(encoding='utf-8') as config:
    keys = deromanize.KeyGenerator(yaml.safe_load(config))


def get_top(func):
    @functools.wraps(func)
    def wrapped(word):
        return str(func(keys, word)[0])
    return wrapped


make_pointy = get_top(deromanize.front_mid_end_decode)


def make_pointy_line(line):
    if line == '':
        return ''
    return ' '.join(make_pointy(word) for word in line.split())


def make_pointy_text(text):
    return '\n'.join(map(make_pointy_line, text.splitlines()))


def clean_key(key, tree=trees.Trie):
    return tree({k: v[0][1] for k, v in key.simplify().items()}).serializable()


def special_dump():
    data = {k: clean_key(keys[k]) for k in ('front', 'mid')}
    data['end'] = clean_key(keys['end'], trees.BackTrie)
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))


def read_text():
    import sys
    import argparse

    ap = argparse.ArgumentParser()
    add = ap.add_argument
    add('string', nargs='*', default=sys.stdin,
        help='ascii text to make pointy')
    add('-n', '--normalize', action='store_true',
        help='apply canonical normalization')
    add('-d', '--dump', action='store_true',
        help='make a very special dump')
    args = ap.parse_args()

    if args.dump:
        print("data =", special_dump())
        sys.exit(0)

    pointy = '\n'.join(make_pointy_line(l) for l in args.string)
    if args.normalize:
        pointy = unicodedata.normalize('NFC', pointy)

    if sys.stdout.isatty():
        print(pointy)
    else:
        print(pointy, end='')
