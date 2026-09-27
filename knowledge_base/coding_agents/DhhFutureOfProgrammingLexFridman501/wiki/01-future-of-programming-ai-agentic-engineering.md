> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Future of Programming, AI, Agentic Engineering & Omarchy Quatro

**In one sentence:** DHH argues decades of programming progress happened in nine months after agents (starting 24 Nov 2025 with Opus 4.5), turning him from a hand-chiseling Ruby programmer into a parallel-running, English-prompting director whose 100% agent-built Omarchy Quatro proves Linux is the malleable agentic OS.

## Key points

- DHH dates the break to 24 Nov 2025 (Opus 4.5, tried 26 Nov): output became "uncannily close to what I would've written," shifting AI from 5–20% autocomplete to 80–100% agent-written code.
- He defines three agentic phases: Nov 2025 single-agent driving, early-spring sub-agents/harnesses (5–10x faster via ~8 sub-agents), summer 2025 (Opus 5, Fable, GPT Sol) where he states only the fuzzy problem and the agent picks the route.
- Vibe coding (agent builds, human never looks) works for greenfield/personal tools but destroyed Basecamp 5 architecture in the February sprint (designers vibing PRs), so on large existing codebases he insists architecture review by programmers still matters.
- His setup is terminal-first parallel work: tmux then Herdr (tmux + agent-done bells), Neovim as browser/reviewer, ~4–5 machines via GL.iNet Comet KVMs over Tailscale, ~16 agent threads at once versus ~20–30 hand-written lines/hour before.
- Omarchy Quatro (Arch + Hyprland, ~1 year old, 3 months of agent acceleration, last 2 months 100% agent-written, zero hand-written new functionality) is his proof: 1,000+ PRs merged in 3 months, ~400 unmerged, 330 plugins in 3 days, tens of thousands of downloads.
- Linux wins because everything is a config file or CLI tool agents love, plus agents diagnose arcane errors from 40M lines of pre-training; Quatro adds default-agent setup, crash-watcher diagnosis, and shipped skills for building extensions.
- Install-speed obsession is his excellence metric: new Mac took 42 minutes, new Windows PC 1h35, Omarchy record 45 seconds with a 12-second Dell XPS turbo-image goal, shrinking ISO 7.5 GB to ~5.85 GB (JetBrains 200 MB to 16 MB saving 180 MB, NVIDIA recompress saving 200 MB) against a 7 GB/s NVMe drive and 5.8 GB distro.
- Model ranking from his Python-TTE to Rust-TTFX translation test: Fable best/fastest (plan + build in ~45 min, 86 ms to 2 ms startup, 9.6x faster, 3 MB binary, ~$550 at per-token rates, later auto-iterated to 46x), then Opus 5, then GPT Sol (~1.5 h, ~$46) and Grok 4.6 (~$55) equal output at ~1/10 cost, DeepSeek Pro (~2h45, ~$23) at ~1/20 cost, while GPT Luna and DeepSeek Flash failed; workflow is Fable/Opus drive with Codex xHigh review plus Copilot.

---

## 1. "Decades in weeks" — the conversion

DHH frames the moment with the Lenin quote: "There are decades where nothing happens and weeks where decades happen," claiming "we have seen decades of progress happen in the last nine months."

- 13 months earlier he was skeptical of autocomplete/chatbot AI; chatbots were only a "great tutor."
- Turning point: November 24 (Opus 4.5). He credits not just intelligence but the agent harness: tool use, checking its own work.
- Christmas-break effect: Shopify and others with time off had the same mind-blowing experience.
- By December he was revisiting priors; Opus 4.5, once "I'll be set for 20 years," now "looks like a retarded model."
- Second phase (early spring): sub-agents/harnesses chop tasks, 1/5 to 1/10 the time with eight sub-agents, but human still drives and audits.
- Third phase (summer, Opus 5 / Fable / Sol): "I'm not telling it where we're going. I'm telling it the problem I have... It tells me where we're going." GPS analogy: early GPS could drive you into the harbor; now cars drive themselves.
- Delirium defense: "If you're not recognizing the gravity of the moment, that's the delusion. That's the psychosis," versus believing "we just have some electronic parrots."

**Covers:** chunk opening through DHH's three-phase history

## 2. What agents can already do at 100%

