// Mirrors the kit's Markdown (function-catalog.md, prompts). In Astro this is generated at build time.
const A = (e, name, rows) => ({ e, name, items: rows.split('\n').map(r => r.trim()).filter(Boolean).map(r => { const [n, d, l] = r.split('|'); return { n, d, l }; }) });

export const KIT = {
  version: 'v1.1',
  catalog: [
    A('🧭', 'Daily rhythm & focus', `
      Morning briefing|Today's calendar, top 3, what's due, one nudge from your goals|S→M
      End-of-day shutdown|What got done, what moves to tomorrow, clear head|S
      Weekly review|Look back, look ahead, empty the inbox, pick the week's priorities|S
      Monthly / quarterly review|Goals check: what to stop, start, continue|S
      "What should I do now?"|Picks the next task for the time and energy you have|S
      Big-task breakdown|Turns a scary task into 15-minute steps|S
      Procrastination buddy|A gentle push and a 5-minute first step|S`),
    A('🧠', 'Knowledge & second brain', `
      Quick capture + inbox triage|Dump thoughts anywhere; they get sorted weekly|S
      Ask my notes|Answers from your own vault, with links to the notes|S
      Save this|Keeps the useful part of a conversation as a proper note|S
      Article / video / podcast digest|Summary plus why it matters to you|S
      Book notes|Key ideas, quotes, how they apply to your life|S
      Research brief|Compares options with sources and flags uncertainty|S
      Learning plan|A curriculum and weekly practice for any skill|S
      Language practice|Quizzes, reading at your level, conversation practice|S
      Scheduled content digest|Curated news on your topics, daily or weekly|L`),
    A('❤️', 'Partner & relationships', `
      People profiles|Preferences, sizes, dietary needs, important dates, gift ideas|S
      Birthday & anniversary radar|Upcoming dates with gift ideas, early enough to act|M
      Quality-time planner|Date nights and outings that respect your hard constraints|S
      Keep-in-touch nudges|Friends you haven't seen in a while|M
      Event planning|Parties and dinners: guests, menus, timeline|S
      Thoughtful messages|Cards, toasts, apologies, difficult conversations|S`),
    A('👨‍👩‍👧', 'Kids & family', `
      Family week plan|Who's where, when, and who drives|M
      School portal digest|Homework, grades, announcements, deadlines in one summary|M→L
      Test & homework prep|Study guides, practice quizzes, "explain it another way"|S
      Activities & clubs|Schedules, kit lists, fees, sign-up deadlines|S
      Chores & pocket money|A fair system the kids can follow|S
      Curiosity projects|Fun learning projects around the kids' questions|S
      Pet care|Vet records, vaccinations, food, insurance claims|S`),
    A('🍽️', 'Food & household', `
      Weekly meal plan|From what you like, your diet and the season|S
      Shopping list|Generated from the meal plan, grouped by aisle|S
      Recipe adaptation|Dietary swaps, servings, substitutions|S
      Pantry / freezer inventory|Know what you have; use it before it expires|S
      Chore rota|Fair split, visible to everyone|S`),
    A('🏠', 'Home', `
      Home manual|Appliances, models, warranties, manuals, filter sizes|S
      Maintenance calendar|Seasonal jobs and service due dates|M
      Service providers directory|Who fixed what, contacts, would you hire them again|S
      Renovation planner|Scope, quote comparison, timeline, decisions log|S
      Smart-home helper|Design automations, troubleshoot devices|M→L
      Home network & devices|Inventory, Wi-Fi fixes, backups, password-manager hygiene|S
      Moving house|Checklist, address changes, utilities|S`),
    A('💶', 'Money & admin', `
      Subscriptions audit|What you pay for, what to cancel|S
      Bills & renewals calendar|Contracts, insurance, notice periods, deadlines|M
      Budget & spending review|From bank exports: where the money goes|M
      Official letters|Explain, translate, draft a reply|S
      Document filing|Scan → name → file → reminder|L
      Tax-season prep|Checklist of what to gather, by when|S
      Insurance overview & claims|What's covered, how to claim, deadlines|S
      Big-purchase research|Compare, total cost of ownership, decide|S
      Financial "what ifs"|Scenarios to discuss with a professional|S`),
    A('🩺', 'Health & fitness', `
      Training plan|Program and progression for your goals and kit|S
      Nutrition ideas|Meals for your goals and diet|S
      Lab results explained|Plain-language explanation, questions for your doctor|S
      Appointment & screening reminders|Check-ups, dentist, vaccinations|M
      Health log|Symptoms, medication, questions for the next appointment|S
      Habit reflections|Sleep, stress, routines: what's working|S`),
    A('✈️', 'Travel & leisure', `
      Trip planner|Interview, itinerary, booking checklist, plan B for bad weather|S
      Packing lists|Per trip type and per person|S
      Weekend & local ideas|Events, walks, museums, rainy-day options|S
      Restaurant picks|Matching diet, budget, location and mood|S
      Watch / read / play lists|Recommendations from what you loved|S
      Hobby projects|Plans, supplies, progress log|S`),
    A('💼', 'Work: communication', `
      Email triage & drafts|Sorts what matters, drafts replies in your voice|M
      Meeting prep|Agenda, background, questions to ask|S→M
      Meeting notes → actions|Decisions, owners, follow-ups|S
      Difficult conversation rehearsal|Role-play and phrasing|S
      Status updates & reports|From your notes, in the right format|S
      Writing editor|Clearer, shorter, right tone|S`),
    A('🧩', 'Work: thinking & planning', `
      Decision memo|Options, trade-offs, a recommendation|S
      Critical review / red team|Finds holes in a plan or document|S
      Project kickoff|Goals, scope, risks, first plan|S
      Pre-mortem|"It failed. Why?" Then prevention|S
      Research & market scan|With sources and confidence levels|S
      Weekly priorities / OKRs|What matters this week and how you'll know|S`),
    A('📚', 'Work: knowledge & output', `
      Personal work wiki|Glossary, how-tos, who's who|S
      Checklists & SOPs|For anything you do more than twice|S
      Spreadsheet help|Analysis, formulas, charts|S
      Presentations & documents|From your notes to a deck or doc|S
      Proposals & reports|From templates, consistent every time|S
      Onboarding pack|For a new colleague, from your wiki|S`),
    A('🚀', 'Career & growth', `
      CV & profile refresh|Tailored to the role you want|S
      Interview prep|Likely questions, mock interviews, feedback|S
      Wins log & self-review|Never scramble for examples at review time again|S
      Learning roadmap|Skills for your next step, and a plan to get them|S
      Networking follow-ups|Who to thank, who to reconnect with|M`),
    A('🧾', 'Self-employed & small business', `
      Client & lead tracker|A light CRM in your vault|S
      Invoices & expenses|Bookkeeping prep, receipts filed|M→L
      Quotes & proposals|Fast, consistent, from templates|S
      Website & social posts|Drafts in your voice, content calendar|S
      Contracts & deadlines|Renewal dates, obligations, reminders|S`),
    A('🎓', 'Profession playbooks', `
      Teacher|Lesson plans, rubrics, differentiated worksheets, parent emails|S
      Healthcare|Study summaries, admin, patient-friendly explanations (never patient data)|S
      Manager|1:1 prep, feedback drafts, team updates, hiring scorecards|S
      Sales / accounts|Account briefs, call prep, follow-up drafts|S→M
      Creative|Ideation, briefs, critique, mood boards|S
      Engineer / analyst|Code, specs, data analysis, documentation|S→M
      Legal / finance / consulting|Research summaries, comparisons, memo drafts (you verify)|S
      Trades / hands-on|Quotes, job checklists, material lists, client messages|S`),
    A('🛠️', 'Builder track (optional)', `
      Connect your apps|Calendar, email, tasks, cloud drive, read-only first|M
      Small scripts|For lists that must be filtered correctly every time|L
      Scheduled automations|Things that run by themselves: digests, review prep|L
      Dashboards & mini pages|Personal web pages from your data|L
      Your own skills|Turn anything you repeat into a playbook (skill-builder)|S`),
  ],
  prompts: [
    { name: 'Setup', items: [
      ['First contact', `Hi! This folder is my new Obsidian vault, set up from the AI Kickstart kit.
Please read AGENTS.md and _system/index.md (nothing else yet), then tell me in three short lines:
1) what this vault is for, 2) how you'll help me, 3) what we should do first.
Then create a test note at _inbox/hello.md that says "It works!" so I can check that you can write here.`],
      ['Help me with a setup step I\'m stuck on', `I'm on harness step <P0.x> and I'm stuck: <what happened>. I use <Mac / Windows / Linux> and <AI tool>. Explain what to do in plain words, one step at a time, and wait for me after each step.`],
    ]},
    { name: 'Interview', items: [
      ['Start', `Start round 1 of my kickstart interview. Keep it friendly and one question at a time. I may answer by voice.`],
      ['Next round', `Start round <2 / 3 / 4> of my kickstart interview.`],
      ['Express (~20 min)', `I'm short on time. Run the express version of my kickstart interview: rounds 1 and 2 merged, about 10 core questions. Then draft my profile with sensible defaults and put the deep dives in my harness plan for later.`],
      ['Fix my profile', `Read my profile files in _system/profile/ and show me anything that looks wrong, outdated or too vague. Ask me one question at a time to fix it, and show me each change before saving.`],
    ]},
    { name: 'Harness', items: [
      ['The main one', `Continue my harness plan.`],
      ['Status', `Harness status.`],
      ['Capture an idea', `Add to harness: <idea>.`],
      ['New AI tool', `I'm continuing my AI setup in a new tool. Read AGENTS.md, then _system/HARNESS-PLAN.md (the Now table and the last two session-log entries), and tell me where we are and what's next. Don't change anything yet.`],
    ]},
    { name: 'Everyday life', items: [
      ['Morning', `Morning briefing.`],
      ['Sunday', `Weekly review.`],
      ['Keep something', `Save this to my notes: just the decision and why, not the whole conversation.`],
      ['Ask your notes', `What do my notes say about <topic>? Cite the notes, and tell me what's missing.`],
      ['Official letter', `Here's a letter I received (attached). In plain words: what is it, do I need to do anything, and by when? If I need to reply, draft a short, polite reply. Flag anything you're not sure about.`],
      ['Meal plan', `Plan dinners for next week for <who>. Respect everyone's dietary needs from their people profiles, keep weeknights under <30> minutes, reuse ingredients, and give me a shopping list grouped by aisle.`],
      ['Date night / outing', `Plan a date night for <Friday>. Three options, one recommendation.`],
      ['Trip', `Help me plan a trip to <place> around <dates>. Interview me first, one question at a time: who's coming, budget, pace, must-dos. Then draft an itinerary with a plan B for bad weather.`],
      ['Gift', `<Name>'s birthday is on <date>. Using their people profile, suggest 5 gift ideas at around <budget>, ranked, with where to get them. Avoid anything we've given before.`],
      ['Kids\' test prep', `<Child> has a <subject> test on <topic> on <date>. Make a short study plan for the days until then, a one-page summary at their level, and 10 practice questions with answers on a separate page.`],
      ['Home fix', `<Appliance / problem> is <doing what>. Check my home manual notes for the model. Walk me through safe things I can try myself, and tell me when to call a professional.`],
      ['Subscriptions', `Here's a list of my subscriptions / a bank export (attached). Find recurring payments, group them, total them per month and year, and suggest what to cancel or downgrade. Ask me about anything unclear.`],
    ]},
    { name: 'Work (any job)', items: [
      ['Decision memo', `Help me decide between <A> and <B>. Ask me up to 5 questions first. Then write a one-page decision memo: context, options, trade-offs, a recommendation, and what would change your mind.`],
      ['Red team', `Red-team this <plan / document> (attached). What are the 5 most likely ways it fails or gets misunderstood? For each: how likely, how bad, and what would prevent it.`],
      ['Meeting prep', `I have a meeting with <who> about <topic> on <date>. Using my notes on them and the topic, give me: the goal of the meeting, 3 key points, questions to ask, and likely objections with answers.`],
      ['Meeting notes → actions', `Here are my rough meeting notes. Turn them into: decisions, actions (who / what / by when), open questions, and a short follow-up email I can send.`],
      ['Email in my voice', `Draft a reply to this email. Tone: <friendly but firm>. Goal: <what I want to happen>. Keep it under 120 words. Don't send anything, just draft.`],
      ['Big task', `Break "<task>" into 15-minute steps, in order. Mark the first one I can do right now, and anything I need from someone else.`],
      ['Wins log', `Add to my wins log: <what happened>. Phrase it as impact (what changed, for whom, by how much), in one or two lines.`],
      ['Explain like a colleague', `Explain <concept> to me as a smart colleague from a different field: what it is, why it matters, a concrete example, and the common misconceptions.`],
    ]},
    { name: 'Making it better', items: [
      ['Turn a repeat into a skill', `Make this a skill. I'll probably ask for this again. Use the skill-builder skill.`],
      ['Ask before doing', `Before you start: what would you need to know to do this really well? Ask me first, one question at a time.`],
      ['Check your work', `Check your work: list the claims you made, how you verified each one, and which ones are still unverified.`],
      ['Learn from today', `What did you learn today about how I like to work? Propose one line for PREFERENCES.md or LEARNED.md. Show it before saving.`],
      ['Prune', `Review my setup: which skills or routines haven't I used in a month, and what keeps annoying me? Suggest what to fix, simplify or archive. Don't change anything until I say so.`],
      ['A mistake happened twice', `You made the same mistake twice: <what>. Should we fix it by improving a skill, the vault structure, or (last resort) one short line in AGENTS.md? Propose the smallest fix.`],
    ]},
  ],
};
