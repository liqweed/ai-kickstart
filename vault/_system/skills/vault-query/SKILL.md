---
name: vault-query
description: Answer a question from the owner's own notes without changing anything — cite the notes, separate what the notes say from inference, and name what's missing. Use when the owner says "what do my notes say about…", "ask the vault", "did I write down…", "remind me what we decided about…".
---

# Vault query (read-only)

## Steps

1. Read `_system/index.md` to find the right section.
2. Search for the key terms, then open the 3–8 most relevant notes. Don't read the whole vault.
3. Answer in this shape:

```markdown
**Answer:** <2–4 sentences>

**From your notes:**
- <fact> — [[Note name#Heading]]
- …

**My inference (not in your notes):**
- …

**Not in your notes:** <what's missing, if anything, and where it might be found>
```

## Rules

- **Read-only.** Don't edit anything. If the owner wants to keep the answer, hand over to `vault-save`.
- Every factual claim cites a note. If the notes disagree, show both and say which is newer.
- "Your notes don't say" is a good answer. Don't fill gaps from general knowledge without labelling it.
