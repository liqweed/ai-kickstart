import { slug } from "./text.ts";

export interface Prompt {
  id: string;
  label: string;
  /** Optional one-line note shown under the label ("Rounds 1 and 2 merged"). */
  note?: string;
  text: string;
}

export interface PromptGroup {
  id: string;
  name: string;
  prompts: Prompt[];
}

/**
 * Parse a prompt library: `## Group`, then per prompt `### Label`, an optional `> note` line,
 * and the prompt itself in a fenced code block.
 */
export function parsePrompts(md: string): PromptGroup[] {
  const groups: PromptGroup[] = [];
  let group: PromptGroup | null = null;
  let prompt: Prompt | null = null;
  let fence: string[] | null = null;
  for (const line of md.split(/\r?\n/)) {
    if (fence) {
      if (/^```\s*$/.test(line)) {
        if (prompt) prompt.text = fence.join("\n");
        fence = null;
      } else fence.push(line);
      continue;
    }
    let m: RegExpMatchArray | null;
    if ((m = line.match(/^##\s+(.+?)\s*$/)) && !line.startsWith("###")) {
      group = { id: slug(m[1]), name: m[1], prompts: [] };
      groups.push(group);
      prompt = null;
    } else if ((m = line.match(/^###\s+(.+?)\s*$/)) && group) {
      prompt = { id: `${group.id}/${slug(m[1])}`, label: m[1], text: "" };
      group.prompts.push(prompt);
    } else if ((m = line.match(/^>\s*(.+)$/)) && prompt) {
      prompt.note = m[1].trim();
    } else if (/^```/.test(line)) {
      fence = [];
    }
  }
  return groups;
}

export type Segment = { kind: "text"; value: string } | { kind: "slot"; name: string };

/** Split a prompt into plain text and `<placeholder>` slots. */
export function splitPlaceholders(text: string): Segment[] {
  const out: Segment[] = [];
  const re = /<([^<>\n]+)>/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push({ kind: "text", value: text.slice(last, m.index) });
    out.push({ kind: "slot", name: m[1] });
    last = re.lastIndex;
  }
  if (last < text.length) out.push({ kind: "text", value: text.slice(last) });
  return out;
}
