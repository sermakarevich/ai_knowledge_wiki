[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** Top-level files configure the docs-site presentation and exclude build output from version control.
## Key points
- The component covers exactly 2 top-level source files: `.gitignore` and `_config.yml` (`.gitignore:1`, `_config.yml:1`).
- `.gitignore` excludes the `dist` build-output directory from version control (`.gitignore:1`).
- `_config.yml` selects the `jekyll-theme-minimal` Jekyll theme for the project site (`_config.yml:1`).
- `_config.yml` sets the site title to `MichiAI` (`_config.yml:2`).
- `_config.yml` sets the site description to `Full-duplex speech LLM with ~75ms latency.` (`_config.yml:3`).
---
## .gitignore
Excludes build output (`dist`) from version control (`.gitignore:1`):

```
dist
```

## _config.yml
Jekyll site configuration with three keys (`_config.yml:1-3`):

| Key | Value |
|---|---|
| `theme` | `jekyll-theme-minimal` (`_config.yml:1`) |
| `title` | `MichiAI` (`_config.yml:2`) |
| `description` | `Full-duplex speech LLM with ~75ms latency.` (`_config.yml:3`) |

Verbatim excerpt:

```
theme: jekyll-theme-minimal
title: MichiAI
description: Full-duplex speech LLM with ~75ms latency.
```

**Covers:** `.gitignore`, `_config.yml`
