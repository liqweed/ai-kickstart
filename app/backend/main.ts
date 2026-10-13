// The companion's backend: the only code with file-system access (txiki.js, not Node).
// K11 spike: app config in ~/.ai-kickstart/, one watcher on the vault, events to the page.
// Paths cross the bridge with '/' separators on every OS.

const enc = new TextEncoder();
const dec = new TextDecoder();

const slash = (p: string) => p.replaceAll('\\', '/');
const configDir = slash(tjs.homeDir) + '/.ai-kickstart';
const configPath = configDir + '/config.json';

type Config = { vault?: string };

async function exists(path: string) {
  try {
    await tjs.stat(path);
    return true;
  } catch {
    return false;
  }
}

// Folders the person's tools own: changes there are never "noticed".
const ignored = (rel: string) => /(^|\/)\.(obsidian|trash|git)(\/|$)|(^|\/)\.DS_Store$/.test(rel);

let watcher: { close(): void } | null = null;

export const api: Record<string, TinyApiHandler> = {
  readConfig: async () => {
    if (!(await exists(configPath))) return { path: configPath, config: null };
    return { path: configPath, config: JSON.parse(dec.decode(await tjs.readFile(configPath))) as Config };
  },

  // Write to a temporary file, then rename: a crash never leaves half a config.
  writeConfig: async ({ config }: { config: Config }) => {
    await tjs.makeDir(configDir, { recursive: true });
    await tjs.writeFile(configPath + '.tmp', enc.encode(JSON.stringify(config, null, 2) + '\n'));
    await tjs.rename(configPath + '.tmp', configPath);
    return { path: configPath };
  },

  // One vault at a time. Pushes 'vault-file' with the path relative to the vault.
  watchVault: async ({ vault }: { vault: string }, app: TinyApp) => {
    watcher?.close();
    const root = slash(vault).replace(/\/$/, '');
    watcher = tjs.watch(root, async (file: string, event: string) => {
      const rel = slash(file);
      if (ignored(rel)) return;
      app.push('vault-file', { path: rel, event, exists: await exists(root + '/' + rel) });
    });
    return { watching: root };
  },
};
