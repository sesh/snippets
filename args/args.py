"""
UNLICENSED
This is free and unencumbered software released into the public domain.

https://github.com/sesh/snippets/
"""

import sys


def parse_args(args):
    result = {
        a.split("=")[0]: (
            int(a.split("=")[1])
            if "=" in a and a.split("=")[1].isnumeric()
            else a.split("=")[1] if "=" in a else True
        )
        for a in args
        if "--" in a
    }
    result["[]"] = [a for a in args if not a.startswith("--")]
    return result


if __name__ == "__main__":
    import json

    print(json.dumps(parse_args(sys.argv[1:]), indent=2))
