#!/usr/bin/env python3
"""
Content Agent for CalmPaw / AnxietyFreePups
Uses OpenRouter + DeepSeek Flash V4 to auto-generate SEO-optimized blog posts
Cost: ~$0.01-0.05 per article with DeepSeek Flash V4

Usage:
  python content-agent.py                          # Generate 1 article
  python content-agent.py --count 5                # Generate 5 articles
  python content-agent.py --topic "fireworks fear" # Specific topic
  python content-agent.py --dry-run                # Show topics without generating
  python content-agent.py --list                   # List generated articles
"""

import os
import re
import json
import sys
import random
import hashlib
from datetime import datetime
from pathlib import Path

# === CONFIG ===
ROOT = Path(__file__).parent.absolute()
SITE_URL = "https://www.anxietyfreepups.com"
SITE_NAME = "AnxietyFreePups"
OUTPUT_DIR = ROOT / "blogs"

# Amazon affiliate tag
AMZ_TAG = "anxietyfreepups-20"

# === API SETUP ===

def get_api_key():
    """Try multiple ways to get the OpenRouter API key."""
    # 1. Environment variable
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key and key != "***":
        return key
    # 2. Project .env
    env_file = ROOT / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY="):
                    val = line.split("=", 1)[1].strip("\"'")
                    if val and val != "***":
                        return val
    # 3. Hermes config (Windows)
    hermes_env = Path.home() / "AppData/Local/hermes/.env"
    if hermes_env.exists():
        with open(hermes_env) as f:
            for line in f:
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY="):
                    val = line.split("=", 1)[1].strip("\"'")
                    if val and val != "***":
                        return val
    # 4. Hermes config.yaml
    hermes_config = Path.home() / "AppData/Local/hermes/config.yaml"
    if hermes_config.exists():
        with open(hermes_config) as f:
            content = f.read()
            m = re.search(r'openrouter.*?api_key:\s*["\']?(sk-or\S+?)[\'"\s]', content, re.DOTALL | re.IGNORECASE)
            if m:
                return m.group(1)
    return None

API_KEY = get_api_key()

# === TOPIC DATABASE ===

