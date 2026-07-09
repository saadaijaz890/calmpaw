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
