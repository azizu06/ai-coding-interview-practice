# ai coding interview practice

Practice problems for the AI-assisted coding interview format that Meta and a growing list of companies use in 2026. You get a small codebase with bugs, a solver to implement, and timed tests that force you to optimize. An AI assistant is allowed the whole time. The interviewer grades how you use it.

This repo gives you that setup inside your own editor with your own coding agent (Claude Code, Cursor, Codex, Copilot, whatever you already use). One problem per folder, an answer key per problem, and a prompt that turns your agent into the interviewer.

## the format

Every problem runs the same way the real interview does. About 50 working minutes, four phases:

1. Code comprehension. Read a small codebase and figure out how it fits together.
2. Fix the bugs. The domain class has two planted bugs. Some tests are commented out with `????` where the expected value should be. Fill those in, run them, follow the failures to the bugs.
3. Implement the solver. `solver.py` has a stub. Make the correctness tests pass. Brute force is fine here.
4. Optimize. Uncomment the timed tests. Brute force fails them. Find the better algorithm, and then the one after that, because the last timed test usually breaks the first optimization too.

## how to practice

```
git clone https://github.com/azizu06/ai-coding-interview-practice
cd ai-coding-interview-practice
```

Pick a problem, open `problems/NN_slug/INSTRUCTIONS.md`, start a 50 minute timer, and open your coding agent in that folder.

Run the demo and the tests from the repo root:

```
python problems/01_word_container/src/main.py
python -m unittest discover -s problems/01_word_container/src -v
```

Do not open `solutions/` until the timer is done. Each answer key lists the two bugs, the optimization ladder with complexities, and examples of good and bad prompts for that problem.

## practice with your agent as the interviewer

Paste [INTERVIEWER_PROMPT.md](INTERVIEWER_PROMPT.md) into your coding agent along with the problem path. It will run the session, ask you to explain your plan before it writes code, refuse to just hand you the answer, and give you a written evaluation at the end using the same criteria interviewers use.

## what interviewers are actually grading

These notes come from watching a former Meta staff engineer run a mock of this format and from candidate reports.

- Using the AI too little is the most common failure. The interview is built to be too hard to finish by hand. If you ignore the assistant, they cannot evaluate how you work with one, and the candidate next to you is moving twice as fast.
- Ask informed questions, not lazy ones. "Implement the solver" and "find the bug" teach the interviewer nothing about you. "Add a one sentence comment to each function in word_list.py" or "give me a bulleted list of the key functions per class" speeds up comprehension and shows you are driving.
- Say your plan out loud before you prompt. A two sentence summary of the brute force, then ask the agent to write exactly that. Now the interviewer knows the idea was yours.
- Do not narrate the generated code line by line. Give a two or three sentence summary of what it does and confirm it matches what you expected.
- Run tests one at a time. Uncommenting everything at once buries you in failures.
- Adding or tightening a test that you think is weak is a visible plus.
- Ask for complexity without leading. "What is the time complexity if N is the number of words and M is the average length" instead of "is this N squared". Then check it against your own answer.
- Clear the chat before asking for optimization options. If the old brute force is in context the model will anchor on it and agree with you.
- The assistant will confidently introduce bugs. In the reference walkthrough the model added a substring check that counted a word as containing itself. A print statement caught it. Read what it writes.
- Ask for a list of options, then pick. "Give me a concise list of options to optimize this beyond brute force" surfaces the trie or heap or index you did not think of, and you still get credit for choosing.

## problems

| # | problem | difficulty | domain |
| --- | --- | --- | --- |
| 01 | word container | medium | strings, sets, trie |
| 02 | spell checker | easy | edit distance, indexing |
| 03 | inventory packer | easy | greedy, bin packing |
| 04 | task scheduler | medium | graphs, topological order |
| 05 | route planner | medium | weighted graphs, dijkstra |
| 06 | maze solver | medium | grid bfs, state search |
| 07 | friend recommender | medium | social graph, counting, top k |
| 08 | card game | medium | enumeration, precomputed tables |
| 09 | log analyzer | medium | sliding window, percentiles |
| 10 | rate limiter | hard | sliding window, token bucket |

## credit

The format is modeled on the AI coding practice at [Hello Interview](https://www.hellointerview.com/practice/ai-coding) and Evan King's [walkthrough video](https://www.youtube.com/watch?v=A1kX8fJx53c). All code and problem text here is original. If you want the real thing with an in-browser CoderPad clone and AI grading, go use theirs.

## license

MIT