# High-traffic affiliate topics organized by category
TOPICS = {
    "product_comparisons": [
        "Best Calming Chews for Dogs 2026 — Top 7 Compared",
        "Thundershirt vs Anxiety Wrap vs Calming Cap — Which Works Best?",
        "CBD Oil for Dogs vs Melatonin vs L-Theanine — A Complete Comparison",
        "Zylkene vs Composure vs Solliquin — Best Calming Supplement",
        "Adaptil Spray vs Diffuser vs Collar — Which Delivery Method Wins?",
        "Best Dog Anxiety Beds 2026 — Pressure-Relief Donut Beds Reviewed",
        "Weighted Blankets for Dogs vs Thundershirt — Which Is More Effective?",
        "Best Calming Treats for Small Dogs vs Large Dogs — Brand Comparison",
        "Trazodone vs Gabapentin for Dogs — Which Anxiety Med Is Better?",
        "Dog Calming Chews vs Prescription Meds — What's Right for Your Dog?",
        "Best Dog Calming Collars Compared — Adaptil vs Sentry vs ThunderEase",
        "Dog Anxiety Wrap vs Pressure Vest vs Thundershirt — Full Comparison",
        "Best Dog Calming Supplement for Travel — Top Brands Compared",
        "Fluoxetine vs Clomipramine for Separation Anxiety — Vet Comparison",
    ],
    "seasonal": [
        "July 4th Fireworks Survival Guide for Dogs — Complete 2026 Plan",
        "How to Calm Your Dog During Thunderstorms — 7 Steps That Work",
        "Is Your Dog Scared of Fireworks? Here's Exactly What to Do",
        "New Year's Eve Dog Anxiety — Preparation Checklist for 2026",
        "Summer Storm Season Dog Anxiety — Your Monthly Action Plan",
        "Best Dog Calming Products for Hurricane Season 2026",
        "Moving to a New Home With an Anxious Dog — Stress-Free Guide",
        "How to Prepare Your Dog for Daylight Savings Time Change Anxiety",
    ],
    "breed_specific": [
        "Best Calming Products for German Shepherds — What Actually Works",
        "Labrador Retriever Separation Anxiety — Complete Treatment Plan",
        "French Bulldog Anxiety Guide — BOAS, Separation & Noise Fears",
        "Corgi Anxiety Solutions — Why Your Corgi Barks at Everything",
        "Golden Retriever Anxiety — The Velcro Dog Protocol",
        "Husky Howling and Escape Anxiety — Why They Run & How to Stop It",
        "Dachshund Noise Phobia — Why Your Wiener Dog Shakes & What Helps",
        "Poodle Anxiety — Grooming, Separation & Noise Sensitivity",
        "Border Collie Anxiety — High-Energy Dog Calming Strategies",
        "Chihuahua Anxiety — Why Small Dogs Tremble and How to Help",
        "Shih Tzu Separation Anxiety — Gentle Solutions for Companion Breeds",
        "Great Dane Anxiety — Managing Anxiety in Giant Breed Dogs",
        "Rottweiler Anxiety and Guarding Behavior — What Owners Need to Know",
    ],
    "problem_solution": [
        "Why Is My Dog Panting at Night? 7 Causes & When to Worry",
        "Dog Pacing and Restless — Is It Anxiety or Something Else?",
        "How to Tell If Your Dog Has Separation Anxiety vs Boredom",
        "My Dog Destroyed the Couch Again — Separation Anxiety or Misbehavior?",
        "Does Your Dog Follow You Everywhere? Velcro Dog Behavior Explained",
        "Dog Whining for No Reason — 5 Hidden Causes of Unexplained Whining",
        "How to Stop Your Dog from Barking at Every Sound — Noise Sensitivity Training",
        "Dog Shaking and Trembling for No Reason — When to Worry",
        "Why Does My Dog Lick His Paws Excessively? Anxiety or Allergies?",
        "Dog Eating Grass Frantically — Is It Anxiety or Something Else?",
        "My Dog Won't Eat When I'm Away — Understanding Stress Anorexia in Dogs",
        "Why Is My Dog Drooling Suddenly? Anxiety Signs Every Owner Misses",
        "Dog Yawning Excessively — Is It Stress or Just Tired?",
        "Why Does My Dog Hide Under the Bed? Fear & Anxiety Explained",
        "Dog Tail Tucking Explained — What It Means for Anxious Dogs",
        "Why Does My Dog Avoid Eye Contact? Subtle Anxiety Signals",
    ],
    "training_behavior": [
        "Crate Training an Anxious Dog — Step-by-Step Guide That Actually Works",
        "How to Socialize a Fearful Puppy — The 3-3-3 Rule Explained",
        "Counterconditioning vs Desensitization — What's the Difference for Dogs?",
        "Does Your Dog Hate the Vet? How to Reduce Vet Visit Anxiety",
        "Rescue Dog Anxiety — The First 30 Days Home Protocol",
        "How to Introduce a Calming Aid to a Skeptical Dog",
        "How to Leave Your Anxious Dog Home Alone — Desensitization Training",
        "Dog Door-Dashing Anxiety — How to Stop Panic Escapes",
        "How to Walk an Anxious Dog — Leash Training for Nervous Pups",
        "Submissive Urination in Dogs — Is It Anxiety and How to Fix It",
        "Does Your Dog Destroy Toys When Anxious? Redirecting Destructive Behavior",
        "Clicker Training for Anxious Dogs — Does It Really Work?",
        "Training an Anxious Dog to Use a Calming Bed — Step by Step",
    ],
    "product_reviews_affiliate": [
        "Thundershirt for Dogs Review 2026 — Does It Really Work?",
        "Zylkene Calming Supplement Review — Vet-Recommended or Overhyped?",
        "Best Dog Calming Treats on Amazon 2026 — Honest Reviews",
        "Adaptil Review — Pheromone Therapy for Anxious Dogs",
        "VetriScience Composure Review — Fast-Acting Calming Chews Tested",
        "Snuggle Puppy Review — Does the Heartbeat Toy Reduce Anxiety?",
        "Calming Music for Dogs — 5 Best Playlists & Sound Machines Reviewed",
        "Best Anxiety Vest for Dogs in 2026 — Top 5 Compared with Test Results",
        "Best Amazon Dog Calming Treats Under $20 — Budget-Friendly Picks",
        "Top 10 Best Calming Dog Beds on Amazon 2026 — Our Picks",
        "Best Dog Calming Sprays and Diffusers on Amazon — Reviewed",
        "Dog Appeasing Pheromone Products on Amazon — Which Actually Work?",
        "Best Calming Treats for Puppies on Amazon — Safe Options Reviewed",
        "Best Calming Aids for Senior Dogs on Amazon — Our Top Picks 2026",
        "Top Rated Anxiety Vests for Dogs on Amazon — Customer Favorites",
        "Best Calming Gummies for Dogs on Amazon — Chewable Options Reviewed",
        "Best Interactive Dog Toys for Anxiety on Amazon — Keep Them Busy",
        "Crate Training Supplies for Anxious Dogs — Amazon Shopping Guide",
        "Best Calming Dog Treats with CBD on Amazon — Top 5 Brands",
        "Dog Calming Music and Sound Machines on Amazon — Buyer's Guide",
        "Best Calming Treats for Dogs with Noise Anxiety — Amazon Picks",
        "Best Travel Calming Aids for Dogs on Amazon — Road Trip Essentials",
    ],
    "health_medical": [
        "Dog Anxiety Medication Guide — Options from Your Vet Explained",
        "Melatonin for Dogs — Dosage Chart, Safety & WHEN NOT to Use It",
        "CBD for Dogs Anxiety 2026 — Science, Dosage & Legal Status",
        "Can Senior Dogs Take Calming Supplements? Age-Specific Guide",
        "Dog Anxiety Medication Side Effects — What Every Owner Should Know",
        "Natural Remedies for Dog Anxiety That Actually Work — Evidence-Based",
        "When to See a Veterinary Behaviorist vs Regular Vet for Anxiety",
        "The Cost of Treating Dog Anxiety — Budget-Friendly Solutions",
        "Dog Anxiety Medication for Travel — What Vets Recommend",
        "Can I Give My Dog Human Anxiety Meds? Dangers Explained",
        "How Long Does Dog Anxiety Medication Take to Work? Timeline Guide",
        "Natural Calming Supplement Ingredients That Really Work — Science Review",
        "Dog Anxiety and Digestion — The Gut-Brain Connection Explained",
        "L-Theanine for Dogs — Natural Calming Aid, Dosage and Safety",
        "Ashwagandha for Dogs — Natural Anxiety Relief or Risky?",
        "Valerian Root for Dogs — Natural Calming Remedy Reviewed by Vets",
        "Passionflower for Dog Anxiety — Herbal Remedy That Actually Works",
        "Chamomile for Dogs — How to Use This Natural Calming Herb Safely",
        "Dog Anxiety and Compulsive Disorders — When to Seek Medication",
    ],
}

