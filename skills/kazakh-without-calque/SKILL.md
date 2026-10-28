---
name: kazakh-without-calque
description: Write, translate, edit or review Kazakh text so it reads as natural Kazakh, free of Russian calques (кальки). Use whenever the output is in Kazakh (қазақ тілі), when translating from Russian or English into Kazakh, or when asked to proofread or improve Kazakh text. Based on 3,000+ corrections from the «Калькасыз қазақ тілі» channel by linguist Назгүл Қожабек.
---

# Kazakh without calques

Most Kazakh written today, and most Kazakh produced by AI, is Russian in disguise: Kazakh words arranged in Russian structures. This skill teaches you to write Kazakh the way Kazakh speakers think, not the way a Russian sentence is built.

All examples come from the Telegram channel «Калькасыз қазақ тілі» (https://t.me/kalkastop) by linguist **Назгүл Қожабек**. Numbers like [#2602] link to the source post: `https://t.me/kalkastop/2602`.

## How to work

1. **Write, don't translate.** Even when the source is Russian or English, grasp the meaning first, then express it as a Kazakh speaker would. Don't map the source sentence word by word. Kazakh readers say the instruction "Қатырып қазақша жазып бер" gives better results than "қазақшаға аудар" [#4133].
2. **Prefer verbs to nouns.** Russian officialese piles up nouns (проведение, осуществление, является). Kazakh prefers a verb in the right form.
3. **Self-check before answering.** Re-read your draft against the core rules below. For anything you're unsure about, search the reference files (see "Looking things up").
4. **Run the checker when you can.** `python3 scripts/check_calques.py <file>` flags known calques and common patterns. Treat each hit as a reason to re-check, not as proof of an error.
5. **When editing someone's text**, show each fix as ❌ → ✅ with a one-line reason, unless the user only wants the clean text.

## Core rules

These patterns cover most calques. Each example comes from the channel.

### 1. The instrumental `-мен/-бен/-пен` only marks a tool or a partner
`-мен` is right only for "doing something *with* a tool" (қаламмен жазу, күрекпен жер қазу) or "doing something *together with* someone" (бастықпен әзілдесу). Nearly every other use copies Russian «с» or the творительный падеж [#2602, #1085]. Use a converb, a participle or another case instead.

- ❌ сүтпен шай → ✅ сүтті шай / сүт қосқан шай [#594]
- ❌ күмәнмен қарау → ✅ күмәндана қарау [#1021]
- ❌ Туған күніңмен! → ✅ Туған күнің құтты болсын! [#1461]
- ❌ жаңалықпен бөлісу → ✅ жаңалықты жар салды / айтты [#225]

### 2. No passive with an agent: make the doer the subject
Russian "сделано кем-то" becomes an active Kazakh verb. Drop `тарапынан` and the agent `-мен`.

- ❌ полиция тарапынан құрықталды → ✅ полиция құрықтаған [#107]
- ❌ мемлекет тарапынан қаржыландырылады → ✅ мемлекет қаржыландырып отыр [#1616]

### 3. Don't turn Russian `-ный/-ский` adjectives into `-лық/-лы`
Use a bare noun or a noun with a possessive. `-лы/-ды` means "having/containing X": жұлдызды бала is a child *with a star on it*. Don't stack suffixes either.

- ❌ Еуропалық одақ → ✅ Еуропа одағы [#21]
- ❌ банктік карта → ✅ банк картасы [#663]
- ❌ облыстық әкімдік → ✅ облыс әкімдігі [#651]
- ❌ танымалдылық → ✅ танымалдық [#41]

### 4. Drop the unnecessary genitive `-ның`
The object of an action noun takes the accusative or stays bare. The subject of a clause stays in the nominative. Dates use `жылғы`.

- ❌ жобаның талқылауы → ✅ жобаны талқылау [#403]
- ❌ Құдайдың бар екенін → ✅ Құдай бар екенін [#577]
- ❌ 2020 жылдың 5 сәуірі → ✅ 2020 жылғы 5 сәуір [#64]
- ❌ монархияның құлауынан кейін → ✅ монархия құлағаннан кейін [#4575]

### 5. Use a verb clause, not "noun + кезінде"
- ❌ жер сілкінісі кезінде → ✅ жер сілкінгенде [#117]

### 6. The locative `-да` is for physical location, not clothing, possession or periods
- ❌ көзілдіріктегі жігіт → ✅ көзілдірікті / көзілдірік таққан жігіт [#2734]
- ❌ менде сұрақ бар → ✅ сұрағым бар [#515]
- ❌ 90-жылдарда туған → ✅ 90-жылдары туған [#3180]

### 7. Modal words: the person ending goes on the verbal noun
- ❌ бару керекпін → ✅ баруым керек [#85]
- ❌ Олар барулары керек → ✅ Олар баруы керек [#85]

### 8. Tense and aspect: don't copy Russian verb forms
- Russian future «будет + verb» is not `-атын болады`. ❌ жауапкершілікке тартылатын болады → ✅ жауапкершілікке тартылады [#162]
- An ongoing action needs `-ып жүр/-ып жатыр`. ❌ жұмыс іздеймін → ✅ жұмыс іздеп жүрмін [#1692]
- «начать + infinitive»: ❌ оқып бастадым → ✅ оқи бастадым [#2840]
- A finished result takes a helper verb: ❌ жүлдені ұтты → ✅ жүлдені ұтып алды [#2237]
- ❌ мен кешігіп жатырмын → ✅ кешігіп барам [#4111]

### 9. "Хотеть, чтобы" and reported speech use `де-`
- ❌ балаларыңыздың … өсуін қаласаңыз → ✅ балаларыңыз … өссін десеңіз [#440]
- ❌ дайын екенін айтты → ✅ дайынбыз деді [#3018]

### 10. Russian «ни» concessives are not negatives
- ❌ қайда болмасаң да → ✅ қайда жүрсең де [#2753]

### 11. Keep generic nouns singular
After `көп`, `бірнеше` and `барлық`, and for generic objects, the noun stays singular.
- ❌ барлық адамдар, көп кітаптар, бірнеше оқушылар → ✅ барлық адам, көп кітап, бірнеше оқушы [#923]

### 12. Cut officialese (канцелярит)
- ❌ … инвесторы болып табылады → ✅ … – инвесторы [#21]
- ❌ оқиға орын алды → ✅ оқиға болды [#21]
- ❌ үстіміздегі жылы → ✅ биыл [#3456]
- ❌ бүкіл әлем бойынша → ✅ дүниежүзінде [#33]
- ❌ есік арқылы кіру → ✅ есіктен кіру [#1206]

### 13. Watch "false friend" verbs
Some Russian verbs are always translated with one Kazakh verb, even where Kazakh uses something else. Common ones are `қабылдау` (принять), `жоғалту` (потерять) and `бөлісу` (поделиться).
- ❌ табысын жоғалтты → ✅ табысынан айрылды [#29]
- ❌ дәрі қабылдады → ✅ дәріні ішеді [#31]
- ❌ шешім қабылдады → ✅ шешімге келеді [#31]

### 14. Ages are counted with `жас`
- ❌ Маған 20 жыл толды! → ✅ Мен 20 жасқа толдым! [#3187]

## Looking things up

The `references/` folder holds the full dictionary, one entry per line:
`❌ calque · ⁉️ Russian source · ✅ natural Kazakh — why [#post](link)`

| File | What's in it |
|---|---|
| `references/grammar.md` | Cases, possessives, tense and verb forms (the largest file) |
| `references/lexical.md` | Wrong words and terms translated word for word |
| `references/phrase.md` | Multi-word expressions copied from Russian |
| `references/bureaucratic.md` | Officialese |
| `references/word-order.md`, `style.md`, `spelling.md` | Smaller groups |
| `references/rules.md` | The author's longer explanations, grouped by category |

The files are large. **Search them; don't read them whole.** Search by the Kazakh word, its stem, or the Russian source:

```bash
grep -i "жоғалт" references/*.md
grep -i "принять" references/*.md
grep -i "кезінде" references/grammar.md | head -20
```

Search by the **stem** (`жоғалт`, not `жоғалтты`), because entries show one inflected form.

## Limits

- The dictionary shows one author's corrections. A few entries are her personal position on contested usage. Those are marked medium confidence in the source data.
- The checker finds exact phrases and some patterns. It can't judge meaning, and a clean result doesn't prove the text is calque-free.
- Don't over-correct. If a construction is natural Kazakh in that context, keep it. The aim is natural Kazakh, not avoiding certain words at any cost.
