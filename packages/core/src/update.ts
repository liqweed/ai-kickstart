import { parsePlan, type Step } from "./harness.ts";

// Kit updates. A release ships a manifest of every vault file with a hash and
// a kind. The app keeps a baseline (the hashes as installed) per vault, and
// the planner compares baseline, vault and the new manifest to decide, file
// by file, what an update may do. The app only ever replaces or adds files;
// person-owned files get a hand-off prompt for the person's AI instead.

/**
 * - `kit`: the kit's own files (skills, interview rounds, catalogs, contracts, templates, tools). Replaced on update when untouched.
 * - `person`: shipped as a starting point, then the person's (and their AI's) to edit. Never overwritten.
 */
export type FileKind = "kit" | "person";

export interface ManifestFile {
  /** Relative to the vault root, with '/' separators. */
  path: string;
  /** "sha256:<hex>" of the text with line endings normalised to \n. */
  hash: string;
  kind: FileKind;
}

export interface KitManifest {
  version: string;
  files: ManifestFile[];
}

/** path → hash of each kit file as installed in this vault. Stored in `~/.ai-kickstart/`. */
export type Baseline = Record<string, string>;

// Files the person's AI is told to edit (plan, profile, indexes, AGENTS.md's
// skills table, the tools registry) or that hold the person's own answers.
const PERSON_OWNED: RegExp[] = [
  /^AGENTS\.md$/,
  /^_system\/HARNESS-PLAN\.md$/,
  /^_system\/index\.md$/,
  /^_system\/profile\/(?!README\.md$)[^/]+\.md$/,
  /^_system\/kickstart\/answers\//,
  /^_system\/tools\/README\.md$/,
  /(^|\/)_index\.md$/,
];

export function kindOf(path: string): FileKind {
  return PERSON_OWNED.some((re) => re.test(path)) ? "person" : "kit";
}

/**
 * Hash text the way manifests do. Line endings are normalised first, so a
 * file that only changed CRLF ↔ LF (a sync service, an editor) still counts
 * as untouched. Uses WebCrypto: the same in the browser, Node and txiki.js.
 */
export async function hashText(text: string): Promise<string> {
  const bytes = new TextEncoder().encode(text.replace(/\r\n?/g, "\n"));
  const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
  return "sha256:" + Array.from(digest, (b) => b.toString(16).padStart(2, "0")).join("");
}

/** Build a release manifest from the vault template's files. */
export async function buildManifest(version: string, files: { path: string; text: string }[]): Promise<KitManifest> {
  const out = await Promise.all(files.map(async (f) => ({ path: f.path, hash: await hashText(f.text), kind: kindOf(f.path) })));
  return { version, files: out.sort((a, b) => a.path.localeCompare(b.path)) };
}

/** The baseline right after installing (or fully applying) a release. */
export function baselineOf(manifest: KitManifest): Baseline {
  return Object.fromEntries(manifest.files.map((f) => [f.path, f.hash]));
}

/**
 * What an update does to one file:
 * - `update`: a kit file the person never touched, and the release changed it: replace it.
 * - `add`: new in this release and not in the vault: create it.
 * - `conflict`: a kit file the person edited, and the release changed it too: they choose (keep mine · take new · ask my AI to merge).
 * - `merge`: a person-owned file the release changed: never overwritten; their AI gets a prompt with what's new.
 * - `removed`: the person deleted it: leave it gone.
 * - `retired`: the release no longer ships it: leave it in the vault, it's theirs now.
 * - `unchanged`: nothing to do.
 */
export type FileAction = "update" | "add" | "conflict" | "merge" | "removed" | "retired" | "unchanged";

export interface FilePlan {
  path: string;
  kind: FileKind;
  action: FileAction;
}

export interface UpdatePlan {
  to: string;
  files: FilePlan[];
  count: Record<FileAction, number>;
}

/**
 * Sort every file into an action. `vault` holds the current hash of each
 * path the baseline or the release mentions, or undefined when it's missing.
 */
export function planUpdate(input: { baseline: Baseline; vault: Record<string, string | undefined>; next: KitManifest }): UpdatePlan {
  const { baseline, vault, next } = input;
  const files: FilePlan[] = [];
  const shipped = new Set<string>();

  for (const f of next.files) {
    shipped.add(f.path);
    const was = baseline[f.path];
    const now = vault[f.path];
    let action: FileAction;
    if (now === undefined) action = was === undefined ? "add" : "removed";
    else if (now === f.hash || was === f.hash) action = "unchanged";
    else if (f.kind === "person") action = "merge";
    else if (was === undefined) action = "conflict"; // the person already has a different file at this path
    else action = now === was ? "update" : "conflict";
    files.push({ path: f.path, kind: f.kind, action });
  }
  for (const path of Object.keys(baseline)) {
    if (!shipped.has(path) && vault[path] !== undefined) files.push({ path, kind: kindOf(path), action: "retired" });
  }

  const count = { update: 0, add: 0, conflict: 0, merge: 0, removed: 0, retired: 0, unchanged: 0 };
  for (const f of files) count[f.action]++;
  return { to: next.version, files: files.sort((a, b) => a.path.localeCompare(b.path)), count };
}

/** Plan steps the new release adds, for the hand-off prompt (e.g. P4.0 in `HARNESS-PLAN.md`). */
export function addedSteps(oldPlan: string, newPlan: string): Step[] {
  const had = new Set(parsePlan(oldPlan).phases.flatMap((p) => p.steps.map((s) => s.id)));
  return parsePlan(newPlan).phases.flatMap((p) => p.steps).filter((s) => !had.has(s.id));
}
