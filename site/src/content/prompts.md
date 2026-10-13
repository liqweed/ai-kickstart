---
summary: The prompt library for ai-kickstart.me. The prompts on START-HERE.html must match these word for word (scripts/check_kit.py).
---

# Prompts

Format: `## Group`, then `### Label`, an optional `> note`, and the prompt in a fenced block. Placeholders use `<angle brackets>`.

## Setup

### First contact
```text
Hi! This folder is my new Obsidian vault, set up from the AI Kickstart kit.
Please read AGENTS.md and _system/index.md (nothing else yet), then tell me in three short lines:
1) what this vault is for, 2) how you'll help me, 3) what we should do first.
Then create a test note at _inbox/hello.md that says "It works!" so I can check that you can write here.
```

### Help me with a setup step I'm stuck on
```text
I'm on harness step <P0.x> and I'm stuck: <what happened>. I use <Mac / Windows / Linux> and <AI tool>. Explain what to do in plain words, one step at a time, and wait for me after each step.
```

## Interview

### Start
```text
Start round 1 of my kickstart interview. Keep it friendly and one question at a time. I may answer by voice.
```

### Next round
```text
Start round <2 / 3 / 4> of my kickstart interview.
```

### Express (~20 min)
> Rounds 1 and 2 merged
```text
I'm short on time. Run the express version of my kickstart interview: rounds 1 and 2 merged, about 10 core questions. Then draft my profile with sensible defaults and put the deep dives in my harness plan for later.
```

### Fix my profile
```text
Read my profile files in _system/profile/ and show me anything that looks wrong, outdated or too vague. Ask me one question at a time to fix it, and show me each change before saving.
```

### Resume after a pause
```text
We paused my kickstart interview last time. Read the latest answer file in _system/kickstart/answers/ and continue where we stopped.
```

### Check-in (round 5)
```text
Let's do my kickstart check-in (round 5).
```

### If skills don't load
```text
Please read _system/skills/kickstart-interview/SKILL.md and follow it exactly. Start with the next round I haven't done yet.
```

### Chat-only round
```text
Using the attached kickstart files (interview-protocol.md and the round files), run round 1 of my kickstart interview in chat-only mode: one friendly question at a time, and at the end give me paste-ready markdown blocks headed with their file paths.
```

## Harness

### The main one
```text
Continue my harness plan.
```

### Status
```text
Harness status.
```

### Capture an idea
```text
Add to harness: <idea>.
```

### New AI tool
```text
I'm continuing my AI setup in a new tool. Read AGENTS.md, then _system/HARNESS-PLAN.md (the Now table and the last two session-log entries), and tell me where we are and what's next. Don't change anything yet.
```

### Step too big
```text
This step is too big for today. Split it into smaller steps in the plan and do just the first one.
```

### Not for me
```text
Skip that step. It doesn't fit me. Note why in the plan.
```

### Life changed
```text
Re-plan my harness. My priorities changed: <what changed>. Propose a new order before changing anything.
```

## Everyday life

### Morning
```text
Morning briefing.
```

### Sunday
```text
Weekly review.
```

### Keep something
```text
Save this to my notes: just the decision and why, not the whole conversation.
```

### Ask your notes
```text
What do my notes say about <topic>? Cite the notes, and tell me what's missing.
```

### Official letter
```text
Here's a letter I received (attached). In plain words: what is it, do I need to do anything, and by when? If I need to reply, draft a short, polite reply. Flag anything you're not sure about.
```

### Meal plan
```text
Plan dinners for next week for <who>. Respect everyone's dietary needs from their people profiles, keep weeknights under <30> minutes, reuse ingredients, and give me a shopping list grouped by aisle.
```

### Date night / outing
```text
Plan a date night for <Friday>. Three options, one recommendation.
```

### Trip
```text
Help me plan a trip to <place> around <dates>. Interview me first, one question at a time: who's coming, budget, pace, must-dos. Then draft an itinerary with a plan B for bad weather.
```

### Gift
```text
<Name>'s birthday is on <date>. Using their people profile, suggest 5 gift ideas at around <budget>, ranked, with where to get them. Avoid anything we've given before.
```

### Kids' test prep
```text
<Child> has a <subject> test on <topic> on <date>. Make a short study plan for the days until then, a one-page summary at their level, and 10 practice questions with answers on a separate page.
```

### Home fix
```text
<Appliance / problem> is <doing what>. Check my home manual notes for the model. Walk me through safe things I can try myself, and tell me when to call a professional.
```

### Subscriptions
```text
Here's a list of my subscriptions / a bank export (attached). Find recurring payments, group them, total them per month and year, and suggest what to cancel or downgrade. Ask me about anything unclear.
```

## Work (any job)

### Decision memo
```text
Help me decide between <A> and <B>. Ask me up to 5 questions first. Then write a one-page decision memo: context, options, trade-offs, a recommendation, and what would change your mind.
```

### Red team
```text
Red-team this <plan / document> (attached). What are the 5 most likely ways it fails or gets misunderstood? For each: how likely, how bad, and what would prevent it.
```

### Meeting prep
```text
I have a meeting with <who> about <topic> on <date>. Using my notes on them and the topic, give me: the goal of the meeting, 3 key points, questions to ask, and likely objections with answers.
```

### Meeting notes → actions
```text
Here are my rough meeting notes. Turn them into: decisions, actions (who / what / by when), open questions, and a short follow-up email I can send.
```

### Email in my voice
```text
Draft a reply to this email. Tone: <friendly but firm>. Goal: <what I want to happen>. Keep it under 120 words. Don't send anything, just draft.
```

### Big task
```text
Break "<task>" into 15-minute steps, in order. Mark the first one I can do right now, and anything I need from someone else.
```

### Wins log
```text
Add to my wins log: <what happened>. Phrase it as impact (what changed, for whom, by how much), in one or two lines.
```

### Explain like a colleague
```text
Explain <concept> to me as a smart colleague from a different field: what it is, why it matters, a concrete example, and the common misconceptions.
```

## Making it better

### Turn a repeat into a skill
```text
Make this a skill. I'll probably ask for this again. Use the skill-builder skill.
```

### What could I connect?
```text
What could I connect? Look at my profile and the connections catalog, and show me the five or six connections that would help me most, with one example each of what it would unlock for me. Use the connect-app skill.
```

### Connect an app
```text
Connect my <app> read-only. Use the connect-app skill: research the current best method for my AI tool, ask before installing or signing in, test it with a real question, and document it.
```

### Vault health check
```text
Vault health check. Use the vault-maintenance skill: show me what's broken or messy in one table, then fix it in small batches. Don't delete or move anything until I say yes.
```

### Turn a repeat into a tool
```text
Make this a tool. It's a list or check with one right answer that you've done by hand before. Use the tool-builder skill and follow TOOLS-CONTRACT.md: test first, dry run by default, and show me a run on my real notes.
```

### Ask before doing
```text
Before you start: what would you need to know to do this really well? Ask me first, one question at a time.
```

### Check your work
```text
Check your work: list the claims you made, how you verified each one, and which ones are still unverified.
```

### Learn from today
```text
What did you learn today about how I like to work? Propose one line for PREFERENCES.md or LEARNED.md. Show it before saving.
```

### Prune
```text
Review my setup: which skills or routines haven't I used in a month, and what keeps annoying me? Suggest what to fix, simplify or archive. Don't change anything until I say so.
```

### A mistake happened twice
```text
You made the same mistake twice: <what>. Should we fix it by improving a skill, the vault structure, or (last resort) one short line in AGENTS.md? Propose the smallest fix.
```
