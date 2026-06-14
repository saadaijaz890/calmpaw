#!/usr/bin/env python3
"""
SEO Tools for AnxietyFreePups / CalmPaw
Fixes: sitemap, schema markup, internal linking, blog index
Runs: python seo-tools.py
"""

import os
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup

SITE = "https://www.anxietyfreepups.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
NOW = datetime.utcnow().strftime("%Y-%m-%d")

# --- Page discovery ---

def discover_pages():
    """Scan the repo for all HTML files."""
    pages = []
    for dirpath, _, filenames in os.walk(ROOT):
        # Skip .git
        if ".git" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith(".html"):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT).replace("\\", "/")
                url = f"{SITE}/{rel}" if rel != "index.html" else f"{SITE}/"
                pages.append((full, rel, url))
    return pages

# --- 1. Sitemap generator ---

def generate_sitemap(pages):
    """Write an XML sitemap including all HTML pages."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for _, rel, url in sorted(pages, key=lambda x: x[2]):
        # Priority rules
        if rel == "index.html":
            priority = "1.0"
            freq = "weekly"
        elif rel.startswith("guides/") or rel.startswith("breeds/"):
            priority = "0.9"
            freq = "monthly"
        elif rel.startswith("blogs/"):
            priority = "0.8"
            freq = "monthly"
        else:
            priority = "0.6"
            freq = "monthly"
        
        lines.append(f'  <url><loc>{url}</loc><lastmod>{NOW}</lastmod>'
                     f'<changefreq>{freq}</changefreq><priority>{priority}</priority></url>')
    lines.append("</urlset>")
    
    sitemap_path = os.path.join(ROOT, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"✅ Sitemap written: {len(pages)} URLs -> sitemap.xml")

# --- 2. Blog hub page ---

def generate_blog_index(pages):
    """Create /blogs/index.html listing all blog posts sorted by title."""
    blog_posts = []
    for full, rel, url in pages:
        if rel.startswith("blogs/") and rel != "blogs/index.html":
            # Extract title from HTML
            soup = BeautifulSoup(open(full, encoding="utf-8"), "html.parser")
            title_tag = soup.find("title")
            desc_tag = soup.find("meta", attrs={"name": "description"})
            title = title_tag.string if title_tag else rel.replace(".html", "").replace("-", " ").title()
            desc = desc_tag["content"] if desc_tag else "Read our guide"
            # Strip site name from title
            clean_title = re.sub(r'\s*[—|–|-]\s*AnxietyFreePups.*$', '', title).strip()
            blog_posts.append((clean_title, url, desc, rel))
    
    blog_posts.sort(key=lambda x: x[0].lower())
    
    blog_index_path = os.path.join(ROOT, "blogs", "index.html")
    
    cards = []
    for title, url, desc, rel in blog_posts:
        slug = rel.replace(".html", "").split("/")[-1]
        # Generate a nice image URL based on the article topic
        img_seed = slug.replace("-", "-")
        cards.append(f'''    <a href="/{rel}" class="article-card">
      <div class="card-body">
        <span class="card-tag">Blog</span>
        <h3>{title}</h3>
        <p>{desc[:120]}{'...' if len(desc) > 120 else ''}</p>
        <span class="card-read">Read more →</span>
      </div>
    </a>''')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐾</text></svg>">
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>All Blog Posts — Dog Anxiety Articles | AnxietyFreePups</title>
  <meta name="description" content="Browse all {len(blog_posts)} articles about dog anxiety — breed-specific guides, product reviews, and expert tips for calming your anxious dog."/>
  <link rel="canonical" href="{SITE}/blogs/"/>
  <meta property="og:type" content="website"/>
  <meta property="og:site_name" content="AnxietyFreePups"/>
  <meta property="og:url" content="{SITE}/blogs/"/>
  <meta property="og:title" content="All Blog Posts — Dog Anxiety Articles | AnxietyFreePups"/>
  <meta property="og:description" content="Browse all {len(blog_posts)} articles about dog anxiety — breed-specific guides, product reviews, and expert tips."/>
  <meta name="twitter:card" content="summary_large_image"/>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'"><noscript><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet"></noscript>
  <style>
    :root{{--cream:#FAF7F2;--warm-white:#FFFEF9;--bark:#2C1A0E;--bark-light:#5C3D2A;--moss:#3D5A3E;--moss-light:#6B8F6C;--sand:#D4A96A;--sand-light:#EDD9B0;--text:#1A1208;--text-muted:#6B5A4A;--shadow:0 4px 32px rgba(44,26,14,.10);--shadow-hover:0 12px 48px rgba(44,26,14,.18)}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'DM Sans',system-ui,-apple-system,sans-serif;background:var(--cream);color:var(--text)}}
    header{{position:sticky;top:0;z-index:100;background:rgba(250,247,242,.98);backdrop-filter:blur(12px);border-bottom:1px solid var(--sand-light);padding:0 5vw;display:flex;align-items:center;justify-content:space-between;height:64px}}
    .logo{{font-family:'Playfair Display',Georgia,serif;font-size:1.5rem;font-weight:900;color:var(--bark);text-decoration:none}}.logo span{{color:var(--moss)}}
    nav{{display:flex;gap:2rem}}nav a{{text-decoration:none;color:var(--text-muted);font-size:.9rem;font-weight:500}}nav a:hover{{color:var(--moss)}}
    .nav-cta{{background:var(--moss);color:white!important;padding:.5rem 1.2rem;border-radius:100px}}
    .breadcrumb{{padding:1.2rem 5vw;font-size:.82rem;color:var(--text-muted)}}.breadcrumb a{{color:var(--moss);text-decoration:none}}
    .hero-mini{{padding:3rem 5vw 2rem}}
    .hero-mini h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(2rem,3.5vw,2.8rem);font-weight:900;color:var(--bark);margin-bottom:.8rem}}
    .hero-mini p{{font-size:1.05rem;color:var(--text-muted);max-width:600px;line-height:1.6}}
    .count-badge{{display:inline-block;background:var(--moss);color:white;padding:.2rem .7rem;border-radius:100px;font-size:.78rem;font-weight:500;margin-bottom:1rem}}
    .blog-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.5rem;padding:0 5vw 4rem}}
    .article-card{{background:var(--warm-white);border-radius:16px;border:1px solid rgba(212,169,106,.25);box-shadow:var(--shadow);transition:all .3s ease;text-decoration:none;color:inherit;overflow:hidden}}
    .article-card:hover{{transform:translateY(-4px);box-shadow:var(--shadow-hover);border-color:var(--moss-light)}}
    .card-body{{padding:1.5rem}}
    .card-tag{{display:inline-block;background:var(--sand-light);color:var(--bark-light);padding:.2rem .7rem;border-radius:100px;font-size:.72rem;font-weight:500;margin-bottom:.8rem}}
    .card-body h3{{font-family:'Playfair Display',Georgia,serif;font-size:1.15rem;font-weight:700;color:var(--bark);margin-bottom:.5rem;line-height:1.3}}
    .card-body p{{font-size:.88rem;color:var(--text-muted);line-height:1.55;margin-bottom:.8rem}}
    .card-read{{font-size:.82rem;color:var(--moss);font-weight:500}}
    footer{{text-align:center;padding:2rem 5vw;color:var(--text-muted);font-size:.82rem;border-top:1px solid var(--sand-light)}}
  </style>
</head>
<body>
<header>
  <a href="/" class="logo">🐾 AnxietyFree<span>Pups</span></a>
  <nav>
    <a href="/guides/">Guides</a>
    <a href="/breeds/">Breeds</a>
    <a href="/blogs/" style="color:var(--moss);font-weight:600">Blog</a>
    <a href="/resources/about.html">About</a>
    <a href="/resources/contact.html" class="nav-cta">Get Help</a>
  </nav>
</header>
<div class="breadcrumb"><a href="/">Home</a> › Blog</div>
<div class="hero-mini">
  <span class="count-badge">{len(blog_posts)} Articles</span>
  <h1>All Dog Anxiety Articles</h1>
  <p>Breed-specific guides, product comparisons, and expert tips to help your anxious dog live a calmer, happier life.</p>
</div>
<div class="blog-grid">
{chr(10).join(cards)}
</div>
<footer>
  <p>© {datetime.utcnow().year} AnxietyFreePups — Helping anxious dogs live calmer lives</p>
</footer>
</body>
</html>'''
    
    with open(blog_index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Blog index created: {len(blog_posts)} posts -> blogs/index.html")

# --- 3. Schema markup (Article, Breadcrumb, FAQ) ---

def inject_schema_markup(pages):
    """Add Article schema to blog posts, BreadcrumbList to all pages."""
    updated = 0
    article_schema_added = 0
    breadcrumb_added = 0
    
    for full, rel, url in pages:
        with open(full, encoding="utf-8") as f:
            content = f.read()
        
        soup = BeautifulSoup(content, "html.parser")
        head = soup.find("head")
        if not head:
            continue
        
        modified = False
        
        # Get title and description
        title_tag = soup.find("title")
        desc_tag = soup.find("meta", attrs={"name": "description"})
        page_title = title_tag.string if title_tag else "Dog Anxiety Guide"
        page_desc = desc_tag["content"] if desc_tag else "Expert-reviewed dog anxiety solutions."
        
        clean_title = re.sub(r'\s*[—|–|-]\s*AnxietyFreePups.*$', '', page_title).strip()
        
        # Check existing schema scripts
        existing_schemas = soup.find_all("script", type="application/ld+json")
        
        # --- Article / BlogPosting schema for blog posts ---
        if rel.startswith("blogs/") and rel != "blogs/index.html":
            has_article = any("Article" in s.string or "BlogPosting" in s.string 
                            for s in existing_schemas if s.string)
            if not has_article:
                # Extract image from OG tag
                og_img = soup.find("meta", property="og:image")
                img_url = og_img["content"] if og_img else "https://picsum.photos/seed/dog-blog/1200/630"
                
                # Extract word count estimate
                body = soup.find("body")
                text_len = len(body.get_text(strip=True)) if body else 1000
                word_count = max(300, text_len // 5)
                
                article_schema = json.dumps({
                    "@context": "https://schema.org",
                    "@type": "BlogPosting",
                    "headline": clean_title,
                    "description": page_desc,
                    "image": img_url,
                    "url": url,
                    "mainEntityOfPage": url,
                    "datePublished": NOW,
                    "dateModified": NOW,
                    "author": {"@type": "Organization", "name": "AnxietyFreePups"},
                    "publisher": {
                        "@type": "Organization",
                        "name": "AnxietyFreePups",
                        "logo": {"@type": "ImageObject", "url": f"{SITE}/"}
                    },
                    "wordCount": word_count
                }, ensure_ascii=False)
                
                script = soup.new_tag("script", type="application/ld+json")
                script.string = f"\n{article_schema}\n"
                head.append(script)
                article_schema_added += 1
                modified = True
        
        # --- BreadcrumbList schema for ALL pages ---
        has_breadcrumb = any("BreadcrumbList" in s.string for s in existing_schemas if s.string)
        if not has_breadcrumb:
            path_parts = rel.replace(".html", "").split("/")
            items = [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE}
            ]
            pos = 2
            for i, part in enumerate(path_parts):
                if not part:
                    continue
                name = part.replace("-", " ").title()
                item_url = f"{SITE}/{'/'.join(path_parts[:i+1])}/" if i < len(path_parts) - 1 else url
                items.append({"@type": "ListItem", "position": pos, "name": name, "item": item_url})
                pos += 1
            
            breadcrumb_schema = json.dumps({
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": items
            }, ensure_ascii=False)
            
            script = soup.new_tag("script", type="application/ld+json")
            script.string = f"\n{breadcrumb_schema}\n"
            head.append(script)
            breadcrumb_added += 1
            modified = True
        
        # --- FAQ schema for guides that have FAQ-like content ---
        if rel.startswith("guides/") and not any("FAQPage" in s.string for s in existing_schemas if s.string):
            # Check if page has FAQ-style h2/h3 questions
            questions = []
            for tag in soup.find_all(["h2", "h3"]):
                text = tag.get_text(strip=True)
                if text and len(text) > 10 and text.endswith("?"):
                    # Find next paragraph for answer
                    next_p = tag.find_next_sibling("p")
                    if next_p:
                        answer = next_p.get_text(strip=True)[:200]
                        questions.append({"q": text, "a": answer})
            
            if questions:
                faq_schema = json.dumps({
                    "@context": "https://schema.org",
                    "@type": "FAQPage",
                    "mainEntity": [{
                        "@type": "Question",
                        "name": q["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": q["a"]}
                    } for q in questions[:6]]
                }, ensure_ascii=False)
                script = soup.new_tag("script", type="application/ld+json")
                script.string = f"\n{faq_schema}\n"
                head.append(script)
        
        if modified:
            with open(full, "w", encoding="utf-8") as f:
                f.write(str(soup))
            updated += 1
    
    print(f"✅ Schema: +{article_schema_added} Article, +{breadcrumb_added} BreadcrumbList, {updated} pages updated")

# --- 4. Internal linking ---

def add_related_posts(pages):
    """Add 'Related Articles' section at the bottom of blog posts."""
    # Build a keyword map: each page -> keywords from its title
    page_keywords = {}
    for full, rel, url in pages:
        if not rel.startswith("blogs/") or rel == "blogs/index.html":
            continue
        soup = BeautifulSoup(open(full, encoding="utf-8"), "html.parser")
        title = soup.find("title")
        if title:
            clean = re.sub(r'\s*[—|–|-]\s*AnxietyFreePups.*$', '', title.string).lower()
            page_keywords[rel] = {
                "url": url,
                "title": clean,
                "words": set(re.findall(r'\b[a-z]{4,}\b', clean)),
                "soup": soup,
                "full": full
            }
    
    related_count = 0
    for rel, info in page_keywords.items():
        # Find 3 most related posts
        scores = []
        for other_rel, other_info in page_keywords.items():
            if other_rel == rel:
                continue
            overlap = len(info["words"] & other_info["words"])
            if overlap >= 2:
                scores.append((overlap, other_info["url"], other_info["title"], other_rel))
        
        scores.sort(reverse=True)
        top3 = scores[:3]
        
        if not top3:
            continue
        
        # Check if related posts already exist
        body = info["soup"].find("body")
        if not body:
            continue
        
        existing = body.find_all(string=re.compile(r"Related\s*(Articles|Posts|Guides)", re.IGNORECASE))
        if existing:
            continue
        
        # Build related posts HTML
        related_html = '\n<div style="margin-top:3rem;padding-top:2rem;border-top:2px solid var(--sand-light)">\n'
        related_html += '  <h2 style="font-family:\'Playfair Display\',Georgia,serif;font-size:1.5rem;font-weight:700;color:var(--bark);margin-bottom:1rem">📖 Related Articles</h2>\n'
        related_html += '  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem">\n'
        
        for score, url, title, other_rel in top3:
            display_title = re.sub(r'\s*[—|–|-]\s*AnxietyFreePups.*$', '', title).strip().title()
            related_html += f'    <a href="/{other_rel}" style="background:var(--warm-white);border:1px solid var(--sand-light);border-radius:12px;padding:1rem;text-decoration:none;color:inherit;transition:all .2s" '
            related_html += f'onmouseover="this.style.borderColor=\'var(--moss-light)\';this.style.transform=\'translateY(-2px)\'" '
            related_html += f'onmouseout="this.style.borderColor=\'\';this.style.transform=\'\'">'
            related_html += f'      <h4 style="font-size:.95rem;font-weight:600;color:var(--bark);margin-bottom:.3rem">{display_title}</h4>\n'
            related_html += f'      <span style="font-size:.82rem;color:var(--moss)">Read more →</span>\n'
            related_html += f'    </a>\n'
        
        related_html += '  </div>\n</div>\n'
        
        # Insert before footer
        content_div = info["soup"].find("div", class_="content")
        if content_div:
            content_div.append(BeautifulSoup(related_html, "html.parser"))
            with open(info["full"], "w", encoding="utf-8") as f:
                f.write(str(info["soup"]))
            related_count += 1
    
    print(f"✅ Related posts added to {related_count} blog pages")

# --- 5. Robots.txt ---

def generate_robots():
    """Write a clean robots.txt."""
    content = f"""User-agent: *
Allow: /
Sitemap: {SITE}/sitemap.xml
"""
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ robots.txt updated")

# --- Run ---

if __name__ == "__main__":
    print("🔍 Discovering pages...")
    pages = discover_pages()
    print(f"   Found {len(pages)} HTML pages")
    
    print("\n📍 Generating sitemap...")
    generate_sitemap(pages)
    
    print("\n📍 Creating blog index...")
    generate_blog_index(pages)
    
    print("\n📍 Injecting schema markup...")
    inject_schema_markup(pages)
    
    print("\n📍 Adding related posts...")
    add_related_posts(pages)
    
    print("\n📍 Updating robots.txt...")
    generate_robots()
    
    print(f"\n🎉 SEO tools complete! All {len(pages)} pages processed.")
    print(f"   Site: {SITE}")
    print(f"   Push to git to deploy.")