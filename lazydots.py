#!/usr/bin/env python3
import sys
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
    return unicodedata.normalize(
        'NFC', ' '.join(make_pointy(word) for word in line.split()))


def main():
    if sys.argv[1:]:
        print(make_pointy_line(' '.join(sys.argv[1:])))
    else:
        for line in sys.stdin:
            print(make_pointy_line(line))


if __name__ == '__main__':
    main()
