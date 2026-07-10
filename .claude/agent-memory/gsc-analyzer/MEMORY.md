# GSC Analyzer Agent Memory

## 2026-07-09: Sitemap canonical-URL bug found and fixed
- sitemap.xml was submitting 127/159 URLs with `.html` suffixes (from seo-tools.py's
  `discover_pages()` using raw file paths) while every page's own `<link rel="canonical">`
  tag declares the extensionless URL. Google indexed the canonical (clean) URL but the
  sitemap kept pointing at the non-canonical `.html` version, so GSC's sitemap panel showed
  "0 indexed" for years despite pages actually ranking (confirmed via URL Inspection —
  several pages showed `coverageState: "Submitted and indexed"` on the clean URL and
  `"Alternate page with proper canonical tag"` on the .html duplicate).
- Fixed in `seo-tools.py`: added `clean_url_for(rel)` helper, used by `discover_pages()`.
  Also fixed `generate_blog_index()` and `add_related_posts()` which were internally
  linking to the `.html` duplicates (contributing to the duplicate-content signal).
- Resubmitted sitemap.xml via GSC API after the push.
- Baseline traffic at time of fix (2026-01-01 to 2026-07-07, sc-domain:anxietyfreepups.com):
  ~69 distinct pages with impressions in that window, ~45 total clicks over ~6 months.
  Top performers by clicks: australian-shepherd-clingy-behavior-solutions (5),
  french-bulldog-puppy-crate-training (4), cavalier-king-charles-spaniel-clingy-behavior-solutions (3).
  Top performers by impressions (low CTR, worth title/meta refresh): guides/dog-calming-products
  (1326 impr, pos 60.6 — too low-ranked for the impressions it gets), guides/thundershirt-review
  (1179 impr, pos 32.6), guides/nighttime-anxiety.html (808 impr — wait, check this is now the
  clean URL post-fix), guides/separation-anxiety (286 impr, pos 69.4 — very low rank despite volume).
- Action for next sessions: re-check `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS` indexed count —
  should start climbing from 0 within days of the fix. If it doesn't move after ~2 weeks,
  the issue is deeper (e.g. hosting not actually serving clean URLs consistently — verify
  live, since _redirects/_headers in repo root are Netlify/Cloudflare Pages syntax but the
  site's response header self-reports as GitHub Pages — that mismatch is unconfirmed/unresolved,
  worth double-checking actual deploy target).

## 2026-07-09 (later same day): CRITICAL — calmpaw was never deployed
Discovered during 3-hourly check that `calmpaw` (this repo) is NOT the live site. The
actual production repo is `saadaijaz890/saadaijaz890.github.io` (has the CNAME for
www.anxietyfreepups.com, last pushed 2026-03-17). It has its own separate, human-gated
4-phase publishing system (researcher/writer/linker/publisher agents, documented in its
own CLAUDE.md) that a later session never knew about — instead building the whole
ceo-agent/daily-routine/content-agent.py pipeline in this disconnected `calmpaw` repo.
This explains the GSC sitemap showing 0 indexed far more than the URL bug alone: the
live site's sitemap.xml was untouched, still the pre-fix version, months after my
earlier "fix" commits here — because those commits never reached production.
calmpaw has ~21 more blog posts, 9 more guides than live. A sync was proposed to the
user (bulk copy calmpaw's content into saadaijaz890.github.io) but NOT executed —
blocked by the safety classifier and awaiting explicit user confirmation, since it would
overwrite live production content. **Do not attempt this sync autonomously.** Do not
keep publishing new content into `calmpaw` until the user decides how to reconcile the
two repos — it just adds to content that may never go live.

## 2026-07-10 pulse check
Sitemap unchanged: still 127 submitted / 0 indexed, lastDownloaded/lastSubmitted still
2026-07-09T19:06 — as expected, since the repo-reconciliation question (calmpaw vs.
saadaijaz890.github.io) is still unresolved and no fixes have reached production.
Clicks 2026-07-03 to 07-07: 1, 0, 0, 0, 1 (2 total over 5 days) — flat, consistent with
pre-fix baseline. No new errors/warnings. No action taken (per policy — blocked on
user's repo-reconciliation decision).
