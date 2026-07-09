# CEO Agent Memory

## Site: anxietyfreepups.com

## Session Log
- 2026-06-13: First strategic session. Site at 129 pages (27 guides, 18 breed pages, 82 blogs). Top priority: seasonal July 4th fireworks + medication-timing guide (3-week indexing window). Secondary: begin Gen1 breed rewrites (french-bulldog first). Gen1 debt: 5 pages remaining. Health YELLOW.
- 2026-07-09: Corrected stale debt list (see below — this file wasn't updated when work actually happened). Also: fixed a real sitemap/canonical-URL bug that had suppressed indexing sitewide since launch (see gsc-analyzer memory) — this is likely the actual reason traffic has stayed near zero, more so than content quality. Monetization is now Amazon-only (Chewy affiliate links/mentions removed site-wide per owner instruction — do not add Chewy links going forward).

## Seasonal Content Calendar
- July 4th fireworks: PUBLISH BY JUNE 20 (missed this year's window — plan for New Year fireworks repurpose in December, and get July 4 2027 content ready by June 2027)
- Back-to-school separation anxiety: prepare by late August
- Spring grooming: peak April-May (queue for Feb 2027)
- Spring rescue/adoption: peak March-April (queue for Feb 2027)

## Gen1 Breed Debt — CORRECTED 2026-07-09
The 2026-06-13 debt list (corgi, chihuahua, pitbull, french-bulldog, pug) was never
updated as work happened. Actual status as of 2026-07-09 (checked via FAQPage schema
presence + warning-box presence + line count, not just the stale list):
- french-bulldog.html: Already Gen2 quality (dateModified 2026-06-13, full FAQ schema,
  BOAS-specific content, warning-box). NOT debt. Minor: canonical tag missing www
  (https://anxietyfreepups.com/... vs og:url's https://www.anxietyfreepups.com/...) —
  worth fixing for consistency but low priority.
- corgi.html, chihuahua.html: dateModified 2026-03-09, DO have FAQPage schema and
  warning-box already. Decent, not urgent, but older than the Gen2 standard — could use
  a content-depth pass eventually, not top priority.
- pug.html: UPGRADED 2026-07-09. Added FAQPage schema, ImageObject, warning-box,
  Signs & Symptoms section, removed deprecated breed-switcher widget, fixed .html
  internal links to canonical URLs.
- pitbull.html: STILL genuinely Gen1 — no FAQPage schema, no warning-box (verified
  2026-07-09). This is the one real remaining rewrite. Next up.

**Before touching any "debt" page in future sessions: check for FAQPage schema and
warning-box class presence directly (grep the file) rather than trusting this list's
prose — it goes stale.**

## Strategic Notes
- Topic clusters to build: puppy anxiety, senior dog anxiety, medication mini-cluster (August: trazodone/gabapentin/fluoxetine)
- Position 5-15 quick-win candidate: melatonin-vs-ltheanine-vs-cbd-dogs.html
- Universal affiliates (Amazon only — no Chewy): VetriScience Composure, Adaptil, Thundershirt, Kong Classic, Zylkene
- Blog template fatigue: pivot next wave to symptom-first / scenario-first.
- content-agent.py needs OPENROUTER_API_KEY — now set in .env (2026-07-09, owner-provided).
  Network note: if running in a sandboxed/cloud session with an egress allowlist, openrouter.ai
  may be blocked (403 at the proxy CONNECT level, not an OpenRouter-side error) — check that
  before assuming the key is bad. Works fine unrestricted (e.g. local machine).

## Strategic Observations (rolling)
- 2026-06-13: Blog count (82) exceeds guide count (27) by 3x — content mix is blog-heavy. Prioritize guide-tier authority pieces next.
- 2026-06-13: Medication coverage is thin (3 guides) vs. clear search demand — most promising unbuilt cluster.
- 2026-07-09: Root-cause traffic bottleneck was technical (sitemap submitting non-canonical URLs, ~127/159 pages showing 0 indexed), not primarily a content-quality problem. Fixed. Re-evaluate whether Gen1 rewrites are still the top lever once indexed count recovers over the next 1-2 weeks, or whether it was mostly a crawl/indexing ceiling all along.