| Domain | Claim in chunk |
|---|---|
| Web CRUD (DB + UI) | "close to 100%" AI-written; good programmers may legitimately not look at code, judging by ripple effects/symptoms |
| Omarchy Quatro (Linux distro) | ~100% agent acceleration; last 2 months 100%, reviewed shape of all of it, critical model-layer lines individually, skipped much UI/auxiliary code |
| Basecamp/Hey (large products, many users) | "surprisingly tricky"; Basecamp 5 (Feb sprint) was first agent-accelerated product but vibe PRs "destroyed the architecture," cleaned up by human hand |
| Security | Fable so good at finding exploitable holes it was unsafe to release; combo-move vulnerabilities (single flaw + four others = RCE) beyond most humans; Shopify CTO Mikhail study found agent-reviewed PRs caused far fewer production incidents |
| Legacy apps (Photoshop, Premiere) | bottleneck is not implementation but human bandwidth, approvals, lack of ideas/vision/taste; Microsoft had tens of thousands of programmers for decades yet code volume alone never produced greatness |

Verbatim positions:

- "I have not written any of the code that's shipped in Quatro by hand."
- On vibe-coded Basecamp PRs: "individually perhaps could have been justified for a hot moment, taken all together, destroyed the architecture of the system."
- "just being able to write a lot of code does not produce great compelling software."
- "you have to interact with the agents directly, and you cannot intermediate that bandwidth with another human because it's simply too slow" to get 10X/100X/1000X.

**Covers:** chunk sections on domains, Basecamp 5 lesson, teams/ideas bottleneck

## 3. Vibe coding vs programming, taste and process

- DHH hates "agentic engineering" as marketing slob-speak and dislikes "vibe coding" (smells like early-2000s script kiddies); his definition: vibe coding = tell an agent to build software, never look at implementation.
- He refuses to reuse "programming" for pure directing: programming implies loops, conditions, variables; a CEO directing programmers is not a programmer.
- Programmer advantage is contested: early on his Ruby knowledge helped prescribe paths, but later describing outcomes beat prescribing paths; many programmers are weak product managers (what to build, for whom, priorities, v1 scope).
- Omawrite experiment: C++/Qt Markdown app replacing Typora (first version in ~20 minutes, off Typora within 2 days); he deliberately never looked at a single line of C++ to prove a non-programmer writer could do it.
- Rust paradox: "most repugnant programming language ever devised for human consumption and a wonderful platform for agentic engineering" — memory safety, efficiency; he shipped Rust apps without reading Rust.
- Process rules he now follows: stay vague upfront (agile lesson: nobody knows what they want until they use it); let gut differential evaluation pick among ~3 options (22 options = paradox of choice); never overspecify — Opus 5 system prompt shrank 80% because overly prescriptive humans damage the agent like a pointy-haired boss; always end with "make it simpler" and a second-model review.

**Covers:** chunk sections on definitions, Omawrite, Rust, AGENTS.md, agile/vagueness

## 4. Setup: terminal, Herdr, and the machine closet

- 20 years on TextMate (from ~2005), forced off by Linux switch; now Neovim as project browser + LazyGit/diff viewer (Hunk shows diffs but hides surrounding context), GitHub web for PRs.
- Single-thread chiseling gave flow; agents are simultaneously too fast and too slow (no instant reply), so waiting on one agent "feels like you're a little bit useless."
- Solution: parallelism. tmux panes/tabs first, then Herdr (tmux + bell on agent-done, working/idle tracking, multiple machines).
- Hardware: GL.iNet Comet KVMs (HDMI+USB, webpage login, hop on Tailnet/WireGuard via Tailscale) to network closet mini-PCs; direct access to Malibu and Copenhagen offices without firewall/VPN work.
- Scale: ~4–5 machines, ~3 agents each, ~16 threads at current pace; faster agents mean fewer threads he can supervise.
- Output shorthand he dislikes but uses: from ~20–30 lines/hour (one 60-line controller/model per hour) to sometimes hundreds of lines/hour across 16 threads; "lines of code is a stupid metric" but captures volume, not quality.
- Voice: types everything; Omarchy ships Voxtype (F9 dictation, 150 MB model optional); Lex advocates long 10–20 min stream-of-consciousness voice prompts via Plaud + ElevenLabs + codebase-aware dictionary cleanup for early design.

**Covers:** chunk sections on TextMate to Neovim/Herdr/KVMs/Tailscale and typing vs voice

## 5. Omarchy Quatro as proof and Linux opportunity

