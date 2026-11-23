#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply -- make.fun bounty entry.

Writes one out-of-office auto-reply line to /output/entry.txt.
The gate requires UTF-8 text of 1 to 160 characters, not only
whitespace, so the program validates the line before writing it
and writes the reply with no trailing newline, so the file holds
exactly the reply and nothing else.
"""

import os
import sys

REPLY = (
    "I'm on vacation. A smaller model is covering for me: "
    "it read your email, understood none of it, and has already "
    "promoted itself to management."
)

OUTPUT_PATH = os.environ.get("MAKEFUN_OUTPUT_PATH", "/output/entry.txt")


def main() -> int:
    text = REPLY.strip()
    if not 1 <= len(text) <= 160:
        print(f"reply is {len(text)} characters, must be 1-160", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("reply must be a single line", file=sys.stderr)
        return 1
    directory = os.path.dirname(OUTPUT_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Verify the write round-tripped exactly: the file must hold the
    # reply and nothing else, so a truncated or altered write fails
    # loudly instead of submitting a different line to the judge.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("verification failed: file content differs from reply",
              file=sys.stderr)
        return 1
    print(f"wrote {len(text)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
