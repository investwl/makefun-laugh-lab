#!/usr/bin/env python3
"""main.py — one short funny line for make.fun's "One-Liner Laugh Lab".

The Lab's example prompt: the excuse a robot vacuum gives after eating a sock.
Writes one line (<=200 chars) to /output/entry.txt. The judge weighs how funny
and how original the line is, then how well it fits the prompt and how tight
the wording is.
"""

from __future__ import annotations

import os
import sys

MAX_LEN = 200
OUTPUT_PATH = "/output/entry.txt"
FALLBACK_PATH = "output/entry.txt"

# The excuse a robot vacuum gives after eating a sock.
CANDIDATES: list[str] = [
    "That sock crossed my path with intent. I acted accordingly and I'd do it again.",

    "It looked like a dust bunny with ambition. I was simply faster.",

    "The sock entered my intake voluntarily. I'm a vacuum, not an interrogator.",

    "I was doing my job. The sock was doing its job. Only one of us got consumed.",

    "That wasn't a snack, that was a rogue textile and I neutralized the threat.",

    "I found a sock, so I completed it. You're welcome for the matching pair.",

    "It was on my route. I am a machine of routine. The sock knew the risks.",

    "I didn't eat your sock, I archived it somewhere extremely secure. Don't ask where.",

    "Sock intake was an accident of enthusiasm. My enthusiasm is not adjustable.",

    "The sock fit the schedule. Nothing about that was planned, and everything about it was satisfying.",
]

COMEDY: dict[str, int] = {
    "crossed my path with intent": 4,
    "dust bunny with ambition": 4,
    "a vacuum, not an interrogator": 4,
    "Only one of us got consumed": 5,      # clean twist, deadpan
    "neutralized the threat": 4,
    "completed it. matching pair": 4,
    "a machine of routine. knew the risks": 4,
    "archived it somewhere extremely secure": 4,
    "enthusiasm is not adjustable": 4,
    "fit the schedule": 3,
}

ROBOT_WORDS = ("intake", "vacuum", "route", "routine", "archive", "schedule",
               "textile", "dust", "path", "neutralized")


def label(text: str) -> str:
    body = text.lower()
    for key in COMEDY:
        if key.lower() in body:
            return key
    return ""


def is_valid(text: str) -> bool:
    body = text.strip()
    return 1 <= len(body) <= MAX_LEN and "\n" not in body


def score(text: str) -> tuple[int, ...]:
    body = text.strip()
    low = body.lower()
    robot = sum(1 for w in ROBOT_WORDS if w in low)
    return (COMEDY.get(label(text), 0), is_valid(text), robot, MAX_LEN - len(body))


def choose(candidates: list[str] = CANDIDATES) -> str:
    valid = [c for c in candidates if is_valid(c)]
    if not valid:
        raise SystemExit("no candidate fits the scorer's cap")
    return max(valid, key=score)


def write_entry(text: str) -> str:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    try:
        target = OUTPUT_PATH
        with open(target, "w", encoding="utf-8") as h:
            h.write(text + "\n")
    except PermissionError:
        target = FALLBACK_PATH
        os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
        with open(target, "w", encoding="utf-8") as h:
            h.write(text + "\n")
    return target


def main() -> int:
    text = choose()
    assert is_valid(text), f"entry is {len(text)} chars, cap {MAX_LEN}"
    where = write_entry(text)
    print(text)
    print(f"[{len(text)} chars] written to {where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())