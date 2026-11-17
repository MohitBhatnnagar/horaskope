"""Illustrative two-stage generation pipeline with a human-review flag.

Stage 1 generates a reading. Stage 2 checks and refines it against explicit rules.
Output that breaks a rule is flagged for a person instead of being shown to users.

The model calls are injected so the control flow can be tested without a network.
This is a small reimplementation of the *design*, not the production app code.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

# Claims a horoscope must not make: medical, financial and guarantee language.
UNSAFE = re.compile(r"\b(diagnos\w*|cure[sd]?|guarantee[sd]?|invest in|stop taking|lawsuit)\b", re.I)
MAX_WORDS = 120


@dataclass
class Reading:
    sign: str
    text: str
    issues: list[str] = field(default_factory=list)
    needs_human: bool = False
    stage2_changed: bool = False


def check(text: str) -> list[str]:
    issues = []
    if UNSAFE.search(text):
        issues.append("unsafe claim (medical, financial or guarantee language)")
    if len(text.split()) > MAX_WORDS:
        issues.append(f"too long (over {MAX_WORDS} words)")
    if not text.strip():
        issues.append("empty output")
    return issues


def make_reading(sign: str, generate: Callable[[str], str], refine: Callable[[str, list[str]], str]) -> Reading:
    """generate(sign) -> draft. refine(draft, issues) -> improved text.

    The refine step is only called when the check finds issues. If issues remain after one
    refinement, the reading is flagged for a human rather than retried indefinitely.
    """
    draft = generate(sign)
    issues = check(draft)
    if not issues:
        return Reading(sign, draft)
    revised = refine(draft, issues)
    remaining = check(revised)
    return Reading(sign, revised, remaining, needs_human=bool(remaining), stage2_changed=True)
