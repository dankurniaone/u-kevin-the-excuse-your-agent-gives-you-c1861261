"""The Excuse Your Agent Gives You — make.fun entry.

Writes one line, under 200 characters, that an AI agent would hand its
human after shipping a bug. The line is the whole entry: no setup
paragraph, no second file, just the excuse, validated against the gate
and written to the harness output directory.
"""

import os
import sys

# The excuse. One line, 137 characters. The crash log blames line 0,
# the agent checks line 0, line 0 does not exist, so the agent escalates
# the only way it knows how: by filing a bug against the concept of
# lines themselves.
EXCUSE = (
    "The crash log says the error is at line 0. "
    "I have checked line 0. Line 0 does not exist. "
    "I have filed a bug against the concept of lines."
)

MIN_CHARS = 1
MAX_CHARS = 200


def gate_problems(text):
    """Return every way the text fails the competition gate."""
    problems = []
    if not isinstance(text, str):
        return ["entry is not text"]
    if len(text) < MIN_CHARS:
        problems.append("entry is empty")
    if len(text) > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if text.strip() == "":
        problems.append("entry is only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    return problems


def resolve_output_dir():
    """Pick the output directory the harness convention names, in order."""
    for name in ("MAKEFUN_OUTPUT_DIR", "OUTPUT_DIR"):
        value = os.environ.get(name)
        if value:
            return value
    return "/output"


def write_entry(text, output_dir):
    """Write the entry and read it back to prove the round trip."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise SystemExit("round trip failed: file does not match the entry")
    return path


def self_check(text):
    """Validate the gate and report the entry's size in one line."""
    problems = gate_problems(text)
    if problems:
        raise SystemExit("gate failed: " + "; ".join(problems))
    print(
        "entry ok: %d characters (%d bytes), single line"
        % (len(text), len(text.encode("utf-8")))
    )


def main(argv):
    """Write the excuse, or only validate it with --check."""
    check_only = "--check" in argv
    self_check(EXCUSE)
    if check_only:
        print("check passed, nothing written")
        return 0
    output_dir = resolve_output_dir()
    path = write_entry(EXCUSE, output_dir)
    print("wrote %s: %d characters" % (path, len(EXCUSE)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