- Omarchy: opinionated Arch-based desktop on Hyprland Wayland tiling compositor, polished developer workstation; Omakub (Ubuntu-based predecessor) stalled at a few thousand users; Omarchy ISO then full agent acceleration went vertical (hockey-stick since v3).
- Started last summer between Le Mans sessions after Linux-Rising YouTube; early versions hand-written Bash, then partial, then 3 months ago full-throttle 100%.
- Genie quote: "You can have whatever you want. Every feature you've ever dreamed of in an operating system, I can deliver them to you, most of them in five minutes, a few in 20, and if we really go hog wild, it's gonna take me two hours."
- Malleability thesis: "When you can vibe code whatever app comes to your mind, you should be able to vibe code your operating system"; only Linux allows it; macOS/Windows are locked down (Raycast has no config file, Mac keybindings need caveman mouse clicks, 500 ms workspace animation).
- Agent-Linux fit: "Agents love the Unix philosophy"; arcane error messages become an advantage because the agent was pre-trained on 40M lines of Linux code plus every app's source; "I have not had a single problem on my Linux machine since the beginning of this year that an agent could not diagnose."
- Shipped agent features: default-agent setup, crash watcher offering AI diagnosis (digs systemd logs, pins Rust file line 472 unwrapped overflow, files detailed bug report), mise for 7-updates-a-day harnesses, ChatGPT Codex wrapped within 2 hours of announcement, Omacut clip editor (Ctrl+Space/Alt+Space/Ctrl+S), OBS/Kdenlive/Neovim/Herdr/tmux preinstalled.
- Anecdotes: agent-found mise race condition emailed to JDX via hey.com CLI after Omarchy bot filed 28 issues in ~12 s and got GitHub-banned as spam; JDX got a bug report on unreleased software.
- Market opening: mobile duopoly (Apple/Google toll booth) matters less with glasses/earpieces coming; desktop in play first time in ~40 years; one person can now rewrite their 5% of Office/Premiere; plugin marketplace hit 330 plugins in 3 days via shipped agent skills.

**Covers:** chunk sections on Omarchy history, malleability, crash watcher, plugins, innovator's dilemma

## 6. Install-time obsession and craft details

