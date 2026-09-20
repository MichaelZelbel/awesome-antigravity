---
name: strip-ai-tells
description: Use when prose a human reads as writing sounds machine-written and needs an edit that fixes it rather than a report about it. Trigger on "make this sound human", "de-AI this", "humanize this chapter", "does this read as AI", or an editing pass over a manuscript, chapter, draft, post or sales page. Handles a whole book one chapter at a time.
---

# Strip AI tells

Everything this skill needs is in this one file. The lists are yours to edit: cross out what you
disagree with, add what you catch your own AI doing.

## What this is

An edit that removes the fingerprints of machine writing and leaves the author's meaning, facts,
terminology, humour and level of difficulty exactly where they were.

**Not a detector and not an audit. The output is the edited text.** Handing back a list of problems
for someone else to fix by hand is a failed run.

## Two layers, and both run

**Layer 1 is the banned list below.** Characters, phrases and words that are never allowed, no
judgment involved. Check it every time before handing text back, and never argue with it.

**Layer 2 is the catalogue further down.** The shapes no list can catch: text narrating itself,
manufactured contrast, neat triads, paragraph templates. This is where most of the work is.

---

## Layer 1: the banned list

Edit this section. It is a starting list, not scripture. Everything inside code blocks, inside
`backticks` and every URL is exempt: a command with a dash in it is a command, not writing.

**Characters, never:**

- the em dash
- the en dash
- the horizontal bar
- a spaced hyphen used as a dash

Use a full stop, a comma, brackets or a colon instead, or rewrite the sentence. Normal hyphens in
words like "hands-off" are fine.

**Phrases, never:**

it's not just / it is not just / in today's fast-paced / let's dive in / here's the thing / at the
end of the day / in conclusion / it's worth noting that / it is worth noting that / whether you're
/ when it comes to / navigating the / in the ever-evolving / plays a crucial role / it's important
to note

**Words, never:**

robust / seamless / seamlessly / leverage / leveraging / delve / realm / landscape / unlock /
unlocking / elevate / game-changer / game-changing / comprehensive / cutting-edge / transformative
/ myriad / tapestry / testament

A banned word is never swapped mechanically. "Leverage" can become use, borrow, or run on, and only
the sentence knows which. Rewrite the line.

**Openings, never:** no piece of writing and no reply opens by flattering the reader or by
correcting them.

great point / great post / great question / thanks for sharing / love this / spot on / couldn't
agree more / this is so true / absolutely / actually, / not quite / small correction / to be fair

**One length rule, and it is advisory.** A sentence over about 28 words is worth a second look in a
post or an email. In book prose it means nothing on its own. Never split a sentence just to shorten
it, and never report sentence lengths as defects.

If your assistant can run commands, it can search the text for every item above rather than reading
for them. If it cannot, the list is short enough to check by eye.

---

## Layer 2: read what owns the text first

- This file, so the banned list is fresh in mind.
- The text's own conventions if it has any: a book's style guide, a publication's house rules.
- The strongest two pages of the text itself. That is the voice to edit toward, not yours. Work out
  where the writing is already natural, then bring the weak passages up to it.

## Never touch

Editing any of these is not humanising, it is breaking something.

- **Quoted output** in blockquotes: what a tool said back, an interview, a source. Word for word.
  Two changes allowed and no others: fixing a banned dash, and an ellipsis where you cut material.
- **Fenced code blocks.** Prompts, commands, file contents, anything the reader types.
- **Any text that has to match something outside the document.** A printed prompt whose words must
  still match the page it links to, for one. Edit it and the link starts lying.
- **Marker comments a pipeline reads**, the kind that get pulled out to make social posts.
- **Anchors and heading text** that contents links and cross-references hang off.
- **Diagram blocks.** Labels are sized to a wrap width, so retyping one re-renders the picture.
- **A term the text defines once and reuses.** Stable terminology beats variety. Five synonyms for
  one concept is a defect, not a style.

## Two modes

**scan** reads and counts, edits nothing: the worst sections ranked, the top patterns, with line
numbers. Use it to plan a pass over something long.

**edit** is the default: fix the prose.

## Running one piece: a chapter, a post, a page

1. Read it cold, top to bottom, before touching anything.
2. Mark every hit: line number, what it is.
3. Fix in one pass. Prefer deleting a sentence to rewriting it. Most tells are sentences a human
   would never have bothered to write.
4. Re-read cold. Does it still sound like the same author?
5. Check the banned list one last time.
6. Save one version per piece, so any single edit can be undone on its own.

## Running a whole book

