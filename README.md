# Global Key Partners: Website

Static site generator for globalkeypartners.com. Builds a fully bilingual (EN/DE), SEO-optimised, LLM-ready website from structured data files.

## What this generates

**43 HTML pages** including:
- Homepage (EN + DE)
- 5 service pages (EN/DE/FR): strategic introductions, off-market real estate, capital introduction, business acquisitions, hospitality investments
- 5 location pages (EN + DE): Switzerland, Zurich, Geneva, Zug, Singapore
- 4 insight articles (EN + DE)
- Index pages for services, locations, insights
- About, Contact, 404
- `sitemap.xml`, `robots.txt`, `agents.md`, `CNAME`

Every page includes: proper `<title>` + `<meta description>`, canonical URL, hreflang tags, Open Graph, Twitter Card, and Schema.org JSON-LD (Organization, Service, FAQPage, BreadcrumbList, Article).

---

## Quick start

```bash
pip install -r requirements.txt
python build.py
# Output: dist/
```

The `dist/` folder is what gets deployed to GitHub Pages.

---

## GitHub setup (one-time)

1. Create a new GitHub repository (e.g. `gkp-website`)
2. Push this project to the `main` branch
3. Go to **Settings → Pages** → set source to **"GitHub Actions"** (not gh-pages branch, the Actions workflow handles it)
4. Go to **Settings → Pages** → add your custom domain: `globalkeypartners.com`
5. In Cloudflare, point your DNS to GitHub Pages:
   - `CNAME` record: `globalkeypartners.com` → `your-username.github.io`
   - Or use Cloudflare proxied A records for GitHub Pages IPs
6. Enable **HTTPS** in GitHub Pages settings

After that, every push to `main` automatically rebuilds and deploys the site.

---

## Adding content

All content is in `data/`. Edit JSON, push to GitHub, site rebuilds automatically.

### Add a new insight article
In `data/articles.json`, append a new object:
```json
{
  "slug": "your-article-slug",
  "published": "2026-06-01",
  "reading_time": 5,
  "en": {
    "title": "Page title | GKP Insights",
    "h1": "Your Article Heading",
    "meta_description": "...",
    "summary": "One sentence summary for cards.",
    "body": [
      {"text": "First paragraph..."},
      {"heading": "A subheading", "text": "Body text..."},
      {"heading": "A bullet list", "bullets": ["Item 1", "Item 2"]}
    ],
    "faqs": [
      {"q": "Question?", "a": "Answer."}
    ]
  },
  "de": { ... }
}
```

### Add a new location page
In `data/locations.json`, append a new location object following the same structure.

### Change the contact form
1. Sign up at [formspree.io](https://formspree.io) (free tier)
2. Create a form, copy the form ID (e.g. `xpzgkrqb`)
3. In `data/config.json`, set `"formspree_id": "xpzgkrqb"`

### Add team photos
Drop images into `assets/images/`:
- `dennis-tong.jpg` (recommended: 200×240px)
- `vlora-rexhepi.jpg` (recommended: 200×240px)
- `logo.png` (white version of the GKP logo)
- `og-image.jpg` (1200×630px for social sharing)
- `favicon.png` (32×32px)
- `hero-bg.jpg` (high-resolution background for the hero)

### Add Google Analytics
In `data/config.json`, set `"google_analytics": "G-XXXXXXXXXX"`.

---

## Adding more languages

The build system is designed for easy language expansion. To add Thai (`th`):

1. Add `"th"` content blocks to service, location, and article JSON
2. Add `"th"` nav to `data/config.json`
3. In `build.py`, add `'th'` to the language loop: `for lang in ('en', 'de', 'th'):`
4. Update the language switcher in `templates/base.html`

---

## SEO & LLM features built in

- **Canonical URLs** on every page
- **Hreflang** tags for EN/DE bilingual
- **Schema.org JSON-LD**: Organization, Service, FAQPage, Article, BreadcrumbList, LocalBusiness, Person
- **robots.txt** with explicit permissions for GPTBot, ClaudeBot, PerplexityBot
- **agents.md**, context file for AI assistants describing GKP's services
- **Sitemap.xml** with all pages, priorities, and lastmod dates
- **FAQPage schema** on all service pages and articles, directly feeds AI answer engines

---

## Project structure

```
gkp-website/
├── build.py              ← Site generator (run this)
├── requirements.txt
├── robots.txt            ← AI-crawler friendly
├── agents.md             ← Context for AI assistants
├── data/
│   ├── config.json       ← Site config, nav, UI strings
│   ├── services.json     ← 6 service pages (EN + DE)
│   ├── locations.json    ← 5 location pages (EN + partial DE)
│   └── articles.json     ← 4 insight articles (EN + partial DE)
├── templates/
│   ├── base.html         ← Master layout with all head/schema/nav/footer
│   ├── home.html
│   ├── service.html
│   ├── location.html
│   ├── article.html
│   ├── contact.html
│   ├── about.html
│   ├── services_index.html
│   ├── locations_index.html
│   ├── articles_index.html
│   └── 404.html
├── assets/
│   ├── css/style.css     ← Full design system (green + gold theme)
│   ├── js/main.js        ← Minimal JS (nav, FAQ, scroll)
│   └── images/           ← Add your images here
├── dist/                 ← Generated output (deploy this)
└── .github/
    └── workflows/
        └── deploy.yml    ← Auto-deploy on push to main
```
