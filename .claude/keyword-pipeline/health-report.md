# Site Health Report — 2026-06-13

| Page | Status | Title Found |
|------|--------|-------------|
| Homepage (`/`) | ✅ | yes |
| Guides (`/guides/`) | ✅ | yes |
| Breeds (`/breeds/`) | ⚠️ | no |

## Issues Found

- **`/breeds/` — 404 Not Found (GitHub Pages)**
  - The page returns a GitHub Pages "Page not found" error (HTTP 301 → 404).
  - The `<title>` reads: `Page not found · GitHub Pages`
  - Body size is ~9 KB (GitHub Pages default 404 page only — no site content).
  - Action required: Confirm the `/breeds/` directory and `index.html` exist in the repo and have been pushed. If the page hasn't been created yet, add a placeholder or remove any links pointing to it.

## Notes

- Homepage title: `Dog Anxiety Help — Vet-Backed Calming Guides & Product Reviews | AnxietyFreePups` (55 KB of content — healthy)
- Guides title: `All Dog Anxiety Guides | AnxietyFreePups` (17 KB of content — healthy)
- New article (`guides/how-early-dog-anxiety-meds-fireworks.html`) skipped per instructions — allow extra time for GitHub Pages deployment.
- WebFetch returned ECONNREFUSED for all three URLs; status confirmed via curl with redirect-following (`-sL`).