- **One chapter per pass.** Never load the whole manuscript. Read by heading.
- **Count before you start.** Search the manuscript for the phrases in the catalogue and rank
  chapters by how many they hold. Every book's worst habit is a different one, and often the banned
  list is already clean while a single judgment pattern is doing all the damage. Count again halfway
  through.
- **Carry a running inventory** across chapters: phrases, metaphors, openings, endings already used.
  A shape that is fine once is conspicuous the tenth time, and only a running list sees that.
- **When you catch one, search the whole book for it before fixing the one you found.** A tell in
  one chapter is usually in three.
- **Compare chapter openings against each other, and endings against each other.** That is where a
  template shows itself, never inside a single chapter.
- If the book already has a queue or a checklist, work that one. Two lists means two half-edited
  manuscripts and no way to tell which chapter was done properly.

## How hard to edit

Change a sentence when it carries a machine fingerprint, when it is inflated or generic, when it
repeats a shape already used several times, or when deleting it plainly improves the paragraph.
Otherwise leave it. The target is not maximum change. It is the most tells removed per edit.

Never:

- add mistakes, typos, slang or filler. Natural writing is not bad writing.
- swap one cliche for another. "It is not just about memory, it is about control" turning into "At
  its core, memory is control" is the same sentence in a new costume.
- introduce a claim, fact, example, promise or number that was not already there.
- weaken a claim the author has grounds for, or strengthen one they do not.
- flatten every sentence to one length. Variation is the whole point.
- make every paragraph elegant. Some paragraphs are one sentence, and then they stop.

## What to report back

Short. One line on what changed and how many hits were fixed. Never a table of individual edits
unless you are asked for one.

## Red flags

| The thought | What it actually means |
|---|---|
| "I will list the problems and let the author fix them" | Not the job. Edit the text. |
| "An AI could have written this sentence too" | So could a human. Leave good writing alone. |
| "I will vary the terminology so it reads less repetitive" | That is how a technical book loses its meaning. Stable terms stay. |
| "250 sentences are over 28 words, I will split them" | Length is advisory in book prose. Do not. |
| "This quote reads a bit AI, I will smooth it" | A quote is evidence. Word for word, or not at all. |

---

# The catalogue

Six families. Each lists the tells and the fix. None of these is banned the way the list above is
banned: a natural sentence is allowed to use an ordinary construction. What marks text as
machine-written is **accumulation**, so judge a hit against how often the shape has already
appeared, not against the phrase alone.

## A. The text narrating itself

The most common tell in long writing, and the one readers feel as "this was assembled, not
written". A model produces it while trying to manufacture continuity it never planned.

**Forward:** the rest of this book / the rest of this chapter / everything that follows builds on /
we will return to this / as we will see / in the next section / later in this book / keep this in
mind / this will matter later / for the remainder of this chapter.

**Backward:** as we discussed earlier / as you have already seen / as we learned in Chapter 2 / now
that we have covered X / building on what we discussed.

**Roadmap:** in this chapter we will explore / first we will look at / before we dive into / let us
start by / let us break this down / now let us turn to / with that foundation in place / we will
cover this in more detail shortly.

**Fix:** delete. Most of these tell the reader nothing they can act on. Where a pointer genuinely
helps somebody find their way, keep exactly one clause saying what is waiting there and why they
would want it. A pointer that names neither is worse than no pointer. Do not keep telling a reader
that something matters later. Make it matter when they arrive. A chapter almost never needs to
announce the subject it is about to start.

## B. Stock constructions and manufactured contrast

**Formulas:** at its core / at the heart of / the key is / the real power lies in / what makes X
powerful is / what matters most is / the result? / the good news? / the bottom line? / the
takeaway? / think of it as / imagine / in other words / put simply / from X to Y / more than just /
that is where X comes in / this is where it gets interesting / and that is exactly the point.

**Contrast frames:** not X but Y / not just X but Y / less X, more Y / rather than X, Y / instead
of X, think Y / X sounds simple, but / X may seem like, but.

**Fix:** keep a contrast that carries a real distinction. Rewrite the ones that exist because the
sentence wanted a flourish. Watch for the trap of swapping one frame for another, which changes
nothing.

## C. Filler shapes

**Suspiciously neat triads.** Three polished items, every time: faster, easier and smarter /
understand, organise and act / simple, powerful and flexible. Do not mechanically turn every three
into two. Ask whether all three earn their place, then cut the decorative one. Across a book, reduce
the sense that every idea conveniently arrives in a set of three.

**Transition addiction.** However / moreover / furthermore / additionally / ultimately / crucially /
importantly / interestingly / in practice / in essence / that said / with that in mind / at the same
time / on the other hand / as a result. The best replacement is usually nothing at all. Let
paragraphs follow each other when the connection is obvious.

