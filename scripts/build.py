#!/usr/bin/env python3
"""Build the question bank and embed it in index.html.

Source files: data/ch01.json ... data/ch10.json (one per Discover Canada chapter).

Authoring format for each question:
  t   type: "s" (single answer), "tf" (true/false), "m" (choose TWO, not used
      in the Canadian test but still supported)
  tp  topic label
  q   question text (for "tf", the statement only)
  a   correct answer: string ("s"), list of two strings ("m"), true/false ("tf")
  w   wrong answers: three for "s", two for "m", none for "tf"
  k   1 if it is a key question (optional)
  e   explanation

Outputs:
  questions.json            full bank with shuffled options and answer indexes
  index.html                the bank is written between the QUESTIONS markers

Usage: python3 scripts/build.py          build
       python3 scripts/build.py --check  fail if outputs are out of date
"""
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_JSON = ROOT / "questions.json"
INDEX = ROOT / "index.html"
MARKER = re.compile(r"(/\*QUESTIONS_START\*/).*?(/\*QUESTIONS_END\*/)", re.S)
TF_PREFIX = "Is the statement below TRUE or FALSE? "


def fail(msg):
    sys.exit(f"error: {msg}")


def build_question(qid, chapter, src):
    t = src.get("t")
    where = f"chapter {chapter}, question {qid} ({src.get('q', '')[:50]!r})"
    for field in ("tp", "q", "e"):
        if not str(src.get(field, "")).strip():
            fail(f"{where}: missing '{field}'")
    rng = random.Random(f"{chapter}:{src['q']}:{src['a']}")

    if t == "tf":
        if not isinstance(src.get("a"), bool) or src.get("w"):
            fail(f"{where}: true/false needs a boolean 'a' and no 'w'")
        options = ["True", "False"]
        answer = [0 if src["a"] else 1]
        text = TF_PREFIX + src["q"]
    elif t in ("s", "m"):
        correct = [src["a"]] if t == "s" else src["a"]
        wrong = src.get("w", [])
        need = (1, 3) if t == "s" else (2, 2)
        if not isinstance(correct, list) or (len(correct), len(wrong)) != need:
            fail(f"{where}: '{t}' needs {need[0]} correct and {need[1]} wrong answers")
        options = correct + wrong
        if len(set(o.strip().lower() for o in options)) != 4:
            fail(f"{where}: duplicate options")
        rng.shuffle(options)
        answer = sorted(options.index(c) for c in correct)
        text = src["q"]
    else:
        fail(f"{where}: unknown type {t!r}")

    return {
        "id": qid,
        "chapter": chapter,
        "topic": src["tp"],
        "type": {"s": "single", "m": "multi", "tf": "truefalse"}[t],
        "q": text,
        "options": options,
        "answer": answer,
        "key": bool(src.get("k")),
        "explanation": src["e"],
    }


def build():
    chapters, questions, seen = [], [], set()
    for path in sorted(DATA.glob("ch*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        chapters.append({"chapter": doc["chapter"], "title": doc["title"]})
        for src in doc["questions"]:
            # the same wording may be reused with different answers (as in the real test)
            norm = (src["q"].strip().lower(), str(src.get("a")).lower())
            if norm in seen:
                fail(f"duplicate question: {src['q']!r}")
            seen.add(norm)
            questions.append(build_question(len(questions) + 1, doc["chapter"], src))
    return {"chapters": chapters, "questions": questions}


def main():
    bank = build()
    json_text = json.dumps(bank, ensure_ascii=False, indent=1) + "\n"
    inline = json.dumps(bank, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = INDEX.read_text(encoding="utf-8")
    if not MARKER.search(html):
        fail("QUESTIONS markers not found in index.html")
    new_html = MARKER.sub(lambda m: f"{m.group(1)}{inline}{m.group(2)}", html, count=1)

    if "--check" in sys.argv:
        stale = [p.name for p, new in ((OUT_JSON, json_text), (INDEX, new_html))
                 if not p.exists() or p.read_text(encoding="utf-8") != new]
        if stale:
            fail(f"out of date: {', '.join(stale)} (run python3 scripts/build.py)")
    else:
        OUT_JSON.write_text(json_text, encoding="utf-8")
        INDEX.write_text(new_html, encoding="utf-8")

    qs = bank["questions"]
    counts = {t: sum(q["type"] == t for q in qs) for t in ("single", "multi", "truefalse")}
    print(f"{len(qs)} questions ({counts}), {sum(q['key'] for q in qs)} key")


if __name__ == "__main__":
    main()
