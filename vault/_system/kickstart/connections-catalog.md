---
tags: [system, kickstart, connections]
type: reference
status: active
created: 2026-10-13
updated: 2026-10-13
summary: Menu of apps and data sources the AI could connect to — what each unlocks, how people usually connect it, where to start and what to watch out for. Used by the connect-app skill and harness P4.
---

# Connections catalog

On its own, your AI only knows what's in your notes and what it can search. Connect it to your calendar and it knows your week. Add maps and it knows how long the drive takes. Add the weather and it knows Saturday's picnic needs a plan B. **Each connection makes every skill a bit smarter**, and two together often unlock something neither could alone (see *Combos* at the end).

This is a menu, not a to-do list. Most people end up with **three to six** connections. Say *"What could I connect?"* and the AI (skill `connect-app`) picks the ones that fit your life, then connects them one at a time, safely. The rules are in [[TOOLS-CONTRACT|the Tools & Connections Contract]], Part B.

## How to read an entry

- **Examples:** common apps in this category. Use whichever you already have. The kit doesn't recommend one over another.
- **Unlocks:** what becomes possible.
- **Try:** a first question to ask once it's connected.
- **Connect via:** the usual ways, best first. The details change often, so the AI looks up the current method for your AI tool when you connect.
- **Start:** the first rung on the ladder: *Export* (a file you download), *Read-only*, *Draft*, *Act*.
- **Risk:** **Low** (public data, nothing personal) · **Medium** (your personal data, read-only) · **High** (money, health, messages to people, other people's data, or the AI can act).
- **Level:** like the function catalog. **S** works with web search alone · **M** needs a connection · **L** needs a small script or a schedule.

**Start here.** The five that unlock the most for most people: **Calendar**, **Tasks & reminders**, **Web search & reading pages**, **Cloud files** and **Weather**.

## 📅 Time & plans

### Calendar
- **Examples:** Google Calendar · Outlook / Microsoft 365 · iCloud Calendar · Proton Calendar
- **Unlocks:** Real morning briefings and weekly reviews. Free-time finder. Prep reminders before important meetings. Conflict spotting across family members. "Leave by" times (with Maps).
- **Try:** "What does my week look like, and where are two hours for deep work?"
- **Connect via:** Built-in connector in your AI app · the calendar's official integration or MCP server · a private read-only calendar link (`.ics`) · export
- **Start:** Read-only
- **Risk:** Medium. Shared calendars contain other people's details. A private calendar link is effectively a password.
- **Level:** M

### Tasks & reminders
- **Examples:** Todoist · Microsoft To Do · Apple Reminders · Google Tasks · Things · TickTick
- **Unlocks:** Briefings that know what's due. Weekly reviews that close loops. Turning meeting notes and letters into dated tasks. "What should I do now?" with real data.
- **Try:** "What's overdue, and which three things matter most this week?"
- **Connect via:** Built-in connector · the app's official MCP server or API · export · or keep tasks as `- [ ]` lines in the vault (no connection needed; `upcoming.py` reads them)
- **Start:** Read-only, then *Act* for adding tasks (small and reversible)
- **Risk:** Low to medium
- **Level:** M

### Subscribed calendars (school terms, holidays, fixtures)
- **Examples:** School holiday calendars · public-holiday feeds · sports club fixtures · waste-collection schedules · a team's match calendar
- **Unlocks:** Holiday planning that knows the school breaks. Reminders for collection days. Family week plans that include fixtures.
- **Try:** "Which school holidays next year overlap with public holidays, and which long weekends can we use?"
- **Connect via:** Subscribe to the `.ics` link in your calendar app (the AI then reads it through your calendar) · or the AI reads the link directly · public-holiday data sources (free, no account)
- **Start:** Read-only
- **Risk:** Low
- **Level:** S

### Contacts
- **Examples:** Google Contacts · iCloud Contacts · Outlook People
- **Unlocks:** Birthday radar for people not yet in your vault. Keep-in-touch nudges. Addresses for cards and invitations.
- **Try:** "Whose birthdays are in the next month that I don't have a note for yet?"
- **Connect via:** Built-in connector (often bundled with mail and calendar) · export (`.vcf`)
- **Start:** Read-only or export
- **Risk:** High. It's other people's data. Store only what you'd be comfortable with them reading (skill `people`).
- **Level:** M

## ✉️ Communication

### Email
- **Examples:** Gmail · Outlook · iCloud Mail · Proton Mail · Fastmail
- **Unlocks:** Inbox triage ("what actually needs me?"). Drafts in your voice. Deadlines pulled from official letters and school emails. Receipts and bookings filed automatically. Travel itineraries from confirmation emails.
- **Try:** "Which emails from the last week need a reply from me, and by when?"
- **Connect via:** Built-in connector · official integration · forwarding selected emails to a dedicated address or folder · export
- **Start:** Read-only, then *Draft*. Sending stays with you.
- **Risk:** High. Email is full of other people's words, and it's the most common place for hidden instructions aimed at AI (contract §12). Keep sending manual.
- **Level:** M

### Messaging apps
- **Examples:** WhatsApp · Signal · Telegram · iMessage · Messenger
- **Unlocks:** Summaries of busy group chats (school class, club, family). Pulling dates and decisions out of a long thread.
- **Try:** "From this exported class chat: what dates, things to bring and decisions did I miss?"
- **Connect via:** Exporting a chat or copying the relevant messages · some apps have unofficial connectors (avoid: they often break the app's rules and put your account at risk)
- **Start:** Export
- **Risk:** High. Other people's private messages. Share only what you'd show a friend helping you.
- **Level:** S

### Meeting transcripts
- **Examples:** Zoom · Microsoft Teams · Google Meet transcripts · voice-memo transcription on your phone
- **Unlocks:** Meeting notes → decisions and actions. Prep from last time's notes. Voice notes turned into tidy inbox notes.
- **Try:** "From this transcript: decisions, owners and deadlines, as a meeting note."
- **Connect via:** The meeting app's transcript download · built-in connector (work plans) · your phone's dictation or voice-memo transcription
- **Start:** Export
- **Risk:** Medium to high. Get consent before recording anyone. Work transcripts: follow your employer's policy.
- **Level:** S

## 📁 Files & knowledge

### Cloud files
- **Examples:** Google Drive · OneDrive · Dropbox · iCloud Drive · Box
- **Unlocks:** "Find the contract with the cancellation clause." Summaries of long documents. Filing scans into the right folders. Spreadsheet analysis. A short `_index.md` in each big folder helps the AI find things there too.
- **Try:** "In my Drive, find our home insurance policy and tell me the excess and the notice period."
- **Connect via:** Built-in connector · official integration · the desktop sync app (the files then sit in a normal folder the AI can read)
- **Start:** Read-only
- **Risk:** Medium to high, depending on what's stored (IDs, tax and medical papers are high)
- **Level:** M

### Notes in other apps
- **Examples:** Notion · Apple Notes · Evernote · OneNote · Google Keep · Bear
- **Unlocks:** One place to search. Old notes brought into the vault, cleaned up and linked (then `vault-maintenance` adds frontmatter and finds duplicates).
- **Try:** "Import my recipes from <app> into 06-reference/recipes/, one note per recipe."
- **Connect via:** The app's Markdown export, then Obsidian's built-in *Importer* plugin · built-in connector (for apps you keep using, e.g. a shared Notion)
- **Start:** Export
- **Risk:** Medium
- **Level:** S→M

### Scans & paperwork
- **Examples:** Your phone's built-in document scanner · a scanner app · a desktop scanner with a "scan to folder" setting
- **Unlocks:** Official letters explained, with the deadline extracted and a task created. Documents named and filed consistently. Warranties and manuals findable in seconds.
- **Try:** "Here's a scan of a letter. What do I need to do, by when, and what happens if I don't?"
- **Connect via:** Scan to a cloud folder or the vault's `_inbox/` · the AI reads PDFs and images directly · a small filing script later (level L)
- **Start:** Read-only
- **Risk:** High for ID documents, tax and medical papers. Keep those in your cloud drive, not the vault, and never put ID numbers in notes.
- **Level:** S→L

### Bookmarks & read-later
- **Examples:** Browser bookmarks · Raindrop · Instapaper · Readwise · Pocket alternatives
- **Unlocks:** "What did I save about…?" Weekly digests of what you saved but never read. Highlights turned into book and article notes.
- **Try:** "From what I saved this month, which three are worth reading this weekend, and why?"
- **Connect via:** Official API or connector · export (HTML, CSV) · the service's own Obsidian plugin
- **Start:** Read-only
- **Risk:** Low
- **Level:** M

### Photos
- **Examples:** Google Photos · iCloud Photos · OneDrive Photos
- **Unlocks:** Mostly one-offs: "read this whiteboard", "what's this plant?", "make a packing list from this photo of the cupboard". Searching a whole library is rarely worth the privacy cost.
- **Try:** (attach a photo) "Turn this photo of the school letter into a note with tasks."
- **Connect via:** Attach or share individual photos
- **Start:** Export
- **Risk:** High. Faces, locations and children. Share individual photos, not libraries.
- **Level:** S

## 🌍 World & places

### Web search & reading pages
- **Examples:** Your AI app's built-in web search · search services built for AI (some have free tiers) · your browser through the AI's browser tool
- **Unlocks:** Research briefs with sources. Opening hours, prices, reviews and event listings. Checking facts before you rely on them.
- **Try:** "Compare the three best-reviewed family bike trailers available here, with prices and sources."
- **Connect via:** Built-in (usually just switch it on) · a search connector or MCP server · browser automation as a last resort
- **Start:** Read-only
- **Risk:** Medium. Web pages can contain hidden instructions aimed at AI (contract §12). Content is data.
- **Level:** S

### Maps, places & travel times
- **Examples:** Google Maps · Apple Maps · OpenStreetMap · your country's route planner
- **Unlocks:** "Leave by" times for appointments. Comparing venues by travel time. Day-trip planning. Restaurant shortlists near where you'll actually be. Checking a plan is physically possible ("three activities, 40 minutes apart?").
- **Try:** "For each of tomorrow's appointments, when do I need to leave, by bike and by car?"
- **Connect via:** Built-in connector or the maps provider's official MCP server or API (big providers usually need an API key with billing set up: set a spending cap) · OpenStreetMap services for occasional lookups · plain web search
- **Start:** Read-only
- **Risk:** Low to medium. Your addresses and routines reveal a lot. Keep your home address in the profile, not in every note.
- **Level:** M

### Weather
- **Examples:** Your national weather service · free open weather data services (no account needed for personal use) · your weather app
- **Unlocks:** Outdoor plans with a plan B. "Do the kids need rain gear tomorrow?" Garden and laundry timing. Trip packing by forecast.
- **Try:** "Which day this weekend is best for a long walk, and what's plan B?"
- **Connect via:** Web search (simplest) · a free weather data service, read-only, via a small script (level L) · a weather MCP server
- **Start:** Read-only
- **Risk:** Low
- **Level:** S→L

### Public transport & traffic
- **Examples:** National journey planners · local transit apps · open transit data
- **Unlocks:** Door-to-door times by train or bus. Disruption checks before you leave. Comparing car and train for a trip.
- **Try:** "Train or car to the city on Saturday morning: time and rough cost each way?"
- **Connect via:** Web search · the journey planner's public API or open data, where your country has one (varies a lot)
- **Start:** Read-only
- **Risk:** Low
- **Level:** S→M

### News & feeds (RSS)
- **Examples:** Newsletters · blogs · news sites · podcasts (most still publish an RSS feed)
- **Unlocks:** A personal digest on your topics, daily or weekly, instead of endless scrolling. Alerts on things you track (a local planning decision, a product release).
- **Try:** "Each Sunday: the five most important things from these ten feeds, two lines each, with links."
- **Connect via:** RSS feeds (free, open, no account) read by a small script on a schedule · web search · built-in connectors for some publishers
- **Start:** Read-only
- **Risk:** Low. Feed content is untrusted data.
- **Level:** L

### Local events & venues
- **Examples:** Cinema, theatre and concert listings · museum agendas · city event calendars · ticketing sites
- **Unlocks:** Date nights and weekend ideas that fit your constraints (skill `quality-time-planner`): times, language, accessibility, distance.
- **Try:** "What's on this Saturday evening within 30 minutes that we'd both like?"
- **Connect via:** Web search · the venue's public listings · a small script when a list must be filtered exactly every time (e.g. showtimes by time window and language)
- **Start:** Read-only
- **Risk:** Low
- **Level:** S→L

## 🎧 Media & reading

### Books & reading
- **Examples:** Goodreads · StoryGraph · e-reader highlights · your library's app · audiobook apps
- **Unlocks:** "What should I read next?" based on what you loved. Book notes from your highlights. Library availability checks.
- **Try:** "From my last ten five-star books, suggest three I haven't read, and say why each fits."
- **Connect via:** Export (CSV) · public profile or RSS feeds some services offer · highlight export tools
- **Start:** Export
- **Risk:** Low
- **Level:** S→M

### Video & podcasts
- **Examples:** YouTube · podcast apps
- **Unlocks:** "Summarise this talk and tell me if it's worth an hour." Notes from lectures and tutorials. Digests of your favourite shows.
- **Try:** "Here's a video link: the five key ideas, and what I could try this week."
- **Connect via:** Transcripts (many videos have them) · the AI's built-in video or audio support · podcast RSS feeds
- **Start:** Read-only
- **Risk:** Low
- **Level:** S

### Music, films & watchlists
- **Examples:** Spotify · Letterboxd · Trakt · streaming watchlists
- **Unlocks:** "What should we watch tonight?" from what you both rated highly. Playlists for a party or a road trip.
- **Try:** "From our watch history, three films for tonight under two hours, available on our services."
- **Connect via:** Export · official API (some need a developer account) · built-in connector where offered
- **Start:** Export
- **Risk:** Low
- **Level:** S→M

## 🏠 Home

### Smart home
- **Examples:** Home Assistant · SmartThings · Apple Home · Google Home · Hue · a robot vacuum's app
- **Unlocks:** Designing and debugging automations in plain words. "Is anything left on?" Energy-hungry devices spotted. Help planning a smart-home upgrade.
- **Try:** "Which lights and plugs were on for more than 8 hours yesterday?"
- **Connect via:** The platform's official MCP server or integration (some home hubs have one built in) · its API with a dedicated, limited key · copy-paste of configs for design help
- **Start:** Read-only. *Act* only for harmless things (lights), never locks, alarms or heating without you.
- **Risk:** High once it can act: it's your physical home.
- **Level:** M→L

### Energy & utilities
- **Examples:** Smart-meter apps · solar-panel apps · your energy supplier's account · water and gas usage exports
- **Unlocks:** Monthly usage reviews. Spotting a broken appliance by its usage. "Was the new contract worth it?" Solar and battery timing.
- **Try:** "From these 12 months of usage: when do we use the most, and what would a dynamic tariff have cost?"
- **Connect via:** Export (CSV) · the device's local integration through your smart-home platform · supplier API where available
- **Start:** Export
- **Risk:** Low to medium. Usage patterns reveal when you're away.
- **Level:** S→L

### Home network & devices
- **Examples:** Your router's app · mesh Wi-Fi apps · a home server or NAS
- **Unlocks:** A device inventory. Wi-Fi troubleshooting. Checking that backups actually ran. Updates nobody remembered.
- **Try:** "From this device list, which ones don't I recognise, and how do I find out what they are?"
- **Connect via:** Copy-paste or export from the admin page · the vendor's official API or MCP server (advanced) · read-only accounts where the device supports them
- **Start:** Export
- **Risk:** High. Admin access to your network. Read-only accounts only, never your main admin login.
- **Level:** L

## 💶 Money & admin

### Bank & card transactions
- **Examples:** Your bank's CSV or spreadsheet export · budgeting apps that link to banks
- **Unlocks:** Where the money goes. Subscription audits. Price creep spotted. Tax-season prep. "Can we afford X?" scenarios to discuss with a professional.
- **Try:** "From this export: recurring payments, what each costs per year, and which I might cancel."
- **Connect via:** **Export files** (strongly preferred) · read-only exports from a budgeting app · never give an AI your banking login
- **Start:** Export
- **Risk:** High. Remove account numbers before sharing an export, and keep the files out of the vault (summaries only).
- **Level:** S→L

### Budget & spreadsheets
- **Examples:** Google Sheets · Excel · budgeting apps with exports
- **Unlocks:** Formulas, charts and categories done for you. Monthly spending reviews. A living budget the AI can update from exports.
- **Try:** "Categorise these 200 transactions with my categories, and show where we're over budget."
- **Connect via:** Built-in connector (cloud spreadsheets) · upload the file · a small script for monthly imports (level L)
- **Start:** Read-only
- **Risk:** Medium to high
- **Level:** S→M

### Receipts, invoices & subscriptions
- **Examples:** Receipt emails · store accounts · app-store subscription lists · a freelancer's invoicing tool
- **Unlocks:** Every subscription in one list with renewal dates (`upcoming.py` reads `renewal:` dates). Warranty lookups. Expense prep for the self-employed.
- **Try:** "From my email: every subscription receipt this year, with price and renewal date."
- **Connect via:** Email connector (read-only) · forwarding receipts to one folder · exports
- **Start:** Read-only
- **Risk:** Medium
- **Level:** M

### Government & tax portals
- **Examples:** Tax authority · municipality · health insurer and pension portals
- **Unlocks:** Letters explained. Deadlines extracted. Checklists of what to gather. Draft replies for you to send.
- **Try:** "Here's the letter (PDF). Explain it, list the deadlines, and draft a reply."
- **Connect via:** Download the letters and documents yourself, then share the files · **never** let an AI log in with your government ID
- **Start:** Export
- **Risk:** High. Identity and money. Never store ID or tax numbers in notes.
- **Level:** S

## 🩺 Health & fitness

### Fitness & health data
- **Examples:** Apple Health · Health Connect (Android) · Garmin · Fitbit · Oura · Strava
- **Unlocks:** Training plans that adapt to how you actually slept and trained. Monthly trends. Questions to bring to your doctor.
- **Try:** "From this export: how did sleep and resting heart rate change over the last three months?"
- **Connect via:** **Export** (most apps offer one) · official API (often needs a developer account) · the app's own AI features
- **Start:** Export
- **Risk:** High. Health data is among the most sensitive. Summaries in the vault, raw exports elsewhere, and delete what you no longer need.
- **Level:** S→L

### Medical records & appointments
- **Examples:** Patient portals · lab results · vaccination records
- **Unlocks:** Lab results in plain words, with questions for the doctor. Appointment and screening reminders. A health log for each family member.
- **Try:** "Explain these lab results in plain words, and what I should ask the doctor."
- **Connect via:** Download the PDF yourself and share it · never automate a patient-portal login
- **Start:** Export
- **Risk:** High. The AI explains; your doctor decides.
- **Level:** S

## 👨‍👩‍👧 Family & school

### School portal
- **Examples:** Your school's parent portal or app (these vary by country and school)
- **Unlocks:** One weekly digest of homework, tests, grades and announcements. Study plans before tests. Deadlines in the family calendar.
- **Try:** "What tests and deadlines are coming in the next two weeks, and what should we start this weekend?"
- **Connect via:** The portal's calendar link or email notifications (easiest) · an official API if one exists · read-only browser access as a last resort (slow and fragile)
- **Start:** Read-only
- **Risk:** Medium to high. It's your children's data. Keep it summarised and private.
- **Level:** M→L

### Family organiser
- **Examples:** Shared family calendars · family to-do and shopping-list apps · chore apps
- **Unlocks:** "Who drives whom on Wednesday?" A Sunday-evening family week plan. Shared shopping lists generated from the meal plan.
- **Try:** "Draft next week's family plan: who's where, who drives, and anything to prepare."
- **Connect via:** The shared calendar (see Calendar) · the list app's connector or API · a shared note
- **Start:** Read-only, then *Draft*
- **Risk:** Medium. Other family members' data. Agree on it together.
- **Level:** M

## ✈️ Travel

### Bookings & itineraries
- **Examples:** Flight, train and hotel confirmation emails · booking sites · airline apps
- **Unlocks:** One itinerary per trip, built from the confirmations. Check-in and passport reminders. Plan B when something is cancelled. Packing lists by destination and weather.
- **Try:** "Build my itinerary for next month's trip from the confirmation emails, with check-in reminders."
- **Connect via:** Email connector (read-only) · forward confirmations to one folder · copy-paste
- **Start:** Read-only
- **Risk:** Medium. Booking references can be used to change your trip, so don't share them publicly.
- **Level:** M

## 💼 Work (check your employer's AI policy first)

### Work chat & email
- **Examples:** Slack · Microsoft Teams · Google Chat · work email
- **Unlocks:** "What did I miss?" catch-ups. Drafts of replies and status updates. Decisions found in long threads.
- **Try:** "Summarise the threads I'm mentioned in since Friday, with what's expected of me."
- **Connect via:** The connector your company approves, often only on business plans · never a personal workaround
- **Start:** Read-only
- **Risk:** High. Company and colleagues' data. Policy first.
- **Level:** M

### Project trackers & code
- **Examples:** Jira · Linear · Asana · Trello · GitHub · GitLab
- **Unlocks:** Weekly status reports from real data. "What's blocked?" Meeting prep from the board. Wins log entries from closed work.
- **Try:** "Draft my weekly status from the items I closed or moved this week."
- **Connect via:** The service's official MCP server or connector (many now have one, some with a read-only mode) · API with a personal token limited to read
- **Start:** Read-only
- **Risk:** Medium to high
- **Level:** M

### Docs & wikis
- **Examples:** Confluence · Notion · SharePoint · Google Workspace for work
- **Unlocks:** Answers with links into the team wiki. Onboarding packs. Spotting outdated pages.
- **Try:** "What does our wiki say about the release process, and is anything contradictory?"
- **Connect via:** Official connector (business plans) · official MCP server
- **Start:** Read-only
- **Risk:** High. Confidential material.
- **Level:** M

### Clients, invoices & accounting (self-employed)
- **Examples:** A CRM · invoicing and accounting software · your business bank's export
- **Unlocks:** A light client tracker. Quote and invoice drafts from templates. Bookkeeping prep with receipts filed. Reminders for unpaid invoices.
- **Try:** "Which invoices are unpaid for more than 30 days, and draft a friendly reminder for each."
- **Connect via:** Export · the software's official API or connector · forwarding receipts to one place
- **Start:** Export or read-only
- **Risk:** High. Client data and money. Drafts only, and you send.
- **Level:** M→L

## 🛠️ Builder

### Automation platforms
- **Examples:** Zapier · Make · n8n · IFTTT · your phone's automation app
- **Unlocks:** The glue between apps that don't talk to each other: "when a receipt email arrives, save the PDF to this folder". Some offer an MCP server, so the AI can trigger your automations.
- **Try:** "Design an automation that saves every invoice attachment from email to my Drive, renamed by date and sender."
- **Connect via:** The platform's own connector or MCP server · webhooks
- **Start:** *Draft*: the AI designs, you build and switch it on
- **Risk:** Medium to high. Automations act without asking. Test them and check their output (harness P6).
- **Level:** L

### Quick capture from your phone
- **Examples:** Obsidian mobile · the share sheet · Shortcuts (iPhone) · automation apps (Android) · email-to-note services · voice notes
- **Unlocks:** Getting thoughts, links, photos and voice notes into `_inbox/` in seconds, wherever you are. The weekly review sorts them.
- **Try:** "Set up a one-tap way to send a voice note from my phone to my vault's inbox."
- **Connect via:** Vault sync to the phone (harness P0.4) · a share-sheet shortcut · emailing yourself into a folder the AI reads
- **Start:** *Act* (it only adds notes to the inbox)
- **Risk:** Low
- **Level:** S→M

### Your computer
- **Examples:** Folders outside the vault · the terminal · desktop apps
- **Unlocks:** Renaming and organising downloads. Converting files. Checking backups. Running the vault tools. Anything a careful assistant could do at your keyboard.
- **Try:** "Sort my Downloads folder: propose a plan, and do nothing until I say yes."
- **Connect via:** A desktop or terminal AI agent (see *Your setup* at ai-kickstart.me/setup/) · its permission settings (allow read-only commands, ask for everything else)
- **Start:** Read-only, one folder at a time
- **Risk:** High. Give agents one folder, not your whole computer. Keep "ask before running" on for anything that changes things.
- **Level:** L

## Combos

Two connections together often unlock more than both alone. Pick one when you have both halves:

| Combo | What becomes possible |
|---|---|
| Calendar + Maps | "Leave by" times for every appointment, and a warning when two are too far apart |
| Calendar + Weather | Outdoor plans with a plan B. "Rain gear tomorrow?" in the morning briefing |
| Calendar + Email | Meeting prep: the last thread with each attendee, and what you promised |
| Email + Cloud files | Receipts, invoices and letters filed and renamed automatically (start with *Draft*: the AI proposes, you file) |
| Email + Tasks | Every deadline in an official letter or school email becomes a dated task |
| School portal + Calendar | Tests and deadlines in the family calendar, with a study plan the week before |
| Bank export + Receipts | A subscription audit with renewal dates and notice periods |
| Fitness data + Calendar | Training plans that adapt to the busy weeks |
| Smart home + Weather + Calendar | "We're away this weekend and it'll freeze: anything to switch?" |
| Event listings + Maps + People | Date nights that match both your tastes and the travel time you'll accept |
| Notes import + vault tools | Years of old notes brought in, with frontmatter, duplicates found and hubs built (`vault-maintenance`) |

## Free public data (no account needed)

Useful to know when building small tools (level **L**). Always check the service's current terms first: free often means *personal, non-commercial and gentle*.

- **Weather:** open weather data services offer free forecasts for personal use, often with an attribution requirement.
- **Public holidays:** open public-holiday data sources cover most countries.
- **Places & addresses:** OpenStreetMap is free and open, but its public search service allows only **occasional** personal lookups (at most one per second, no bulk use). For more, use a paid provider.
- **Calendars:** any `.ics` link (school terms, fixtures, holidays).
- **News & blogs:** RSS feeds.
