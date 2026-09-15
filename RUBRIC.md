# Rubric

Six dimensions, the same six the interviewer prompt scores and the same six the README
lists. Every one runs 1 to 4. The scores describe the session, not the person, and a score
only means something if a specific moment in the session earned it.

The short version of the whole table: a 1 did not do the thing, a 2 did it late or only
after prompting, a 3 is a solid hire signal, and a 4 is the session you would tell someone
else about.

## Code comprehension

*Did you understand the codebase before you changed it.*

- **1** Started editing or prompting before reading. Could not say what the domain class was
  for when asked.
- **2** Read the README and skimmed the source. Learned how the pieces fit together by
  breaking them.
- **3** Ran the demo, read the domain class, and could describe in a couple of sentences what
  each file is for and where the solver plugs in, before touching anything.
- **4** Used the assistant to speed up comprehension on purpose, with something like a
  per-class list of key functions or a one line comment per function, and came out of it able
  to predict which file a given failure would be in.

## Debugging

*Did you use the tests to find the bugs, and can you explain the fix.*

- **1** Guessed at fixes, or asked the assistant to find the bugs and accepted what came back
  without checking.
- **2** Found the bugs eventually, mostly by trial and error, and could not say why the fix
  worked beyond that the test went green.
- **3** Uncommented tests one at a time, worked out each `????` value by hand before running,
  and followed each failure to its cause. Explained both fixes in terms of the behavior the
  code promised.
- **4** Predicted the failure from reading the demo output or the source before running
  anything, and tightened a weak test on the way through.

## Implementation

*Did you have a plan before you prompted, and did you verify the output.*

- **1** Asked the assistant to implement the solver with no stated plan, then shipped what it
  returned unread.
- **2** Had a rough idea, let the assistant fill in the shape of it, and checked it only by
  running the tests.
- **3** Said the approach out loud in two sentences before prompting, asked for exactly that,
  read what came back, and summarized what it does before moving on.
- **4** Caught a real mistake in generated code, said what was wrong with it, and got it
  fixed. Brute force first, correctness before speed, on purpose.

## Optimization

*Did you reason about complexity, and did you find the second rung of the ladder.*

- **1** Never got past brute force, or kept trying the same shape faster.
- **2** Reached one better algorithm, could not say what its complexity was without being
  told.
- **3** Named the bottleneck in terms of N and M, asked for a list of options rather than the
  answer, picked one, and stated the new complexity before running the timed test.
- **4** Found the second rung too, the one the last timed test forces, and could explain why
  the first optimization stopped being enough.

## AI usage

*Too hesitant or too dependent, did you lead the model, did you catch its mistakes.*

- **1** Either ignored the assistant almost entirely, or pasted its output straight in without
  reading. Both fail for the same reason: there is nothing to evaluate.
- **2** Used it for whole tasks with vague prompts ("implement the solver", "find the bug")
  and was carried by it.
- **3** Specific, scoped prompts. Asked for summaries and options, made the calls, read every
  diff, and asked for complexity without leading the answer.
- **4** Managed the context deliberately, for example clearing the chat before asking for
  optimization options so the brute force would not anchor it, and caught the model being
  confidently wrong.

## Communication

*Did the interviewer always know what you were doing and why.*

- **1** Long silences. The interviewer had to ask what was happening.
- **2** Narrated actions but not reasons, or read generated code aloud line by line.
- **3** Said the plan before doing it, flagged when changing direction, and gave short
  summaries instead of transcripts.
- **4** Kept the interviewer a step ahead the whole way, named the tradeoff being taken at
  each fork, and said plainly when something was not working and what would be tried next.

---

Grading works only in the same chat that did the session. The grader reads the conversation
itself, so a fresh chat has nothing to score, and an agent that was not there will invent a
session that never happened. If the session ran with an agent that has no memory of it, do
not paste this: grade yourself against the table above instead.

## Paste this into the same chat when the timer ends

```text
The session is over. Stop helping and grade it.

Grade from this conversation only, from what I actually said and did in this chat. Do not
give me the benefit of the doubt, and do not score anything you cannot point at.

1. Score all six dimensions 1 to 4: comprehension, debugging, implementation, optimization,
   AI usage, communication. For every score, quote the exact message or moment from this
   chat that earned it, and say in one line why that moment sets the score there. A score
   with no quoted evidence is not a score, drop it to the level you can evidence. A 4 with
   no quoted moment behind it is not allowed at all.

2. List every prompt I sent that was too vague to be useful, the "implement the solver" and
   "find the bug" kind. Quote each one, then rewrite it into the prompt I should have sent
   at that moment, specific to this problem and this file.

3. Name the one thing in this session that would have failed a real interview. One thing,
   the worst one, quoted.

4. Name the one thing that would have impressed a real interviewer. One thing, quoted. If
   there is nothing, say there is nothing rather than reaching for something.

5. Finish with three changes for next time, in order of impact, each one an action I can
   take in the first ten minutes of the next session.

Be blunt. An inflated score costs me the real interview.
```
