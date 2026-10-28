# Extraction instructions

You are extracting structured data from posts of the Telegram channel **"Калькасыз қазақ тілі"** (t.me/kalkastop) by **Nazgul Kozhabek (Назгүл Қожабек)**, a Kazakh linguist. The channel corrects *calques*: Kazakh phrases that copy Russian words, word order or grammar instead of using natural Kazakh.

The data will become an open-source skill that teaches AI agents to write natural, calque-free Kazakh. Accuracy matters more than volume. Never invent corrections the author did not give.

## Input

A JSONL batch file. Each line is `{"id": <post id>, "text": "<post text>"}`. Read the whole file in chunks.

Common post formats:
- `❌ wrong` / `⁉️ Russian source` / `✅ correct` (sometimes several pairs in one post, sometimes ❌ only)
- `Қате: ... Несі қате: ... Неге қате: ... Дұрысы: ...` (longer explanations)
- Free-form explanations, comments on signs, news, ads or official texts
- Off-topic posts: reactions, jokes, announcements, polls, sarcasm without a lesson. Skip these.

## Output

Write a JSONL file (one JSON object per line, UTF-8, `ensure_ascii=False` style, real Cyrillic, not \u escapes). Use exactly these fields:

```json
{"post": 162,
 "kind": "pair",
 "wrong": "жауапкершілікке тартылатын болады",
 "russian": "будут привлечены к ответственности",
 "correct": ["жауапкершілікке тартылады"],
 "category": "grammar",
 "rule": "Russian future 'будут + participle' is copied as '-атын болады'; in Kazakh the plain future/present form is enough. '-атын бол-' is needed only in past tense and conditional mood.",
 "confidence": "high"}
```

Field rules:
- `post`: the post id (integer).
- `kind`:
  - `"pair"`: one concrete wrong→correct phrase.
  - `"rule"`: a general pattern or principle explained in the post (it may also have examples). Put up to 4 illustrative examples in an extra field `"examples": [{"wrong": "...", "correct": "..."}]`.
  - One post can produce several entries (several pairs, or a rule plus pairs).
- `wrong`: the calque, copied verbatim from the post. Use `""` if the post gives only a correct form.
- `russian`: the Russian source the author names, or the obvious Russian original if it is unambiguous. Otherwise use `""`.
- `correct`: list of correct forms **as given by the author**, verbatim. Fix capitals used only for emphasis (e.g. `үстемЕақы` → `үстемеақы`), and add a `"note"` saying which letter was stressed.
  - If the author gives no correct form (❌ only), leave the list empty and set `"confidence": "low"`.
  - You may add your own suggestion in a separate field `"suggested": "..."`. Never put it in `correct`.
- `category`, exactly one of:
  - `lexical`: wrong word choice or a word-for-word translated term
  - `phrase`: a multi-word expression copied from Russian
  - `grammar`: case, possessive, tense or verb-form patterns copied from Russian
  - `word-order`: sentence structure or order copied from Russian
  - `bureaucratic`: officialese and clichés from Russian канцелярит
  - `spelling`: orthography or hyphenation, not a calque but a common error
  - `style`: other naturalness or stylistic issues
- `rule`: 1–2 sentences in **English** explaining *why* it is wrong and the general pattern. Base it on the author's explanation. Keep Kazakh and Russian words in Cyrillic. If the post has no explanation, give a brief, careful explanation. Do not overclaim.
- `confidence`:
  - `high`: the author clearly states both wrong and correct.
  - `medium`: you had to interpret the format or context.
  - `low`: the correction is missing, or the post is ambiguous or sarcastic.

Skip a post entirely if it contains no linguistic lesson. Do not output anything for skipped posts.

## Finish

After writing the file, validate it with:
`python3 -c "import json,sys; [json.loads(l) for l in open(sys.argv[1])]; print('ok')" <output file>`

Then reply briefly:
- number of entries
- number of posts used and posts skipped
- 3–5 recurring patterns you noticed in this batch (useful for writing the skill's core rules)
- anything odd