**Over-explaining.** The five-step loop: make a point, say it again in other words, explain that,
give an example, restate the point. Markers: in other words / what this means is / to put that
another way / essentially / in practical terms. Compress. Do not assume the reader missed the
previous sentence.

**Mini-conclusions.** A tidy summary at the end of every section: "ultimately the key is to find
what works for you", "by understanding these principles you can", "and that is what makes this so
powerful". Delete the ones that only restate what was just read. A section may end on its last real
point.

## D. Sentences that say nothing

**Generic abstraction.** "This creates a more intuitive experience." "This opens up new
possibilities." "The implications are profound." "This represents a significant shift." The test:
could this sentence appear unchanged in a hundred unrelated articles? If yes, make it concrete, say
what specifically changes, or delete it.

**Machine vocabulary** beyond the banned list: nuanced, multifaceted, holistic, pivotal, crucial,
foster, streamline, facilitate, enhance, optimise, dynamic, ecosystem, journey, paradigm,
intersection, boundaries, intentional, thoughtfully, inherently, fundamentally. Plus the vague nouns
a model reaches for when it has nothing specific: context, capability, approach, experience,
interaction, system, process, framework. Keep them where they are precise. Rewrite them where a
plainer word would say more.

**Consulting language.** Drive adoption, enable transformation, accelerate outcomes, maximise
impact, deliver value, align stakeholders, scalable solution, strategic approach. Keep real
specialist terms. Cut the presentation deck that wandered into the prose.

**Synthetic enthusiasm.** Powerful, exciting, remarkable, incredibly useful, revolutionary, amazing.
Show the benefit instead of naming it.

**Unearned certainty.** The reality is / the truth is / there is no question that / one thing is
clear / it is clear that / the answer is simple / this changes everything. Replace with the actual
claim. Do not hedge a claim the author has grounds for.

**Defensive hedging.** Clusters of generally, typically, often, potentially, in many cases, to some
extent, relatively, arguably, may, might. Keep the qualifications that are honestly necessary, cut
the ones protecting nobody.

## E. Fake intimacy with the reader

**Manufactured reactions.** You might be wondering / if you are like most people / we have all been
there / you may feel overwhelmed / do not worry / the good news is / you are not alone. Delete these
when the text has no way of knowing what the reader feels. Where a real objection exists, answer it
directly instead.

**Coaching cadence.** You can, you will, you need to, you should, all you have to do, simply, just.
Second person is fine, and plenty of good books are written in it. The tell is nearly every
paragraph telling the reader what they can or should do. Vary it.

**Fake punchiness.** The reason? Simple. / The problem? Memory. / No setup. No hassle. / And the
best part? / That is it. / Powerful. One strong fragment works. A page of them reads as marketing.

**Manufactured symmetry.** "It does not replace your judgment, it amplifies it." "The system adapts
to you rather than forcing you to adapt to it." These can be excellent sentences. The defect is
accumulation: when too many lines sound quote-ready, flatten some back into ordinary prose.

## F. Shape, visible only across a whole book

**Paragraph architecture.** Claim, explanation, example, neat closing line. Or setup, contrast,
resolution. Or topic sentence, three supports, small conclusion. When every paragraph runs the same
invisible template, vary it. Some paragraphs are one sentence. Some develop an observation and stop
without wrapping it up.

**Sentence rhythm.** Repeated long-sentence-then-short-punchline, repeated rhetorical question then
immediate answer, repeated colons, repeated "This means", repeated "That is why". Fix enough of them
to restore a natural rhythm. Do not randomise sentence length mechanically.

**Chapter openings.** Compare them against each other: imagine / think about / most people / at
first glance / here is the problem, plus anecdote-then-lesson and question-then-answer. Each chapter
should open the way its own subject deserves.

**Chapter endings.** Summary plus preview, "now that you understand X you are ready for Y",
motivational takeaway, three-item recap, neat aphorism. A chapter does not need to hand the reader
ceremonially to the next one. End on the strongest real idea.

**Repeated conceptual vocabulary.** A model gets attached to a small set of nouns and reuses them
for everything: context, control, memory, workflow, system, capability, approach, framework. Where
the repetition is not carrying meaning, name the specific thing instead. Where the term is the
text's own defined vocabulary, leave it exactly as it is.

**Vague referents.** This approach, this process, this shift, this capability, these insights. Cover
everything above the sentence and ask what the word points at. If the answer is not immediate, name
the thing.

---

## The last check, before handing the text back

1. Does it still sound like the same author?
2. Were formulas removed, or only exchanged for different formulas?
3. Is the narration about what the text is about to do gone?
4. Did the meaning survive intact?
5. Was genuinely good writing left alone?
