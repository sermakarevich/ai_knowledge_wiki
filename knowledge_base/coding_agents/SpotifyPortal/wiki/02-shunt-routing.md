> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Enforced Routing: the Shunt Plugin
**In one sentence:** The shunt Claude Code plugin enforces delegation through hooks, scripts, and skills so routing is automatic, not advisory.
## Key points
- The first try put routing rules in CLAUDE.md, but those rules were advisory only, Claude could ignore them, and every project needed its own copy.
- The current fix is a Claude Code plugin called shunt, which sends work through the Portal CLI (command-line interface) actions registry so it works with any Portal instance that has the AiKA plugin enabled.
- The check-file-size hook watches every Read call and blocks files over a set line limit, by default 350 lines, while small targeted reads pass through.
- The check-bash-read hook catches shell workarounds such as cat, head, tail, less, and more on large files, while piped commands such as filtering with grep pass through as targeted reads.
- The line limit can be changed with SHUNT_MIN_LINES, for example `{ "env": { "SHUNT_MIN_LINES": "500" } }`.
- The bulk-read script wraps each file in XML (eXtensible Markup Language) tags plus a question as a one-shot short-lived call with nothing stored, so follow-ups re-send files for free because the full text goes only to the cheap worker model and never enters Claude context; the code-write script needs a spec plus a required reference file, strips markdown fences, writes straight to disk so Claude never sees the output, and modes resolve own > team > public.
- When a hook blocks a read, the block message points Claude to the /bulk-reader skill with exact call syntax, so even if Claude never read the skill text the costly read stays blocked.
---
## Why advisory routing failed
The first version was a block of routing rules in CLAUDE.md. It told Claude when to delegate large reads and boilerplate writes. The problem was that advice is easy to skip. Claude could ignore the rules when busy, and each project needed its own copy of the same rules. There was no single place that forced the behavior.
## Layer 1 Hooks
Hooks run before every tool call and can stop a costly call before it happens. Shunt registers two hooks that run before tool use. The check-file-size hook fires on every Read call. If the file is longer than the set limit, the hook stops the read and tells Claude to use the /bulk-reader skill instead. Small targeted reads with a narrow range still pass through, so Claude can still fix exact lines. The check-bash-read hook stops shell tricks for reading large files, such as cat, head, tail, less, and more. Piped commands pass through, because a command that filters a file down is also a targeted read. The limit is set with SHUNT_MIN_LINES in the shell profile or `.claude/settings.json`, for example `{ "env": { "SHUNT_MIN_LINES": "500" } }`.
## Layer 2 Scripts
Scripts do the actual delegation. Claude calls a script with named inputs, and the script builds the Portal CLI request, handles errors, and reports token use. For reading, the call looks like this:
`bulk-read --question "What does this service do?" --paths src/Service.java src/Handler.java`
The bulk-read script wraps each file in XML tags and sends the files plus the question to the bulk-reader mode. Each call is one-shot and short-lived, with nothing stored on the server. A follow-up sends the files again. Re-sending is free where it matters because the large text goes to the cheap worker model and never enters Claude context. For writing, code-write sends a spec plus a required reference file to the code-writer mode. The reference file is required because without it the worker writes generic code that fits nothing. The script strips markdown fences and can write the result straight to disk, so Claude never sees the made code.
## Layer 3 Skills
Skills are short guides that tell Claude when and how to call the scripts. When a hook stops a read, the stop message names the /bulk-reader skill and gives the exact call form. This keeps Claude on track at the moment it needs help. If Claude never read the skill guide before, the hook still stops the costly read, so savings do not depend on Claude remembering advice.
## Mode name resolution
Modes are picked by name, without hard server addresses in the plugin. Portal matches names without regard to upper or lower case. It prefers your own mode first, then your team mode, then public modes. This means if you copy the public bulk-reader to make your own version, your copy wins on its own without changing the plugin.
**Covers:** article section "Routing" (Layers 1-3).
