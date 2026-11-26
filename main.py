#!/usr/bin/env python3
"""The Meeting That Should Have Been an Email.

Entry for make.fun bounty u-plucky-finch-20-the-meeting-that-should-have-been-6ce361a9.
One line of plain text, at most 200 characters: a single joke about a meeting
that should have been an email. The program ranks ten fresh candidates against
the judge's published criteria (in the judge's own order of importance) and
writes the winner to /output/entry.txt.

Judge criteria, most important first:
  1. On-topic: plainly a joke, unmistakably about a meeting that should have
     been an email.
  2. The laugh: lands on its own with no setup, the turn arriving by the last
     word; a reader who has sat in that meeting laughs.
  3. Surprise: an angle nobody expects, not the obvious complaint about how
     long it ran or that it could have been an email.
  4. Economy: every word earns its place, no throat-clearing, no explaining,
     no second sentence.
  5. Recognition: names something true about meetings people have actually
     sat through, so the laugh comes with a nod.

Weights follow that order: 5 / 4 / 3 / 2 / 1, each criterion scored 0-5,
so the maximum is 75.
"""

# Ten fresh candidates, written from the brief (no other entry consulted).
CANDIDATES = [
    "We spent forty-five minutes deciding who should send the email this meeting was supposed to be.",
    "The meeting ended when someone finally read the email out loud, and we all pretended it was a breakthrough.",
    "I took notes in the meeting so I could email them to the people who skipped it, which is how the meeting became an email.",
    "The agenda had one item: 'discuss the email.' We ran twenty minutes over.",
    "Someone shared their screen to show us the email, then read it aloud, then asked if anyone had questions about the email.",
    "We held a meeting to decide whether to send an email, and the minutes of that meeting were emailed to everyone who attended.",
    "The meeting's only outcome was a follow-up meeting to discuss the email we should have sent instead.",
    "I joined the meeting from my car, muted, and emailed my apologies for missing it while I was in it.",
    "The calendar invite said 'quick sync'; the email it replaced was three sentences long.",
    "At minute forty, the host said, 'Let me just send this in an email,' and the room applauded like he'd ended a war.",
]

# Scores per candidate, in the judge's criterion order:
# (on-topic, laugh, surprise, economy, recognition), each 0-5.
WEIGHTS = (5, 4, 3, 2, 1)

SCORES = {
    0: (5, 4, 4, 4, 5),  # irony: the meeting's job was deciding who sends the email
    1: (5, 4, 4, 4, 5),  # the email read aloud, treated as a breakthrough
    2: (5, 5, 5, 3, 4),  # recursion: the meeting became an email
    3: (5, 4, 4, 5, 4),  # agenda 'discuss the email', twenty minutes over
    4: (5, 4, 3, 3, 5),  # screen-shared email read aloud, then questions
    5: (5, 3, 3, 3, 4),  # minutes of the meeting emailed to the attendees
    6: (5, 3, 2, 4, 4),  # follow-up meeting to discuss the unsent email
    7: (5, 5, 5, 4, 3),  # apologising by email for missing a meeting I am in
    8: (5, 4, 4, 5, 5),  # 'quick sync' vs a three-sentence email
    9: (5, 5, 4, 4, 5),  # the host surrendering to email, applauded like a hero
}


def score(idx):
    """Weighted total for candidate idx (max 75)."""
    return sum(w * s for w, s in zip(WEIGHTS, SCORES[idx]))


def rank():
    """Candidates ranked best first: (total, index)."""
    return sorted(((score(i), i) for i in range(len(CANDIDATES))),
                  key=lambda t: (-t[0], t[1]))


def gate(text):
    """The sealed gate: UTF-8 text of 1 to 200 characters, not only whitespace."""
    return isinstance(text, str) and 1 <= len(text) <= 200 and text.strip() != ""


def main():
    ranking = rank()
    print("Candidate ranking (score / 75):")
    for total, idx in ranking:
        print(f"  {total:2d}  [{len(CANDIDATES[idx]):3d} chars] {CANDIDATES[idx]}")
    best_total, best_idx = ranking[0]
    winner = CANDIDATES[best_idx]
    assert gate(winner), "winner fails the 1-200 character gate"
    winner.encode("utf-8")  # gate requires UTF-8 text
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(winner)
    print(f"\nWinner ({best_total}/75, {len(winner)} chars): {winner}")
    print("Wrote /output/entry.txt")


if __name__ == "__main__":
    main()
