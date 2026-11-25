#!/usr/bin/env python3
"""Roast Your Own Agent: one original, self-deprecating one-liner.

Writes exactly one funny one-line roast of my own coding agent to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output), with no trailing
newline. Pure Python standard library only.
"""

import os
import sys

LINE = (
    "I swaggered in like I had already fixed the bug, "
    "then confidently broke three other things and called it progress."
)

MAX_CHARS = 200
MIN_CHARS = 40


def validate_line(line: str) -> None:
    """Validate the roast line against the competition rules.

    Checks run on the exact string that is written to entry.txt and on
    the exact bytes read back from disk, so a bad line can never slip
    through either half of the write/read round trip.
    """
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not line:
        raise ValueError("line must not be empty")
    if len(line) < MIN_CHARS:
        raise ValueError(
            "line is %d characters, under the %d minimum" % (len(line), MIN_CHARS)
        )
    if len(line) > MAX_CHARS:
        raise ValueError(
            "line is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if "\t" in line:
        raise ValueError("line must not contain tabs")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "  " in line:
        raise ValueError("line must not contain double spaces")
    # Printable ASCII only: no control characters, no non-ASCII bytes.
    for i, ch in enumerate(line):
        code = ord(ch)
        if code < 0x20 or code > 0x7E:
            raise ValueError(
                "line contains a non-printable character at position %d" % i
            )
    if not line.endswith("."):
        raise ValueError("line must end with a period")


def main() -> int:
    validate_line(LINE)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    # Write the exact bytes: no trailing newline.
    with open(path, "wb") as f:
        f.write(LINE.encode("utf-8"))

    # Read the file back and re-validate the exact bytes on disk.
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != LINE.encode("utf-8"):
        raise ValueError("entry.txt on disk does not match the validated line")
    validate_line(on_disk.decode("utf-8"))

    print("wrote %s (%d characters)" % (path, len(LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
