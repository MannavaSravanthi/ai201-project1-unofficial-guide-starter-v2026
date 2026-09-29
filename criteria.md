# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

Four of my five test questions ask for a single fact stated directly in the guide — a frequency or a count (trams every X minutes, six train services, two-hourly buses). Those I'd expect to retrieve reliably since the answer is a specific number sitting in one section. The restaurant question ("which district has the best restaurants") is different — it's closer to a recommendation than a plain fact, so the right chunk might not literally answer the way I phrased the question. That's the one question I'd expect this target to need to absorb, which is why I set 4 of 5 instead of 5 of 5.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

My `ask` command's output always includes a "Sources retrieved:" line listing every document handed to the model for that question, regardless of what the generated answer itself says — that's a property of how the pipeline is built, not something the model's output could vary on its own. As long as a question isn't refused outright, a source gets named every time. That's why I set this at 5 of 5 rather than leaving room for a miss.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**

When I measured this in Milestone 4, my five in-corpus questions all landed between 0.24 and 0.32 distance, while my five out-of-scope questions all landed at 0.81 or higher — a gap of roughly half a point with nothing in between. With that much separation, I'd expect the gate to get this right almost every time. I left room for 1 of 5 to miss in case a real question ever comes in phrased ambiguously enough to land in that gap, which none of my ten test questions actually did.

---

## 4. Something about your chunks

For at least 4 of 5 chunks sampled from my own chunker, the chunk reads as a complete thought no sentence is cut in half at either boundary and no chunk is shorter than 100 characters.

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->



**Why this target:**

The starter's fixed 800 character chunker produced a shortest chunk of only 24 characters clearly a meaningless fragment and cut straight through city_guides labeled sections rather than respecting them. Since these documents are organized by heading, a chunker that respects that structure shouldn't produce anything shorter than roughly one full sentence. 100 characters is about that length, so anything under it is very likely a fragment rather than usable content

---

## 5. Your choice

For at least 4 of my 5 test questions, the source document named in the answer is the actual document the answer came from not merely any document that happened to be retrieved.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->



**Why this target:**

Naming a source and naming the correct source aren't the same guarantee an answer could cite a file without the fact actually coming from it. With 9 separate town guides in this corpus, a wrong but plausible sounding town would be an easy failure to miss if I only checked whether a source was present at all, but it's the kind of error that would actually mislead someone using this as a real travel guide.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->