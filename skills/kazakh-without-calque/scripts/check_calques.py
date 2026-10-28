#!/usr/bin/env python3
"""Flag likely Russian calques in a Kazakh text.

Usage:
    python3 check_calques.py draft.txt
    echo "Туған күніңмен!" | python3 check_calques.py

It checks two things:
  1. Exact matches against the ❌ phrases in references/*.md (from «Калькасыз қазақ тілі»).
  2. A few regex heuristics for the most common calque patterns.
Every hit is a hint to re-check, not a verdict: the same words can be fine in another context.
Exit code: 0 = nothing found, 1 = hints found.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REFS = os.path.join(HERE, "..", "references")

# (pattern, hint) pairs for the most frequent patterns. Keep them narrow to avoid noise.
HEURISTICS = [
    (r"\bболып\s+табыла\w*", "Officialese 'болып табылады' (является). Use a personal ending or a dash: 'Ол – ұстаз', 'Мен мұсылманмын'."),
    (r"\bтарапынан\b", "Passive with an agent (со стороны). Make the agent the subject: 'полиция құрықтаған'."),
    (r"\b(күн|мереке|жыл|жас)\w*(мен|бен|пен)\s*!", "Greeting calque (С днём рождения!). Use 'X құтты болсын!'."),
    (r"\b\d{4}\s+жылдың\b", "Date calque. Use 'жылғы': '2020 жылғы 5 сәуір'."),
    (r"\bкерек(пін|сің|сіз|піз|бін|біз)\b", "Personal ending goes on the verbal noun: 'баруым керек', not 'бару керекпін'."),
    (r"\b\w+(атын|етін|йтын|йтін)\s+бол(ады|амыз|асыз|асың|амын)\b", "Russian future 'будет + verb'. Use the plain form: 'тартылады', 'айтамыз'."),
    (r"\bорын\s+алды\b", "Officialese 'орын алды' (имело место). Use 'болды'."),
    (r"\bүстіміздегі\s+жыл\w*", "Officialese. Use 'биыл'."),
    (r"\bменде\s+(сұрақ|жаңалық|ұсыныс|идея)\w*", "Calque of 'у меня есть'. Use a possessive: 'сұрағым бар'."),
    (r"\b(шара|шешім|душ|дәрі)\w*\s+қабылда\w*", "'принять меры/решение/душ/лекарство' copied as 'қабылдау'. See references (e.g. 'дәрі ішу', 'шешімге келу')."),
    (r"\b\w+(тегі|дегі|тағы|дағы)\s+(жігіт|қыз|адам|әйел|бала|апа|ер\b|кісі)", "Clothing/state in the locative (девушка в платье). Use '-лы' or 'киген/таққан': 'көзілдірік таққан жігіт'."),
    (r"\bжер\s+сілкінісі\s+кезінде\b", "Nominal style. Use a verb: 'жер сілкінгенде'."),
    (r"\b\w+(ның|нің|дың|дің|тың|тің)\s+\w+(уы|уі|уын|уін)\b", "Possible genitive + verbal noun copied from Russian ('жобаның талқылауы'). Consider 'жобаны талқылау'."),
]
HEURISTICS = [(re.compile(p, re.IGNORECASE), h) for p, h in HEURISTICS]


def load_known_calques():
    """Read '- ❌ wrong · ... ✅ correct — rule [#post](url)' lines from the reference files."""
    known = []
    for path in glob.glob(os.path.join(REFS, "*.md")):
        if path.endswith("rules.md"):
            continue
        for line in open(path, encoding="utf-8"):
            if not line.startswith("- ❌ "):
                continue
            body = line[4:]
            wrong = body.split(" · ")[0].split(" — ")[0]
            correct = re.search(r"✅ (.*?)(?: — | \[#)", line)
            src = re.search(r"\[#\d+\]\((\S+)\)", line)
            for variant in re.split(r"\s*(?:/|;|,)\s*", wrong):
                variant = re.sub(r"\([^)]*\)", "", variant).strip(" .!?…\"'«»")
                # Skip very short single words: they cause false hits.
                if (len(variant) >= 6 and " " in variant) or len(variant) >= 9:
                    known.append((variant.lower(), correct.group(1) if correct else "", src.group(1) if src else ""))
    return known


def main():
    text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    low = text.lower()
    hits = []

    seen = set()
    for wrong, correct, src in load_known_calques():
        if wrong in seen:
            continue
        for m in re.finditer(r"(?<!\w)" + re.escape(wrong) + r"(?!\w)", low):
            seen.add(wrong)
            hits.append((m.start(), text[m.start():m.end()], f"Known calque. ✅ {correct}  ({src})"))
            break

    for rx, hint in HEURISTICS:
        for m in rx.finditer(text):
            hits.append((m.start(), m.group(0).strip(), hint))

    if not hits:
        print("No known calques found. (This does not prove the text is calque-free.)")
        return 0
    for pos, frag, hint in sorted(hits):
        line = text.count("\n", 0, pos) + 1
        print(f"line {line}: «{frag}» — {hint}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
