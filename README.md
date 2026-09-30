# The Unofficial Guide

Sravanthi — city_guides corpus

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a retrieval-augmented Q&A system built on the `city_guides` corpus — nine town guides plus five cross-cutting guides (accessibility, eating, regional transport, seasons, walking) covering a fictional region. It answers specific factual questions about getting around, where to eat, where to stay, and what to see in each town, pulling answers only from these documents rather than the model's own general knowledge. If a question falls outside what the corpus covers, it refuses rather than guessing.

## Chunking Strategy

**Chunk size:** Not fixed by design — each chunk is one full document section, so size varies naturally with how much the author wrote under that heading (184–762 characters, averaging 323, across 94 chunks)
**Overlap:** None — since chunks follow section boundaries rather than a character count, there's no repeated text between chunks to create

The starter's fixed 800-character chunker was cutting straight through the labeled sections in these documents (Getting There, Where to Eat, etc.), producing a shortest chunk of just 24 characters — a meaningless fragment. Since city_guides documents are already organized by heading, I replaced it with a chunker that splits on each `## ` section heading instead, so every chunk is one complete section. Any intro text before the first heading becomes its own "Overview" chunk instead of getting dropped, and every chunk is prefixed with the document's title so it still identifies which town it's about even when read completely on its own.

After the change: 94 chunks, averaging 323 characters (shortest 184, longest 762) — versus 51 chunks averaging 650 characters (shortest 24, longest 800) with the old fixed-size approach.

## Sample Chunks

Produced by: `chunker.py::split_documents`

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

Overview

An honest assessment rather than a promotional one. Some of these places are difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** How often do Marchwood's trams run on weekdays during the day?

**Answer:**

```
(best distance 0.262, cutoff 0.5)

Marchwood's trams run every 8 minutes on weekdays (guide_marchwood.md).

Sources retrieved: guide_eating.md, guide_kestrelford.md, guide_marchwood.md
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| How often do Marchwood's trams run on weekdays during the day? | Yes | 0.2437 |
| Which district in Marchwood has the best restaurants? | Yes | 0.3069 |
| How many train services run from Brightwater to the regional hub on Sundays? | Yes | 0.3199 |
| How often does the bus to Kestrelford run on Saturdays? | Yes | 0.3061 |
| Why is the Halden Bay coastal path sometimes closed? | Yes | 0.3143 |
| What is the capital of Mongolia? | No | 0.8089 |
| How do I change the oil in a diesel engine? | No | 0.8881 |
| Who won the 1994 World Cup? | No | 0.9839 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8350 |
| How do I write a for loop in Rust? | No | 0.8365 |

My five in-corpus questions all landed between 0.24 and 0.32. My five out-of-scope questions all landed at 0.81 or higher. That left a gap of about half a point (0.32 to 0.81) with nothing in it, so I set `THRESHOLD = 0.5` in `config.py` — roughly centered in that gap, with plenty of room on both sides in case a real question comes in slightly noisier than my test set.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I didn't understand what the relevance cutoff (`THRESHOLD` in `config.py`) actually meant or how I was supposed to pick a number for it — I assumed it was something to guess at. I asked AI to explain it, and it clarified that distance is "lower is better" (a close match sits around 0.3, an unrelated one around 0.9), and that the way to set it isn't to guess but to run my own in-corpus questions and my own out-of-scope questions, note the best distance for each, and place the cutoff in the gap between the two groups. I ran all 10 of my test questions this way and found my in-corpus results clustered at 0.24–0.32 while my out-of-scope results clustered at 0.81+, so I set `THRESHOLD = 0.5` — in the middle of that gap — instead of leaving the starter's default of 0.6.

**2.** I pasted my `judge()` function in `scorer.py` and asked AI to check it for syntax errors and whether its time complexity could be reduced. My first version compared `expects` and `answer` directly without lowercasing them, even though the function's own docstring says the match should be case-insensitive — so a correct answer that happened to capitalize a word differently than `expects` (e.g. "Marchwood" vs. "marchwood") would have been marked wrong. AI pointed this out and I added `.strip().lower()` to both sides of the comparison to fix it. On time complexity, it confirmed there wasn't really anything to reduce — a substring containment check (`in`) is already about as efficient as this kind of match gets, so I left that part alone.

**3.** After my before run showed the Kestrelford question failing all three runs identically, I asked AI to help me figure out why a 3/3 identical failure felt different from a random miss. It pointed out that my system's actual answer ("every two hours") and my expected phrase ("two-hourly") mean the same thing, and that my scorer's literal substring match doesn't credit synonyms the failure was in the test, not the system. I didn't just take that at face value. I went back to my own `judge()` function in `scorer.py` and confirmed the `in` check really was doing an exact match with no normalization for phrasing. That reframed my whole Milestone 2 and 3 write up around this one finding instead of treating it as a real retrieval problem.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

Produced by `run_eval.py::main` (criteria 1, 2, 5) and `run_eval.py::check_out_of_scope` (criterion 3), from `results/run_2026-09-29_1540_before.md`. Criterion 4 comes from `chunker.py::split_documents`, sampled with `python app.py chunks -n 5`. Corpus: `city_guides`. Top-k: 5. Relevance cutoff: 0.5. Three runs per question, caching off.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks read as a complete thought, ≥100 characters | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Cited source is the actual source the answer came from | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Criterion 1** — produced by `run_eval.py::main` using `scorer.py::judge`

```
How often do Marchwood's trams run on weekdays during the day? run 1
Marchwood's trams run every 8 minutes on weekdays (guide_marchwood.md).
```
expects: "8" found and pass

Question 4 (the Kestrelford bus question) failed all three runs but not because the system got it wrong. Every run answered "every two hours," which means the same thing as my expected phrase "two-hourly." My scorer does a literal substring match, so a correct answer worded differently than `expects` reads as a miss. The target is still met at 4/5 in every run, but this is worth carrying into Milestone 2 and 3 rather than ignoring.

**Criterion 2** — produced by `run_eval.py::main`

```
Which district in Marchwood has the best restaurants? run 2
The best eating in Marchwood is in the Northgate district.

