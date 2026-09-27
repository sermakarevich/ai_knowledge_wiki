> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Top-level files

**In one sentence:** Repo-level hygiene plus Windows packaging: line-ending and binary rules, ignores for build/model/runtime artifacts, and a Windows-only build script that embeds the orb-rendered icon into the executable.

## Key points

- `.gitattributes` forces every text file to LF in the repo via `* text=auto`, so a clone on another OS or in CI cannot rewrite line endings and turn a one-line change into a whole-file diff (.gitattributes:12).
- `.gitattributes` marks `*.ico`, `*.png`, and `*.icns` as `binary` because `text=auto` would otherwise guess "text" and corrupt the rendered icons by rewriting line endings inside the image data (.gitattributes:18).
- `.gitignore` excludes the Rust build output (`/target`) and wingman's own state directory (`.wingman/`, holding its index, sessions, and memory) (.gitignore:25, .gitignore:44).
- Model weights fetched by `scripts/fetch-models.ps1` — `/models/*.onnx`, `/models/*.onnx.json`, `/models/*.bin`, plus `/piper/` and `/whisper/` (~6 MB of weights) — are ignored as fetched artifacts, not source (.gitignore:29).
- Files IRA writes at runtime are ignored: `/transcript.jsonl` (the record of conversations), `/ira.log` (written when she starts from a shortcut and closes her own console; see `src/console.rs`), and `/ira.local.db` plus its `-journal` (this machine's URLs and model ids written by the settings window — not keys, which go to the OS keyring) (.gitignore:33, .gitignore:36, .gitignore:41).
- Release-packaging outputs built by `.github/workflows/release.yml` into the working directory (`/*.msi`, `/*.deb`, `/*.dmg`, `/IRA.app/`, `/*.iconset/`) are ignored (.gitignore:47).
- `build.rs` does nothing except on Windows (`#[cfg(windows)]`): it re-runs when `assets/ira.ico` changes and embeds that icon via `winresource::WindowsResource::set_icon`, because Windows reads taskbar/alt-tab/Explorer/Start-menu icons out of the binary itself, so a shortcut-level icon would still leave a generic gear everywhere else (build.rs:71, build.rs:75).
- A missing resource compiler is a warning, not a fatal error: if `res.compile()` fails (needs `rc.exe` from the Windows SDK), the build emits `cargo:warning=no icon embedded` and still produces an IRA with a plain icon (build.rs:79).

---

## Line endings and rendered icons (`.gitattributes`)

Verbatim (`.gitattributes:9`):

```
* text=auto
```

Verbatim binary guards (`.gitattributes:17`):

```
*.ico binary
*.png binary
*.icns binary
```

The icons are rendered by the ignored `render_the_icon` test in `src/orb.rs` (`.gitattributes:16`).

## Ignored build, model, runtime, and release artifacts (`.gitignore`)

| Pattern | Why it is ignored |
|---|---|
| `/target` | Rust build output (.gitignore:25) |
| `/models/*.onnx`, `/models/*.onnx.json`, `/models/*.bin`, `/piper/`, `/whisper/` | Fetched by `scripts/fetch-models.ps1`, ~6 MB of weights, not source (.gitignore:29) |
| `/transcript.jsonl` | Written by IRA at runtime — a record of conversations, not source (.gitignore:33) |
| `/ira.log` | Written when started from a shortcut and she closes her own console; see `src/console.rs` (.gitignore:36) |
| `/ira.local.db`, `/ira.local.db-journal` | Written by the settings window: this machine's URLs and model ids (keys go to the OS keyring); per-machine, unlike shareable `ira.toml` (.gitignore:40) |
| `.wingman/` | `wingman serve` keeps its index, sessions, and memory here (.gitignore:44) |
| `/*.msi`, `/*.deb`, `/*.dmg`, `/IRA.app/`, `/*.iconset/` | Built by `.github/workflows/release.yml` into the working directory (.gitignore:47) |

## Windows icon embedding (`build.rs`)

`assets/ira.ico` is rendered from the orb by an ignored test in `orb.rs`, so the icon and the thing on screen cannot drift apart (build.rs:64). Verbatim build body (build.rs:67):

```rust
fn main() {
    #[cfg(windows)]
    {
        println!("cargo:rerun-if-changed=assets/ira.ico");
        let mut res = winresource::WindowsResource::new();
        res.set_icon("assets/ira.ico");
        if let Err(e) = res.compile() {
            println!("cargo:warning=no icon embedded ({e})");
        }
    }
}
```

A Linux build has neither a resource compiler nor resources, and wants neither (build.rs:70).

**Covers:** `.gitattributes`, `.gitignore`, `build.rs`; grounded in chunk `02-top-level-files.md` lines 1-84.
