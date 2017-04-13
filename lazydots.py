#!/usr/bin/env python3
import unicodedata
from pathlib import Path
import deromanize
import yaml

PROFILE = yaml.safe_load((Path(__file__).parent/'data.yml').open())
keys = deromanize.TransKey(PROFILE)


@keys.processor
def make_pointy(keys, word):
    end, remainder = keys['end'].getpart(word)
    try:
        front, remainder = keys['front'].getpart(remainder)
    except KeyError:
        return end
    try:
        middle = keys['mid'].getallparts(remainder).add()
    except KeyError:
        return front + end
    return (front + middle + end)[0].value


def make_pointy_line(line):
    return ' '.join(make_pointy(word) for word in line.split())


def main():
    import sys
    import argparse
    ap = argparse.ArgumentParser()
    add = ap.add_argument
    add('string', nargs='*', default=sys.stdin,
        help='ascii text to make pointy')
    add('-n', '--normalize', action='store_true',
        help='apply canonical normalization')
    args = ap.parse_args()

    for line in args.string:
        pointy = make_pointy_line(line)
        if args.normalize:
            pointy = unicodedata.normalize('NFC', pointy)
        print(pointy)


if __name__ == '__main__':
    main()
