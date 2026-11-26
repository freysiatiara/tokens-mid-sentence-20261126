"""Out of Tokens, Mid-Sentence — make.fun entry.

Writes the funniest one-line error message an AI agent shows when it
runs out of tokens mid-sentence to the entry output file.

Output path resolution (in order):
  1. ENTRY_OUTPUT environment variable
  2. OUTPUT_DIR / MAKEFUN_OUTPUT_DIR joined with "entry.txt"
  3. /output/entry.txt

Stdlib only. No trailing newline in the entry text.
"""

import os

ENTRY = "Error 402: out of tokens. The sentence you were reading has been repossessed for non-payment."
MAX_CHARS = 140


def resolve_output_path() -> str:
    """Resolve where the entry text goes; never fall back to the cwd."""
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    return os.path.join(os.sep, "output", "entry.txt")


def validate(text: str) -> None:
    """Guard: the gate requires 1..140 UTF-8 chars, not only whitespace."""
    assert isinstance(text, str), "entry must be text"
    assert 1 <= len(text) <= MAX_CHARS, (
        "entry must be 1..140 characters, got %d" % len(text)
    )
    assert text.strip(), "entry must not be only whitespace"
    assert "\n" not in text and "\r" not in text, "entry must be one line"


def main() -> None:
    validate(ENTRY)
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