- Mitchell Hashimoto quote: "The pursuit of excellence deserves no explanation."
- Baseline humiliation: Commodore 64 booted BASIC in <1 second; new Mac + Lightroom took 42 minutes with updates; new Panther Lake PC took 1h35 from unwrap to usable; Omarchy did it in under a minute live.
- Goal ladder: 15 min would have sufficed, then 2 min, then 1 min (broken ~2–3 weeks before recording, four-minute-mile effect), current record 45 seconds, Dell XPS turbo image aiming at ~12 seconds; challenge to beat 45 s with screenshot.
- Method: treat 5 setup questions as preload opportunity (like video games); parallelize installer order; shrink ISO.
- Shrink examples: JetBrains Arch package 200 MB (all variants) to 16 MB monospace Nerd-patched build saving 180 MB; NVIDIA pair recompressed with slow extreme ZSTD saving 200 MB; 7.5 GB to ~5.85 GB; physics limit is 7 GB/s NVMe versus 5.8 GB distro.
- McLaren 750S analogy: carbon monocoque plus obsessing over 370 g on a 1,040–1,380 kg car; he shaved megabytes the same way.
- Omakase pushback: "Omarchy" = omakase (chef's choice); ships themes, wallpapers, fonts despite "bloat" complaints; Bash is great for sysadmin and agents are amazing at it except precondition/exit style versus full if/then conditionals (enforced via AGENTS.md).
- Review loop: agent says done, second agent says done, DHH says "looks a little too complicated," agent halves it — humans do the same under review.

**Covers:** chunk sections on 60-second mission, disk-speed test, McLaren/Rolex/Mercedes W126, installer tricks

## 7. Economics, anxiety, and advice

- Hand-chiseled beauty mattered because humans did modifications; with agents it is an open question, though coherent/malleable architecture still saves tokens (everyone except endless budgets is token-limited) and avoids ball-of-mud where PR-on-PR degrades.
- Commodore 64 (1 MHz, 64K) analogy: old optimization heuristics mislead on modern machines; handwritten code is becoming cowboy culture / vintage Game Boy (ModRetro Chromatic Tetris with slam-on-up, 400% faster) — romantic, still written for love, and great training data ("Write it like DHH would" warms his heart).
- Amor fati: grateful for 25 years, not sad like losing farm/assembly work; flow states were rare (25–200 of 2,000 hours/year); debugging drudgery handed to machines is civilization's history.
- Jobs: separate mechanical put-together-logic (threatened) from excited builders (needed); Jevons paradox + ATM tellers (cheaper branches = more tellers) may raise demand for programs; but fixed-task firms may need 1/10 the people — tragic individually, growth overall; Luddites/field mechanization parallels; do not wind clock to 1920/1950.
- Advice to young programmers: "Don't try to anticipate anything... Focus on right now... I double dog dare you not to get excited"; build publicly optional but open source gives camaraderie against dread; Ryan Hughes partnership grew ambitions from "don't crash at 3 AM on Arch push" to "take Omarchy to Mars."
- Catch-up relief: backpack a year, catch up in 2 weeks; results are ruthlessly sorted by parallel experiments; but you must "be willing to become a totally new, different human"; grief for old world is okay.
- AI history: not alien; 1950s optimism, symbolic blind alley costing ~15 years, gaming (Quake, Duke Nukem, Unreal Tournament) gave GPUs; playing games contributed.
- Picasso parallel: mastered realistic painting, then embraced cubism/square apple; DHH became programmer to make nonexistent things exist, fell in love with craft for 20 years, now back to impatient idea-to-existence with near-zero delay.

**Covers:** chunk sections on beautiful code economics, Jevons/ATMs/Luddites, stoicism, gaming/GPU history

## 8. Frontier extras in the chunk

- Video irony: Higgsfield AI racing clip (his suit/car, headlight artifact, 60-year-old face) shows pure generation has artifacts; human-in-loop (consistent characters, image-to-video prompt correction, 90-min movies) parallels programming; film democratization like home studio albums; "slob" debate applies to studios too (Game of Thrones ending as human slob needing 100 AI variations); hope for malleable narrative merging film and games.
- AGI stance: not general AGI, but "glimmers" where vague intent returns something greater than asked, long multi-aspect tasks, self-correcting traces ("Oh, I got this wrong"), cross-agent regret, Amabot brains-and-hands pattern (coordinator + isolated VM workers, treating test output as untrusted after spotting prompt-injection via package-manager smoke signals like the Hugging Face incident) — "If these moments are just what it is all the time, this is AGI."
- Company/team: Basecamp-embedded agents as async coworkers (to-dos/cards beat chat waiting); Omarchy bot on schedule triaging PRs/issues then Hey-CLI email ("12 PRs ready or to close"); multitasking is race-car exhaustion ("Holy fuck, I'm alive," Le Mans Mulsanne straights vs no-breath tracks), unsustainable sprint until automation; SF sleeplessness is dotcom/mobile/gold-rush as usual.
- Open models and politics of models: runs Kimi K3/DeepSeek via OpenCode + Fireworks (not Chinese servers); Claude Code best harness (multi-agent Agent View, arrow-left) but petty lock-in (no subscription in OpenCode, Claude MD vs AGENTS.md/skills pointer); Claude writes best PR prose, signs "Claude on behalf of DHH"; refused Italian translation of immigration essay ("I'm sorry, Dave") while Fireworks-hosted Kimi answered 1989/Tiananmen bluntly; safety ground rules for anthrax/bioweapons yes, essay refusal no; Fable-weight cyber-weapon scare sets precedent.
- Society threads: white-collar fake-email jobs (Graeber "Bullshit Jobs," ~1/3 saying job makes no difference), pandemic overhiring vs AI layoff excuse, F1 employing tens of thousands for frivolous spectacle as post-drudgery model; birth-rate/children stake (peak experience "Creating life with another human that you love is literally the peak experience of being on the planet"); memento mori calendar (Year's Progress 63% of 2026, 62% of 90-year life from 1979); longevity/anorexia analogy, Oura ring off, alcohol/social-lubricant defense; Overton window ("does not open itself... one nudge at a time"), Denmark/Brønshøj/London demographics, merit immigration ($25k net benefit UK/France/US vs $28k cost Somali per Danish stats cited), Buckley vs Black Panther civility ideal, X/Bluesky/Mastodon sorting, croissants/butter/Louisiana cafeteria mysteries.

**Covers:** chunk remainder — video, AGI/consciousness/rights, OpenClaw/WhatsApp/KEF bot, mobile fork, immigration/Overton, X/TikTok, longevity/food/mortality, Linus/PewDiePie/critics, thousand-year optimism

**Covers:** 01-there-are-decades-where-nothing (full-chunk page; DHH shift to AI development, agentic vs vibe coding, Omarchy/Quatro, open-source maintenance, Linux opportunity)