# Flatten into a single list with metadata
ALL_TOPICS = []
for category, topics in TOPICS.items():
    for topic in topics:
        ALL_TOPICS.append({"title": topic, "category": category})


def generate_slug(title):
    """Convert title to URL-friendly slug."""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')
    return slug


def get_generated_list():
    """Get list of already-generated articles to avoid duplicates."""
    generated = set()
    if OUTPUT_DIR.exists():
        for f in OUTPUT_DIR.glob("*.html"):
            slug = f.stem
            generated.add(slug)
    return generated


def get_article_template(title, description, body_html, slug, category):
    """Generate a full HTML article page matching the site style."""
    canonical = f"{SITE_URL}/blogs/{slug}"
    img_seed = slug.replace("-", "-")
    
    # Build breadcrumb
    breadcrumb_items = {
        "Home": SITE_URL,
        "Blog": f"{SITE_URL}/blogs/",
        title: canonical
    }
    
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": name, "item": url}
            for i, (name, url) in enumerate(breadcrumb_items.items())
        ]
    }
    
    # Build FAQ schema from any question headers in the body
    faq_items = []
    for match in re.finditer(r'<h[23][^>]*>(.*?\?)</h[23]>', body_html):
        q = match.group(1).strip()
        # Find the next paragraph after the question
        after = body_html[match.end():]
        p_match = re.search(r'<p>(.*?)</p>', after)
        if p_match:
            a = p_match.group(1).strip()
            a = re.sub(r'<[^>]+>', '', a)[:300]
            faq_items.append({"@type": "Question", "name": q, 
                             "acceptedAnswer": {"@type": "Answer", "text": a}})
    
    article_schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "url": canonical,
        "mainEntityOfPage": canonical,
        "datePublished": datetime.utcnow().strftime("%Y-%m-%d"),
        "dateModified": datetime.utcnow().strftime("%Y-%m-%d"),
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
        "wordCount": len(body_html.split())
    }
    
    schemas = [
        json.dumps(article_schema, ensure_ascii=False),
        json.dumps(breadcrumb_schema, ensure_ascii=False),
    ]
    if faq_items:
        schemas.append(json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_items[:6]
        }, ensure_ascii=False))
    
    schema_html = "\n  ".join(
        f'<script type="application/ld+json">{s}</script>'
        for s in schemas
    )
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🐾</text></svg>">
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} | {SITE_NAME}</title>
  <meta name="description" content="{description}"/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="{SITE_NAME}"/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:title" content="{title} | {SITE_NAME}"/>
  <meta property="og:description" content="{description}"/>
  <meta property="og:image" content="https://picsum.photos/seed/{img_seed}/1200/630"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{title} | {SITE_NAME}"/>
  <meta name="twitter:description" content="{description}"/>
  <meta name="twitter:image" content="https://picsum.photos/seed/{img_seed}/1200/630"/>
  {schema_html}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'"><noscript><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet"></noscript>
  <style>
    :root{{--cream:#FAF7F2;--warm-white:#FFFEF9;--bark:#2C1A0E;--bark-light:#5C3D2A;--moss:#3D5A3E;--moss-light:#6B8F6C;--sand:#D4A96A;--sand-light:#EDD9B0;--blush:#E8C4A0;--text:#1A1208;--text-muted:#6B5A4A;--shadow:0 4px 32px rgba(44,26,14,.10)}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'DM Sans',system-ui,-apple-system,sans-serif;background:var(--cream);color:var(--text)}}
    header{{position:sticky;top:0;z-index:100;background:rgba(250,247,242,.98);backdrop-filter:blur(12px);border-bottom:1px solid var(--sand-light);padding:0 5vw;display:flex;align-items:center;justify-content:space-between;height:64px}}
    .logo{{font-family:'Playfair Display',Georgia,serif;font-size:1.5rem;font-weight:900;color:var(--bark);text-decoration:none}}.logo span{{color:var(--moss)}}
    nav{{display:flex;gap:2rem}}nav a{{text-decoration:none;color:var(--text-muted);font-size:.9rem;font-weight:500}}nav a:hover{{color:var(--moss)}}
    .nav-cta{{background:var(--moss);color:white!important;padding:.5rem 1.2rem;border-radius:100px}}
    .breadcrumb{{padding:1.2rem 5vw;font-size:.82rem;color:var(--text-muted)}}.breadcrumb a{{color:var(--moss);text-decoration:none}}
    .hero-article{{background:linear-gradient(135deg,var(--sand-light) 0%,var(--cream) 60%);padding:3rem 5vw 2rem}}
    .article-tag{{display:inline-block;background:var(--bark);color:var(--sand-light);padding:.3rem .9rem;border-radius:100px;font-size:.72rem;font-weight:500;letter-spacing:.06em;margin-bottom:1.2rem}}
    h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(2rem,4vw,3rem);font-weight:900;color:var(--bark);line-height:1.1;max-width:760px;margin-bottom:1rem}}
    .lead{{font-size:1.1rem;color:var(--text-muted);max-width:680px;line-height:1.7;margin-bottom:1.5rem}}
    .meta{{display:flex;gap:2rem;font-size:.82rem;color:var(--text-muted);margin-bottom:.5rem}}
    .content{{max-width:760px;margin:0 auto;padding:2rem 5vw 4rem}}
    h2{{font-family:'Playfair Display',Georgia,serif;font-size:1.8rem;font-weight:700;color:var(--bark);margin:2.5rem 0 1rem}}
    h3{{font-family:'Playfair Display',Georgia,serif;font-size:1.3rem;font-weight:700;color:var(--bark);margin:1.5rem 0 .8rem}}
    p{{font-size:1rem;color:var(--text-muted);line-height:1.8;margin-bottom:1.2rem}}
    ul,ol{{color:var(--text-muted);font-size:1rem;line-height:1.75;margin-bottom:1.2rem;padding-left:1.5rem}}
    li{{margin-bottom:.4rem}}
    .product-box{{background:var(--warm-white);border:1px solid var(--sand-light);border-radius:16px;padding:1.5rem;margin:1.5rem 0;display:flex;gap:1rem;align-items:flex-start}}
    .product-box .emoji{{font-size:2rem;flex-shrink:0}}
    .product-box h4{{font-weight:600;color:var(--bark);margin-bottom:.3rem;font-size:1.05rem}}
    .product-box p{{font-size:.9rem;margin-bottom:0}}
    .btn-amz{{display:inline-block;background:var(--moss);color:white;padding:.5rem 1.2rem;border-radius:100px;text-decoration:none;font-size:.82rem;font-weight:500;margin-top:.5rem;transition:all .2s}}
    .btn-amz:hover{{background:var(--bark)}}
    .pro-con-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0}}
    .pro-box,.con-box{{border-radius:12px;padding:1.2rem}}
    .pro-box{{background:#E8F5E9;border:1px solid #A5D6A7}}
    .con-box{{background:#FFEBEE;border:1px solid #EF9A9A}}
    .pro-box h4,.con-box h4{{font-size:.9rem;margin-bottom:.5rem}}
    .pro-box li,.con-box li{{font-size:.85rem}}
    blockquote{{border-left:4px solid var(--sand);padding:1rem 1.5rem;margin:1.5rem 0;background:var(--warm-white);border-radius:0 12px 12px 0;font-style:italic;color:var(--text-muted)}}
    table{{width:100%;border-collapse:collapse;margin:1.5rem 0;font-size:.9rem}}
    th,td{{padding:.8rem 1rem;text-align:left;border-bottom:1px solid var(--sand-light)}}
    th{{background:var(--moss);color:white;font-weight:500}}
    tr:nth-child(even){{background:var(--warm-white)}}
    .related-section{{margin-top:3rem;padding-top:2rem;border-top:2px solid var(--sand-light)}}
    .related-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem}}
    .related-card{{background:var(--warm-white);border:1px solid var(--sand-light);border-radius:12px;padding:1rem;text-decoration:none;color:inherit;transition:all .2s}}
    .related-card:hover{{border-color:var(--moss-light);transform:translateY(-2px)}}
    .related-card h4{{font-size:.95rem;font-weight:600;color:var(--bark);margin-bottom:.3rem}}
    footer{{text-align:center;padding:2rem 5vw;color:var(--text-muted);font-size:.82rem;border-top:1px solid var(--sand-light)}}
    @media(max-width:640px){{.pro-con-grid{{grid-template-columns:1fr}}}}
  </style>
</head>
<body>
<header>
  <a href="/" class="logo">🐾 AnxietyFree<span>Pups</span></a>
  <nav>
    <a href="/guides/">Guides</a>
    <a href="/breeds/">Breeds</a>
    <a href="/blogs/">Blog</a>
    <a href="/resources/about.html">About</a>
    <a href="/resources/contact.html" class="nav-cta">Get Help</a>
  </nav>
</header>
<div class="breadcrumb"><a href="/">Home</a> › <a href="/blogs/">Blog</a> › {title}</div>
<div class="hero-article">
  <span class="article-tag">{category.replace("_", " ").title()}</span>
  <h1>{title}</h1>
  <p class="lead">{description}</p>
  <div class="meta">
    <span>📅 Updated {datetime.utcnow().strftime("%B %Y")}</span>
    <span>⏱ {max(5, len(body_html.split()) // 200)} min read</span>
  </div>
</div>
<div class="content">
{body_html}
</div>
<footer>
  <p>© {datetime.utcnow().year} {SITE_NAME} — Helping anxious dogs live calmer lives</p>
  <p style="margin-top:.5rem;font-size:.78rem">As an Amazon Associate, we earn from qualifying purchases.</p>
</footer>
</body>
</html>'''


# === AI Content Generator ===

def generate_article(topic_title, category):
    """Use DeepSeek Flash V4 via OpenRouter to generate article content."""
    slug = generate_slug(topic_title)
    
    print(f"🤖 Generating: {topic_title}")
    print(f"   Slug: {slug}")
    
    # Skip if this article already exists
    if (OUTPUT_DIR / f"{slug}.html").exists():
        print(f"   ⏭ Already exists, skipping")
        return None
    
    if not API_KEY:
        print(f"   ❌ No API key found. Set OPENROUTER_API_KEY in .env file.")
        return None
    
    # Build the prompt for the AI
    system_prompt = """You are an expert veterinary content writer specializing in dog anxiety. 
Write comprehensive, SEO-optimized blog posts that help dog owners solve real problems.

RULES:
- Write 1500-2500 words of genuine, helpful content with real actionable advice
- Use proper HTML formatting: <h2>, <h3>, <p>, <ul>, <ol>, <li>, <table>, <blockquote>
- Include a comparison table when reviewing products
- Include pro/con boxes with <div class="pro-box"> and <div class="con-box">
- Include product recommendation boxes with <div class="product-box"> format. Add Amazon affiliate links using: https://www.amazon.com/dp/XXXXX?tag=anxietyfreepups-20
- Include 3-5 FAQ questions as <h3> with answers in following <p> tags
- Add an <h2>Conclusion</h2> at the end
- Write in natural, helpful tone — not salesy, not overly medical
- Target real search queries dog owners type into Google
- DO NOT use markdown — only HTML tags
- DO NOT wrap the response in any HTML or markdown code blocks — just raw HTML"""
    
    user_prompt = f"""Write a complete SEO-optimized blog post titled: "{topic_title}"

Category: {category.replace('_', ' ').title()}

Requirements:
- 1500-2500 words
- HTML formatted (h2, h3, p, ul, ol, table, div)
- Include 1 comparison table comparing top products
- Include at least 2 product recommendation boxes with Amazon affiliate links (use placeholder ASINs like B0XXXXX)
- Include pro/con sections where appropriate
- Include 3-5 FAQ questions at the end
- End with a conclusion section
- Include relevant internal links to other pages on anxietyfreepups.com where natural (e.g., /guides/, /breeds/)
- Write for real dog owners with practical, actionable advice"""

    try:
        import requests
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            json={
                "model": "deepseek/deepseek-v4-flash",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 8000,
            },
            timeout=120
        )
        
        data = response.json()
        
        # Check for errors
        if "error" in data:
            error_msg = data["error"].get("message", str(data["error"]))
            print(f"   ❌ API Error: {error_msg}")
            return None
        
        body_html = data["choices"][0]["message"]["content"]
        
        # Clean up — remove markdown code fences if AI wrapped them
        body_html = re.sub(r'^```html?\s*', '', body_html)
        body_html = re.sub(r'\s*```$', '', body_html)
        
        # Generate meta description (first 155 chars from first paragraph)
        p_match = re.search(r'<p>(.*?)</p>', body_html)
        description = ""
        if p_match:
            clean_text = re.sub(r'<[^>]+>', '', p_match.group(1))
            description = clean_text[:155].strip()
        if not description:
            description = f"Complete guide to {topic_title.lower()} — expert tips, product reviews, and proven solutions for your anxious dog."
        
        html = get_article_template(topic_title, description, body_html, slug, category)
        
        # Write the file
        output_path = OUTPUT_DIR / f"{slug}.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        word_count = len(body_html.split())
        print(f"   ✅ Generated: {output_path.name} ({word_count} words)")
        
        # Track what was generated
        log_entry = {
            "title": topic_title,
            "slug": slug,
            "category": category,
            "words": word_count,
            "date": datetime.utcnow().isoformat(),
            "file": str(output_path)
        }
        log_path = ROOT / "content-log.json"
        existing = []
        if log_path.exists():
            with open(log_path) as f:
                try:
                    existing = json.load(f)
                except:
                    existing = []
        existing.append(log_entry)
        with open(log_path, "w") as f:
            json.dump(existing, f, indent=2)
        
        return output_path
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None


# === Main ===

def main():
    count = 1
    specific_topic = None
    dry_run = False
    list_only = False
    
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--count" and i + 1 < len(args):
            count = int(args[i + 1])
        elif arg == "--topic" and i + 1 < len(args):
            specific_topic = args[i + 1]
        elif arg == "--dry-run":
            dry_run = True
        elif arg == "--list":
            list_only = True
    
    if list_only:
        generated = get_generated_list()
        print(f"\n📚 Already generated: {len(generated)} articles\n")
        log_path = ROOT / "content-log.json"
        if log_path.exists():
            with open(log_path) as f:
                entries = json.load(f)
            for e in entries[-20:]:
                print(f"  📄 {e['title']} ({e['words']}w) — {e['slug']}.html")
        return
    
    if not API_KEY:
        print("\n⚠️  No OpenRouter API key found!")
        print("   Create a .env file in this directory with:")
        print('   OPENROUTER_API_KEY=sk-or-v1-xxxxx')
        print("   Or set it as an environment variable.\n")
        return
    
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True)
    
    generated = get_generated_list()
    
    if specific_topic:
        topics_to_generate = [{"title": specific_topic, "category": "custom"}]
    else:
        # Filter out already-generated topics
        available = [t for t in ALL_TOPICS if generate_slug(t["title"]) not in generated]
        
        if not available:
            print("\n✅ All topics have been generated! Add more topics to the TOPICS dict.")
            print(f"   Total articles: {len(generated)}")
            return
        
        # Pick random topics, prioritizing product-related ones (higher affiliate value)
        product_topics = [t for t in available if t["category"] in 
                         ("product_comparisons", "product_reviews_affiliate")]
        other_topics = [t for t in available if t not in product_topics]
        
        # Mix: 60% product, 40% other
        random.shuffle(product_topics)
        random.shuffle(other_topics)
        
        n_product = min(max(1, int(count * 0.6)), len(product_topics))
        n_other = min(count - n_product, len(other_topics))
        
        selected = product_topics[:n_product] + other_topics[:n_other]
        random.shuffle(selected)
        topics_to_generate = selected[:count]
    
    if dry_run:
        print(f"\n🔍 Dry run — would generate {len(topics_to_generate)} articles:\n")
        for t in topics_to_generate:
            slug = generate_slug(t["title"])
            status = "✅ Exists" if slug in generated else "⬜ New"
            print(f"  {status} [{t['category']}] {t['title']}")
            print(f"         → blogs/{slug}.html")
        print()
        return
    
    print(f"\n🚀 Generating {len(topics_to_generate)} articles using DeepSeek Flash V4...\n")
    
    for i, topic in enumerate(topics_to_generate):
        print(f"\n[{i+1}/{len(topics_to_generate)}] ", end="")
        result = generate_article(topic["title"], topic["category"])
        if result:
            print(f"   Saved: {result.name}")
    
    # Update sitemap and blog index after generation
    print(f"\n🔄 Updating sitemap and blog index...")
    # Re-run seo-tools to update sitemap
    os.system(f"python3 \"{ROOT}/seo-tools.py\"")
    
    new_total = len(get_generated_list())
    print(f"\n🎉 Done! Total articles: {new_total}")
    print(f"   Push to git to publish to https://www.anxietyfreepups.com/blogs/")


if __name__ == "__main__":
    main()