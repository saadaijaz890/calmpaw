# Site Content Auditor Memory

## Breed Page Quality Tiers (confirmed March 2026)

### Generation 1 — Critical/thin (corgi, chihuahua, pitbull)
- ~300-350 words of actual body content
- Identical boilerplate: "Their natural temperament and breed history make them particularly sensitive to stress triggers. Understanding the root cause is the first step to solving it."
- Identical tip box: "[Breed]-specific anxiety often responds best to a combination of pressure therapy (Thundershirt) and calming supplements. Single-product solutions rarely work for this breed."
- Same 3 products (Thundershirt, Adaptil, Zylkene) with only size/trigger swapped
- No FAQ section or FAQPage schema; no ImageObject in Article schema
- Blocking Google Fonts load; missing --bark-light, --moss-light CSS variables
- Has breed-switcher grid widget (8 avatars) — omit from new/upgraded pages

### Generation 1.5 — Partial (pug)
- ~500 words, has breed-specific brachycephalic content + separation protocol
- No FAQPage schema; Article schema missing ImageObject
- Blocking Google Fonts; missing --bark-light, --moss-light, h3 styling, warning-box

### Generation 2 — Good (border-collie, poodle, golden-retriever)
- 800-1100 words of breed-specific body content
- FAQPage schema present (6 questions each); Article schema has ImageObject
- Async font loading: preconnect + preload onload + noscript fallback
- CSS root includes --bark-light:#5C3D2A and --moss-light:#6B8F6C
- html{scroll-behavior:smooth} present
- h3 styling present; warning-box and faq-section CSS components present
- Breed-specific products with breed rationale; training protocol sections present
- affiliate-note div in footer col 1; footer-bottom uses rgba(255,255,255,.6)
- No breed-switcher widget

## HTML Patterns for New Pages (Gen2 standard)
- Font: preconnect + preload with `onload="this.onload=null;this.rel='stylesheet'"` + noscript
- body font-family: `'DM Sans',system-ui,-apple-system,sans-serif`
- Three JSON-LD blocks: BreadcrumbList, Article (with ImageObject 1200x630), FAQPage (6+ questions)
- Canonical: no .html extension
- BreadcrumbList item 2: `"name":"Breeds","item":"https://www.anxietyfreepups.com/#breeds"`
- faq-section uses `<section class="faq-section">` outside .content div
- related-section uses `<div class="related-section">` after faq-section
- Dog.ceo script targets `.breed-hero-img` only (no .guide-hero-img fallback)

## dog.ceo API Breed Paths (confirmed)
- pug: breed/pug/images/random
- corgi: breed/corgi/images/random
- chihuahua: breed/chihuahua/images/random
- pitbull (staffordshire): breed/bullterrier/staffordshire/images/random
- border collie: breed/collie/border/images/random
- french bulldog: breed/bulldog/french/images/random
- poodle standard: breed/poodle/standard/images/random
- golden retriever: breed/retriever/golden/images/random
- labrador: breed/labrador/images/random
- german shepherd: breed/germanshepherd/images/random
- dachshund: breed/dachshund/images/random
- beagle: breed/beagle/images/random
- husky: breed/husky/images/random
- australian shepherd: breed/australian-shepherd/images/random
- yorkshire terrier: breed/yorkshire-terrier/images/random
- cavalier (Blenheim): breed/spaniel-blenheim/images/random
- doberman: breed/doberman/images/random
- weimaraner: breed/weimaraner/images/random
- boxer: breed/boxer/images/random

## Hero Gradient Colors (avoid duplicates)
- Used Gen1: #D9E8D9 (BC/corgi), #EDD9B0 (GR/french-bulldog), #F5E6D3 (pug/chihuahua), #E8E0F0 (pitbull), #E8D9F5 (poodle)
- Used Gen2 new pages: #D9EDF5 (german-shepherd, husky), #F5EDD9 (labrador), #F5D9D9 (dachshund, cavalier), #D9F5E8 (beagle), #E8F0D9 (australian-shepherd), #F0EDD9 (yorkshire-terrier), #D9D9F5 (doberman), #D9EAF0 (weimaraner)

## File Naming
- Breed pages: kebab-case .html in breeds/ (e.g., german-shepherd.html, labrador-retriever.html)
- Guide pages: kebab-case .html in guides/

## Generic Phrases to Never Use in New Content
- "Their natural temperament and breed history make them particularly sensitive to stress triggers."
- "[Breed]-specific anxiety often responds best to a combination of pressure therapy (Thundershirt) and calming supplements. Single-product solutions rarely work for this breed."

## New Breed Pages Created (March 2026 session) — all Gen2 standard
HIGH PRIORITY (done): german-shepherd, labrador-retriever, dachshund, beagle, australian-shepherd, husky
MEDIUM PRIORITY (done): yorkshire-terrier, cavalier-king-charles-spaniel, doberman, weimaraner

## Remaining Content Action Items (not yet done)
- REWRITE: corgi, chihuahua, pitbull (all Gen1 → Gen2)
- EXPAND: pug (Gen1.5 → Gen2 — add FAQ, FAQPage schema, ImageObject, warning-box, training section)
- ADD: new pages to sitemap.xml (10 new breed pages created this session)

## Gen1 → Gen2 Rewrites Completed
- french-bulldog — rewritten 2026-06-13; ~2,050 words body content; hero gradient #F5E6D3; all Gen2 standards met
