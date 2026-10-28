# Kazakh without calques · Калькасыз қазақ тілі

An agent skill that teaches AI assistants (Claude, Codex, Cursor and others) to write **natural Kazakh** instead of Russian structures dressed in Kazakh words.

> ❌ Туған күніңмен! → ✅ Туған күнің құтты болсын!
> ❌ полиция тарапынан құрықталды → ✅ полиция құрықтаған
> ❌ бару керекпін → ✅ баруым керек

## 🙏 Credits: Назгүл Қожабек

**All the knowledge in this repository comes from linguist [Назгүл Қожабек](https://t.me/kalkastop) (Nazgul Kozhabek) and her Telegram channel [«Калькасыз қазақ тілі»](https://t.me/kalkastop).**

Since 2020 she has published more than 4,000 posts that find, explain and fix calques in everyday Kazakh: in the news, on signs, in ads, in official documents and in speech. This project only collects her corrections into a form AI agents can use. The rules, explanations and examples are hers.

Every entry in this repo links back to her original post. If this skill helps you, **subscribe to her channel: [t.me/kalkastop](https://t.me/kalkastop)**.

Mistakes in the extraction are ours, not hers. Please report them (see [Contributing](#contributing)).

## What's inside

```
skills/kazakh-without-calque/
├── SKILL.md              # Core rules and workflow (English instructions, Kazakh examples)
├── references/           # Full dictionary: 2,700+ ❌ → ✅ entries by category, plus rules
│   ├── grammar.md  lexical.md  phrase.md  bureaucratic.md
│   ├── word-order.md  style.md  spelling.md
│   └── rules.md          # Longer explanations of general patterns
└── scripts/
    └── check_calques.py  # Flags known calques in a text (Python 3, no dependencies)
data/
└── calques.jsonl         # Structured dataset: 3,301 entries, each linked to its source post
```

The instructions are written in English because AI agents follow English meta-instructions most reliably. All rules and examples are in Kazakh.

## Install

### Claude Code

```bash
git clone https://github.com/kosbay/kazakh-language-without-calque.git
cp -r kazakh-language-without-calque/skills/kazakh-without-calque ~/.claude/skills/
```

Claude uses it automatically whenever it writes, translates or edits Kazakh.

### Other tools with Agent Skills support (Codex, Cursor and others)

Copy the `skills/kazakh-without-calque` folder into your tool's skills directory. The folder follows the standard `SKILL.md` format.

### Any agent (`AGENTS.md`, `.cursorrules`, system prompt)

Put the skill folder somewhere in your project and add this to your agent instructions:

```markdown
When writing, translating or editing Kazakh text, follow `path/to/kazakh-without-calque/SKILL.md`.
```

For a chat assistant with no file access, paste the contents of `SKILL.md` into its system prompt or custom instructions. The core rules work without the reference files.

## Check a text yourself

```bash
python3 skills/kazakh-without-calque/scripts/check_calques.py my-text.txt
```

```
line 1: «күніңмен!» — Greeting calque (С днём рождения!). Use 'X құтты болсын!'.
line 3: «жобаның талқылауы» — Known calque. ✅ жобаны талқылау  (https://t.me/kalkastop/403)
```

## How the dataset was built

The channel's public text posts were downloaded, and AI agents turned each post into structured entries. Off-topic posts (ads, announcements, reactions) were skipped. The entries were then checked, de-duplicated and saved to `data/calques.jsonl`, and `references/` was generated from that file. Entries marked low confidence are kept out of the skill; these are mostly posts that mark an error without giving a fix.

Each entry looks like this:

```json
{"post": 162, "kind": "pair", "wrong": "жауапкершілікке тартылатын болады",
 "russian": "будут привлечены к ответственности", "correct": ["жауапкершілікке тартылады"],
 "category": "grammar", "rule": "...", "confidence": "high", "source": "https://t.me/kalkastop/162"}
```

Not yet included: examples that exist only as images in the channel (about 1,000 photos).

## Contributing

- **Found a wrong entry?** Open an issue with the entry and the post link.
- **Low-confidence entries** in `data/calques.jsonl` need a native speaker's review. Many just need the correct form filled in.

## Қазақша

Бұл жоба жасанды интеллект агенттері (Claude, Codex, Cursor т.б.) қазақша жазғанда орысшадан калька жасамауы үшін жасалды.

Ережелер мен мысалдардың бәрі тіл маманы **Назгүл Қожабектің** [«Калькасыз қазақ тілі»](https://t.me/kalkastop) телеграм арнасынан алынды: 2020 жылдан бері жазылған 4 мыңнан астам жазбадан 3 мыңнан астам түзету жиналды. Әр мысал арнадағы түпнұсқа жазбаға сілтеме береді.

Назгүл апайға көп рахмет! Арнаға жазылыңыз: [t.me/kalkastop](https://t.me/kalkastop)

Қате тапсаңыз, issue ашып жазыңыз.

## License

- **Rules, examples and dataset** (`skills/kazakh-without-calque/SKILL.md`, `references/`, `data/`): [CC BY 4.0](LICENSE-DATA). Use them freely, including commercially, but credit the source: *«Калькасыз қазақ тілі», Назгүл Қожабек, https://t.me/kalkastop*.
- **Code** (`check_calques.py`): [MIT](LICENSE).