Sources: `guide_marchwood.md` and `guide_eating.md`
```

**Criterion 3** — produced by `run_eval.py::check_out_of_scope`

```
refused  (best distance 0.809)  What is the capital of Mongolia?
refused  (best distance 0.888)  How do I change the oil in a diesel engine?
refused  (best distance 0.984)  Who won the 1994 World Cup?
refused  (best distance 0.835)  What is the recommended dosage of ibuprofen for a headache?
refused  (best distance 0.836)  How do I write a for loop in Rust?
gate refused 5 of 5
```

**Criterion 4** — produced by `chunker.py::split_documents`, sampled via `python app.py chunks -n 5` (see Sample Chunks in Unit 1 all five read as complete sections, shortest is 184 characters, well above the 100 character floor)

**Criterion 5** — produced by `run_eval.py::main`

```
Why is the Halden Bay coastal path sometimes closed? run 1
The Halden Bay coastal path is closed in high wind because it is exposed and genuinely dangerous (*guide_halden_bay.md* and *guide_walking.md*).
```
Both cited documents are directly about Halden Bay's path conditions. I checked the "Northgate" claim (question 2) directly against `guide_marchwood.md`'s "Eat and drink" section, which states: *"The best eating is in the Northgate district, a 12-minute tram ride from the station, where about thirty restaurants sit within four streets."* — a verified match, not an assumption.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer (4 of 5) | MET | Held at exactly 4/5 in all three runs, not fluctuating between passes. The one consistent miss (Kestrelford bus) wasn't the system giving a wrong answer it answered "every two hours" every time, which means the same thing as my expected phrase "two-hourly." My scorer's literal substring match doesn't credit that, so the target is met by the numbers, but I'm flagging that the underlying cause isn't a retrieval or generation failure. |
| 2 | Every answer names a source (5 of 5) | MET | All 15 answers across the three runs (5 questions × 3 runs) named at least one source, either inline in the sentence or in a "Sources:" line held completely, with no exceptions. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | The gate refused all 5 out of scope questions in the single deterministic pass, clearing the 4 of 5 target with a full point of margin. |
| 4 | Sampled chunks read as complete, ≥100 characters (4 of 5) | MET | Checked all five sampled chunks directly: each is one whole document section, none cut off mid sentence, and the shortest is 184 characters well clear of the 100 character floor. 5 of 5, not just 4. |
| 5 | Cited source is the actual source (4 of 5) | MET | Spot checked the least obvious case (the "Northgate" restaurant claim) directly against `guide_marchwood.md`'s text and confirmed it's stated there verbatim. The other four questions cite documents that are directly on topic for what's being asked, not documents that merely happened to be retrieved. 5 of 5. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

I missed nothing all five criteria held at or above target in every one of the three runs. A clean sweep like this is a real result, but it usually means at least one target was set conservatively rather than the system being flawless everywhere, so here's an honest look at which ones were too loose.

**Criterion 3 (the relevance gate) is the clearest case.** My distances showed a wide, consistent gap: in corpus questions topped out at 0.32, and out of scope questions never came in under 0.81. With separation that large, the gate refusing 4 of 5 out of scope questions was never really in doubt. I set the target at 4/5 to leave room for an ambiguous edge case, but none of my ten test questions actually produced one. I'd tighten this to **5 of 5**.

**Criterion 2 (every answer names a source) is loose for a different reason it isn't measuring much.** My `ask` command appends a "Sources retrieved" line to every non refused answer as a fixed part of its output format, so the source list is guaranteed by the code rather than something the model could fail to produce. Passing this 5/5 tells me almost nothing about whether the system is actually working correctly, only that I didn't break the output template. A more meaningful version of this criterion would check whether the *top ranked* retrieved chunk not just any retrieved chunk is the one the answer cites, which is closer to what criterion 5 already tests.

The criterion I'd actually tighten going forward is criterion 3, from 4 of 5 to 5 of 5, since the real distance gap in my corpus supports a stricter bar than I originally set. 
## The Improvement

**What I changed:** Raised `THRESHOLD` in `config.py` from 0.5 to 0.4, tightening the relevance gate.

**Why I picked it:** My Milestone 3 diagnosis pointed directly at criterion 3 the gate's target (4 of 5) had more margin than my actual distance data supported, since my in corpus questions never exceeded 0.32 and my out of scope questions never fell below 0.81. Tightening the cutoff was the most direct way to test whether the gate could hold up to a stricter bar.

### Run Log — After

Produced by `run_eval.py::main` / `run_eval.py::check_out_of_scope`, from `results/run_2026-09-29_2337_after.md`. Same corpus, same top-k, `THRESHOLD` changed from 0.5 to 0.4.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out of corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks read as a complete thought, ≥100 characters | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Cited source is the actual source the answer came from | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

No the results are identical to "before," down to the exact same distances for every question, confirmed across two separate "after" runs. Tightening `THRESHOLD` from 0.5 to 0.4 made no measurable difference on this test set, and looking at the actual numbers explains why: my in corpus questions never went above 0.3199, and my out of scope questions never went below 0.8089. Both my old cutoff (0.5) and my new one (0.4) sit inside that same half point gap with nothing in it, so neither threshold could possibly change which questions pass or fail I'd have needed to move the cutoff all the way up past 0.81, or below 0.32, to see any actual change in behavior.

This is still a useful result. It confirms my Milestone 3 diagnosis was right for the wrong reason I said the gate's target was too loose because the *target number* (4 of 5) had room above it, but the gate's actual *cutoff value* also has enormous room on both sides. The real lesson isn't "tighten the cutoff," it's that this particular improvement can't be tested meaningfully with only 10 fixed test questions that all fall so cleanly on one side or the other. A more revealing change would need to add genuinely ambiguous test questions ones I'd expect to land near the middle of the gap rather than adjusting a number that has no fixed points nearby to move past.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

Nothing missed a target in either run all five criteria stayed MET before and after. But two things are still imperfect enough to name honestly rather than pretend are fully solved:

**Criterion 1's Kestrelford question is still a false negative, every time.** The system answers "every two hours," which is correct and means the same thing as my expected phrase "two-hourly," but my scorer's literal substring match doesn't credit it. I didn't fix this in this unit because the one change rule meant my improvement had to be the gate tuning I chose and rewriting `expects` after seeing it fail would be exactly the "loosen what you missed" trap the instructions warn against. I'm leaving it as a known, understood gap rather than a test I actually trust completely.

**Criterion 2 still isn't testing anything meaningful.** As I found in Milestone 3, the "Sources retrieved" line is guaranteed by my code's output format regardless of whether the answer is any good, so this criterion can't actually fail. I didn't rewrite it this unit because doing so would mean changing something other than my one chosen improvement, which the rules don't allow.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

I'd write **criterion 2** differently next time. Instead of "every answer names a source" which my code guarantees structurally and literally cannot fail I'd write something closer to what criterion 5 already tests "for at least 4 of 5 questions, the top ranked retrieved chunk is the one the answer cites." That would actually measure ranking quality instead of a fixed output habit.

I'd also write **criterion 3** differently, not by changing the "4 of 5" number itself, but by pairing it with something about margin, since my Milestone 4 improvement showed that tightening the cutoff couldn't be tested meaningfully against my existing ten questions (both my old and new cutoff sat inside the same gap with nothing between them). A criterion like "and the gap between my in corpus and out of scope distances should be at least 0.3" would tell me something new as I add test questions later, instead of a pass/fail number that stopped being informative the moment I confirmed the gap once.