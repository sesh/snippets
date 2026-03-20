"""
UNLICENSED
This is free and unencumbered software released into the public domain.

https://github.com/sesh/snippets/
"""

import hashlib
import json
from pathlib import Path
from thttp import request, Response


def cached_get(url, *args, enable_cache=True, encoding="utf-8", debug=False, **kwargs):
    """
    Uses a .cache directory to cache responses for http requests, cached responses
    will not have the `request` or `cookiejar` parameters set.

    Only caches response with response code <= 299
    """

    m = hashlib.sha256()
    m.update(url.encode())

    for k, v in kwargs.get("params", {}).items():
        m.update(f"{k}{v}".encode())

    for k, v in kwargs.get("headers", {}).items():
        m.update(f"{k}{v}".encode())

    fn = m.hexdigest()

    cache_dir = Path(".cache")
    cache_dir.mkdir(exist_ok=True)
    cached_file = cache_dir / fn

    if enable_cache and cached_file.exists():
        if debug:
            print(f"[cached-get] Reading from cache: {cached_file}")
        with open(cached_file, "r") as f:
            j = json.load(f)
            if debug:
                print(f"[cached-get] Using cached response")
            return Response(
                None,  # request
                j.get("content").encode(encoding),
                j.get("json"),
                j.get("status"),
                j.get("url"),
                j.get("headers"),
                None,  # cookiejar
            )

    if debug:
        print(f"[cached-get] Cache miss for request")
    response = request(url, *args, **kwargs)

    if response.status >= 300:
        return response

    with open(cached_file, "w") as f:
        if debug:
            print(f"[cached-get] Writing {cached_file}")
        f.write(
            json.dumps(
                {
                    "content": response.content.decode(),
                    "json": response.json,
                    "status": response.status,
                    "url": response.url,
                    "headers": response.headers,
                }
            )
        )

    return response


import unittest
import time


class CachedGetTestCase(unittest.TestCase):
    def test_simple_get(self):
        response = cached_get("https://brntn.me", enable_cache=False)
        self.assertIsNotNone(response.request)

        r = cached_get("https://brntn.me")
        self.assertIsNone(r.request)

    def test_param_cached_busting(self):
        response = cached_get(
            "https://brntn.me", params={"t": "000"}, enable_cache=False
        )
        self.assertIsNotNone(response.request)

        r = cached_get("https://brntn.me", params={"t": str(time.time())})
        self.assertIsNotNone(r.request)
