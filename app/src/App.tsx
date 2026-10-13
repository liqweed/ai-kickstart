import { useEffect, useState } from 'react'

// K11 spike: one row per thing the stack must prove on macOS and Windows.
// Each row turns ✓ when the app has seen it work, not when it was attempted.

type Status = 'todo' | 'ok' | 'fail'
type Noticed = { path: string; event: string; exists: boolean }

const inApp = typeof tiny !== 'undefined'
const HELLO = '_inbox/hello.md'

export default function App() {
  const [vault, setVault] = useState<string | null>(null)
  const [configPath, setConfigPath] = useState<string | null>(null)
  const [watching, setWatching] = useState(false)
  const [noticed, setNoticed] = useState<Noticed[]>([])
  const [obsidian, setObsidian] = useState<Status>('todo')
  const [error, setError] = useState<string | null>(null)

  const css: Status = getComputedStyle(document.documentElement).getPropertyValue('--accent') ? 'ok' : 'fail'
  const hello = noticed.some((n) => n.path === HELLO && n.exists)

  const fail = (e: unknown) => setError(e instanceof Error ? e.message : String(e))

  async function openVault(path: string) {
    setVault(path)
    setNoticed([])
    const { path: written } = await tiny.api.call('writeConfig', { config: { vault: path } })
    setConfigPath(written)
    await tiny.api.call('watchVault', { vault: path })
    setWatching(true)
  }

  useEffect(() => {
    if (!inApp) return
    const off = tiny.api.on('vault-file', (n: Noticed) => setNoticed((all) => [n, ...all].slice(0, 5)))
    tiny.api
      .call('readConfig')
      .then(({ config }) => config?.vault && openVault(config.vault))
      .catch(fail)
    return off
  }, [])

  async function choose() {
    const path = await tiny.dialog.pickFolder()
    if (path) await openVault(path).catch(fail)
  }

  async function openObsidian() {
    if (!vault) return
    try {
      await tiny.app.shell.open('obsidian://open?path=' + encodeURIComponent(vault))
      setObsidian('ok')
    } catch (e) {
      setObsidian('fail')
      fail(e)
    }
  }

  if (!inApp) return <main className="spike"><p>Open this page with <code>tinyjs dev</code>.</p></main>

  return (
    <main className="spike">
      <p className="kk-eyebrow">K11 spike · {tiny.system.os()}</p>
      <h1>Does the stack work here?</h1>

      <ol className="spike__checks">
        <Check status={vault ? 'ok' : 'todo'} title="Pick a folder">
          {vault ? <code>{vault}</code> : 'Choose any folder to stand in for a vault.'}
          <button className="kk-btn kk-btn--line" onClick={choose}>Choose folder…</button>
        </Check>
        <Check status={configPath ? 'ok' : 'todo'} title="Write ~/.ai-kickstart/">
          {configPath ? <code>{configPath}</code> : 'Written when a folder is chosen.'}
        </Check>
        <Check status={hello ? 'ok' : 'todo'} title="Notice a new file">
          {watching ? <>Create <code>{HELLO}</code> in the folder.</> : 'Starts once a folder is chosen.'}
          {noticed.length > 0 && (
            <ul className="spike__log">
              {noticed.map((n, i) => <li key={i}><code>{n.event}</code> {n.path}{n.exists ? '' : ' (gone)'}</li>)}
            </ul>
          )}
        </Check>
        <Check status={obsidian} title="Open an obsidian:// link">
          Opens the folder as a vault. ✓ means the system accepted the link; check that Obsidian came forward.
          <button className="kk-btn kk-btn--line" onClick={openObsidian} disabled={!vault}>Open in Obsidian</button>
        </Check>
        <Check status={css} title="Load kickstart.css">
          {css === 'ok' ? 'The shared tokens are applied (light and dark follow the system).' : 'The tokens did not load.'}
        </Check>
      </ol>

      {error && <p className="kk-note" role="alert">{error}</p>}
    </main>
  )
}

function Check({ status, title, children }: { status: Status; title: string; children: React.ReactNode }) {
  const mark = { todo: '○', ok: '✓', fail: '✕' }[status]
  return (
    <li className="kk-card spike__check" data-status={status}>
      <span className="spike__mark" aria-hidden="true">{mark}</span>
      <div className="spike__body">
        <strong>{title}<span className="kk-sr"> ({status})</span></strong>
        {children}
      </div>
    </li>
  )
}
