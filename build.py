#!/usr/bin/env python3
"""
Global Key Partners Static Site Generator
Generates the complete bilingual GKP website into dist/

Usage:
    pip install -r requirements.txt
    python build.py

Output: dist/ (deploy this folder to GitHub Pages, gh-pages branch)
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ──────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent
DIST_DIR      = BASE_DIR / 'dist'
TEMPLATES_DIR = BASE_DIR / 'templates'
DATA_DIR      = BASE_DIR / 'data'
ASSETS_DIR    = BASE_DIR / 'assets'

# ──────────────────────────────────────────────────────────────
# Jinja2
# ──────────────────────────────────────────────────────────────
env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(['html']),
    trim_blocks=True,
    lstrip_blocks=True,
)

def load(filename: str):
    with open(DATA_DIR / filename, encoding='utf-8') as f:
        return json.load(f)


def render(template_name: str, output_path: str, **ctx):
    tmpl = env.get_template(template_name)
    ctx.setdefault('current_year', datetime.now(timezone.utc).year)
    html = tmpl.render(**ctx)
    out  = DIST_DIR / output_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'    {output_path}')


# ──────────────────────────────────────────────────────────────
# URL helpers
# ──────────────────────────────────────────────────────────────
PREFIXES = {'en': '', 'de': 'de/', 'fr': 'fr/'}


def canonical_and_hreflang(lang: str, path: str) -> tuple[str, str, str]:
    """Return (canonical, hreflang_en, hreflang_de) for a page."""
    other = 'de' if lang == 'en' else 'en'
    other_prefix = PREFIXES[other]

    # Strip language prefix to get the core path
    current_prefix = PREFIXES[lang]
    core = path.lstrip('/')
    if core.startswith(current_prefix):
        core = core[len(current_prefix):]

    en_path  = f"/{core}"
    de_path  = f"/{other_prefix}{core}" if other == 'de' else f"/{core}"
    if lang == 'en':
        de_path = f"/de/{core}"
    else:
        en_path = f"/{core}"

    canonical = f"/{current_prefix}{core}"
    return canonical, en_path, de_path


# ──────────────────────────────────────────────────────────────
# Page builders
# ──────────────────────────────────────────────────────────────
def build_home(lang, cfg, services, where_we_operate, articles):
    prefix  = PREFIXES[lang]
    path    = f"{prefix}index.html"
    canon   = f"/{prefix}"
    titles  = {'en': 'Boutique Access Partner Switzerland', 'de': 'Boutique-Zugangspartner Schweiz', 'fr': "Partenaire d'Accès Boutique Suisse"}
    render('home.html', path,
           lang=lang, config=cfg,
           canonical=canon, hreflang_en='/', hreflang_de='/de/', hreflang_fr='/fr/',
           page_title=f"Global Key Partners | {titles.get(lang, titles['en'])}",
           meta_description=cfg['description'].get(lang) or cfg['description']['en'],
           services=services, where_we_operate=where_we_operate, articles=articles[:3])


def build_about(lang, cfg):
    prefix = PREFIXES[lang]
    core   = 'about/'
    canon  = f"/{prefix}{core}"
    titles = {'en': 'About GKP | Boutique Access Partner Switzerland', 'de': 'Über GKP | Boutique-Zugangspartner Schweiz', 'fr': "À propos de GKP | Partenaire d'Accès Boutique Suisse"}
    render('about.html', f"{prefix}{core}index.html",
           lang=lang, config=cfg,
           canonical=canon,
           hreflang_en=f"/{core}", hreflang_de=f"/de/{core}", hreflang_fr=f"/fr/{core}",
           page_title=titles.get(lang, titles['en']),
           meta_description=cfg['description'].get(lang) or cfg['description']['en'])


def build_contact(lang, cfg):
    prefix = PREFIXES[lang]
    core   = 'contact/'
    canon  = f"/{prefix}{core}"
    titles = {'en': 'Contact | Global Key Partners', 'de': 'Kontakt | Global Key Partners', 'fr': 'Contact | Global Key Partners'}
    metas  = {
        'en': 'Get in touch with Global Key Partners for confidential conversations and introductions in Switzerland and globally.',
        'de': 'Nehmen Sie Kontakt mit Global Key Partners auf für vertrauliche Gespräche und Kontaktvermittlung in der Schweiz und weltweit.',
        'fr': 'Contactez Global Key Partners pour des échanges confidentiels et des mises en relation en Suisse et à l\'international.',
    }
    render('contact.html', f"{prefix}{core}index.html",
           lang=lang, config=cfg,
           canonical=canon,
           hreflang_en=f"/{core}", hreflang_de=f"/de/{core}", hreflang_fr=f"/fr/{core}",
           page_title=titles.get(lang, titles['en']),
           meta_description=metas.get(lang, metas['en']))



def build_disclaimer(lang, cfg):
    prefix = PREFIXES[lang]
    core   = 'disclaimer/'
    canon  = f"/{prefix}{core}"
    titles = {'en': 'Legal Disclaimer | Global Key Partners', 'de': 'Rechtlicher Hinweis | Global Key Partners', 'fr': 'Avis Juridique | Global Key Partners'}
    metas  = {
        'en': 'GKP is not a licensed financial advisor or FINMA-supervised entity. Read our full legal disclaimer regarding introductions, advisory services, and the informational nature of this website.',
        'de': 'GKP ist kein zugelassener Finanzberater und untersteht nicht der FINMA. Lesen Sie unseren vollständigen Haftungsausschluss zu Vermittlungen, Beratungsleistungen und dem Informationsgehalt dieser Website.',
        'fr': "GKP n'est pas un conseiller financier agréé et n'est pas supervisé par la FINMA. Lisez notre avis juridique complet concernant les introductions, les services de conseil et la nature informative de ce site.",
    }
    render('disclaimer.html', f"{prefix}{core}index.html",
           lang=lang, config=cfg,
           canonical=canon,
           hreflang_en=f"/{core}", hreflang_de=f"/de/{core}", hreflang_fr=f"/fr/{core}",
           page_title=titles.get(lang, titles['en']),
           meta_description=metas.get(lang, metas['en']))

def build_privacy(lang, cfg):
    prefix = PREFIXES[lang]
    core   = 'privacy-policy/'
    canon  = f"/{prefix}{core}"
    titles = {'en': 'Privacy Policy | Global Key Partners', 'de': 'Datenschutzerklärung | Global Key Partners', 'fr': 'Politique de Confidentialité | Global Key Partners'}
    metas  = {
        'en': 'How Global Key Partners GmbH processes personal data: contact form, web analytics, hosting, and your rights under the Swiss FADP and GDPR.',
        'de': 'Wie die Global Key Partners GmbH Personendaten bearbeitet: Kontaktformular, Webanalyse, Hosting und Ihre Rechte nach DSG und DSGVO.',
        'fr': 'Comment Global Key Partners GmbH traite les données personnelles : formulaire de contact, analyse web, hébergement et vos droits selon la LPD et le RGPD.',
    }
    render('privacy.html', f"{prefix}{core}index.html",
           lang=lang, config=cfg,
           canonical=canon,
           hreflang_en=f"/{core}", hreflang_de=f"/de/{core}", hreflang_fr=f"/fr/{core}",
           page_title=titles.get(lang, titles['en']),
           meta_description=metas.get(lang, metas['en']))


def build_services(lang, cfg, services):
    prefix   = PREFIXES[lang]
    svc_base = 'services/'

    # Index
    canon = f"/{prefix}{svc_base}"
    idx_titles = {'en': 'Services | Global Key Partners', 'de': 'Services | Global Key Partners', 'fr': 'Services | Global Key Partners'}
    idx_metas  = {
        'en': 'Specialist access and introductions from GKP: strategic introductions, off-market sourcing, and strategic partnerships, Switzerland and globally.',
        'de': 'Spezialisierter Zugang und Kontaktvermittlung von GKP: strategische Kontaktvermittlung, Off-Market-Beschaffung und strategische Partnerschaften, Schweiz und weltweit.',
        'fr': 'Accès et introductions spécialisés de GKP : introductions stratégiques, sourcing hors marché et partenariats stratégiques, Suisse et international.',
    }
    render('services_index.html', f"{prefix}{svc_base}index.html",
           lang=lang, config=cfg,
           canonical=canon,
           hreflang_en=f"/{svc_base}", hreflang_de=f"/de/{svc_base}", hreflang_fr=f"/fr/{svc_base}",
           page_title=idx_titles.get(lang, idx_titles['en']),
           meta_description=idx_metas.get(lang, idx_metas['en']),
           services=services)

    # Individual service pages
    for svc in services:
        content = svc.get(lang) or svc.get('en')
        slug    = svc['slug']
        core    = f"{svc_base}{slug}/"
        canon   = f"/{prefix}{core}"
        render('service.html', f"{prefix}{core}index.html",
               lang=lang, config=cfg,
               canonical=canon,
               hreflang_en=f"/{core}", hreflang_de=f"/de/{core}", hreflang_fr=f"/fr/{core}",
               page_title=content['title'],
               meta_description=content['meta_description'],
               service=svc, content=content,
               all_services=services)


def build_where_we_operate(lang, cfg, where_we_operate):
    prefix  = PREFIXES[lang]
    core    = 'where-we-operate/'
    canon   = f"/{prefix}{core}"
    content = where_we_operate.get(lang) or where_we_operate['en']
    render('where_we_operate.html', f"{prefix}{core}index.html",
           lang=lang, config=cfg,
           canonical=canon,
           hreflang_en=f"/{core}", hreflang_de=f"/de/{core}", hreflang_fr=f"/fr/{core}",
           page_title=content['title'],
           meta_description=content['meta_description'],
           where_we_operate=where_we_operate)


def build_articles(lang, cfg, articles):
    prefix   = PREFIXES[lang]
    art_base = 'insights/'

    # Index
    canon = f"/{prefix}{art_base}"
    idx_titles = {'en': 'Insights | Global Key Partners', 'de': 'Einblicke | Global Key Partners', 'fr': 'Analyses | Global Key Partners'}
    idx_metas  = {
        'en': 'Private market insights from GKP: off-market real estate, family office deal flow, capital introduction, and Swiss private market strategy.',
        'de': 'Private Market Einblicke von GKP: Off-Market Immobilien, Family Office Deal Flow, Kapitalvermittlung und Schweizer Privatmarktstrategie.',
        'fr': 'Analyses des marchés privés par GKP : immobilier hors marché, deal flow des family offices, introduction en capital et stratégie des marchés privés suisses.',
    }
    render('articles_index.html', f"{prefix}{art_base}index.html",
           lang=lang, config=cfg,
           canonical=canon,
           hreflang_en=f"/{art_base}", hreflang_de=f"/de/{art_base}", hreflang_fr=f"/fr/{art_base}",
           page_title=idx_titles.get(lang, idx_titles['en']),
           meta_description=idx_metas.get(lang, idx_metas['en']),
           articles=articles)

    # Individual articles
    for art in articles:
        content   = art.get(lang) or art.get('en')
        slug      = art['slug']
        core      = f"{art_base}{slug}/"
        en_url    = f"/{core}"
        de_url    = f"/de/{core}"
        fr_url    = f"/fr/{core}"

        # Not every article is translated into all 3 languages yet. For a
        # language with no genuine translation we still render a page at
        # that URL (so existing internal links/nav keep working), but:
        #   - its canonical points back to the English original, so it
        #     doesn't compete with it as duplicate content
        #   - it's excluded from the hreflang set (hreflang must only list
        #     genuine alternate-language versions, not English fallbacks)
        #   - it's marked noindex so search engines consolidate on the
        #     canonical English page instead of indexing 3 copies
        available     = [l for l in ('en', 'de', 'fr') if l in art]
        is_translated = lang in available
        canon         = f"/{prefix}{core}" if is_translated else en_url

        render('article.html', f"{prefix}{core}index.html",
               lang=lang, config=cfg,
               canonical=canon,
               hreflang_en=en_url,
               hreflang_de=de_url if 'de' in available else None,
               hreflang_fr=fr_url if 'fr' in available else None,
               lang_switch_de=de_url, lang_switch_fr=fr_url,
               noindex=not is_translated,
               page_title=content['title'],
               meta_description=content['meta_description'],
               article=art, content=content, all_articles=articles)


# ──────────────────────────────────────────────────────────────
# Sitemap
# ──────────────────────────────────────────────────────────────
def build_sitemap(cfg, services, where_we_operate, articles):
    base = cfg['site_url'].rstrip('/')
    now  = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    urls = []

    def add(path, priority='0.7', freq='monthly'):
        urls.append({'loc': base + path, 'lastmod': now,
                     'changefreq': freq, 'priority': priority})

    for lang in ('en', 'de', 'fr'):
        p = PREFIXES[lang]
        add(f"/{p}",                    priority='1.0', freq='weekly')
        add(f"/{p}about/",              priority='0.6')
        add(f"/{p}contact/",            priority='0.7')
        add(f"/{p}services/",           priority='0.8')
        add(f"/{p}disclaimer/",         priority='0.3')
        add(f"/{p}privacy-policy/",     priority='0.3')
        add(f"/{p}insights/",           priority='0.7', freq='weekly')
        for svc in services:
            add(f"/{p}services/{svc['slug']}/",         priority='0.9')
        for art in articles:
            if lang in art:  # only sitemap genuine translations, not English fallbacks
                add(f"/{p}insights/{art['slug']}/",      priority='0.8', freq='weekly')

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(
            f'  <url>\n'
            f'    <loc>{u["loc"]}</loc>\n'
            f'    <lastmod>{u["lastmod"]}</lastmod>\n'
            f'    <changefreq>{u["changefreq"]}</changefreq>\n'
            f'    <priority>{u["priority"]}</priority>\n'
            f'  </url>'
        )
    lines.append('</urlset>')
    (DIST_DIR / 'sitemap.xml').write_text('\n'.join(lines), encoding='utf-8')
    print('    sitemap.xml')


def build_llms_txt(cfg, services, where_we_operate, articles):
    """Generate llms.txt, a concise, AI-readable map of the site (https://llmstxt.org)."""
    base = cfg['site_url'].rstrip('/')
    L = []
    L.append('# Global Key Partners')
    L.append('')
    L.append('> Global Key Partners GmbH (GKP) is a Swiss boutique access and introduction firm based in Cham, Zug. '
             'GKP connects UHNWIs, family offices, and private investors with curated off-market opportunities in Swiss '
             'real estate, hospitality, business acquisitions, and private markets. GKP acts exclusively as an introducer '
             'and business consultant; it is not a bank, asset manager, or financial adviser and is not supervised by FINMA.')
    L.append('')
    L.append('Site languages: English (default), German (/de/), French (/fr/). Contact: ' + base + '/contact/')
    L.append('')
    L.append('## Services')
    L.append('')
    for svc in services:
        c = svc['en']
        L.append(f"- [{c['h1']}]({base}/services/{svc['slug']}/): {c.get('meta_description','')}")
    L.append('')
    L.append('## Insights')
    L.append('')
    for art in articles:
        c = art['en']
        L.append(f"- [{c['h1']}]({base}/insights/{art['slug']}/): {c.get('meta_description','')}")
    L.append('')
    L.append('## Company')
    L.append('')
    L.append(f"- [About GKP]({base}/about/): Founders, mission, and principles of Global Key Partners.")
    L.append(f"- [Contact]({base}/contact/): Start a confidential conversation with GKP.")
    L.append(f"- [Agent context]({base}/agents.md): Extended structured context for AI agents.")
    L.append(f"- [Legal disclaimer]({base}/disclaimer/): GKP's regulatory positioning as an introducer, not a financial adviser.")
    L.append(f"- [Privacy policy]({base}/privacy-policy/): How GKP processes personal data.")
    L.append('')
    (DIST_DIR / 'llms.txt').write_text('\n'.join(L), encoding='utf-8')
    print('    llms.txt')


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────
def build():
    print()
    print('══════════════════════════════════════════════════')
    print('  Global Key Partners, Static Site Build')
    print('══════════════════════════════════════════════════')

    # Clean output, purge contents item by item so stale pages never survive a build
    DIST_DIR.mkdir(exist_ok=True)
    leftovers = []
    for child in DIST_DIR.iterdir():
        try:
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink()
        except OSError as e:
            leftovers.append(f'{child.name} ({e})')
    if leftovers:
        raise SystemExit(
            '  ✗ Could not fully clean dist/, stale files would be deployed:\n    '
            + '\n    '.join(leftovers))
    print('  ✓ dist/ cleaned')

    # Assets
    shutil.copytree(ASSETS_DIR, DIST_DIR / 'assets', dirs_exist_ok=True)
    print('  ✓ assets/')

    # Data
    cfg              = load('config.json')
    services         = load('services.json')
    where_we_operate = load('where_we_operate.json')
    articles         = load('articles.json')

    # Build pages per language
    for lang in ('en', 'de', 'fr'):
        label = {'en': '🇬🇧 EN', 'de': '🇩🇪 DE', 'fr': '🇫🇷 FR'}[lang]
        print(f'\n  {label}')
        build_home(lang, cfg, services, where_we_operate, articles)
        build_about(lang, cfg)
        build_contact(lang, cfg)
        build_disclaimer(lang, cfg)
        build_privacy(lang, cfg)
        build_services(lang, cfg, services)
        build_articles(lang, cfg, articles)

    # Global
    print('\n  🌐 Global')
    build_sitemap(cfg, services, where_we_operate, articles)
    build_llms_txt(cfg, services, where_we_operate, articles)

    # Static files
    for fname in ('robots.txt', 'agents.md'):
        src = BASE_DIR / fname
        if src.exists():
            shutil.copy(src, DIST_DIR / fname)
            print(f'    {fname}')

    # CNAME for custom domain
    (DIST_DIR / 'CNAME').write_text('globalkeypartners.com\n', encoding='utf-8')
    print('    CNAME')

    # 404 page (single global file, not language-prefixed — hosts serve this
    # for any unmatched path regardless of /de/ or /fr/. No genuine /de/404.html
    # or /fr/404.html exist, so don't advertise them via hreflang; noindex since
    # error pages should never be indexed; language switcher sends a lost
    # visitor to the relevant homepage instead of a 404-on-a-404.)
    render('404.html', '404.html',
           lang='en', config=cfg,
           canonical='/404.html',
           hreflang_en='/404.html',
           lang_switch_de='/de/', lang_switch_fr='/fr/',
           noindex=True,
           page_title='Page Not Found | Global Key Partners',
           meta_description='The page you are looking for does not exist.')
    print('    404.html')

    # Config sanity checks, warn loudly if launch-critical IDs are missing
    warnings = []
    fid = cfg.get('formspree_id', '')
    if not fid or 'YOUR_' in fid:
        warnings.append('formspree_id is not set, the contact form will NOT deliver messages!')
    if not cfg.get('google_analytics'):
        warnings.append('google_analytics is empty, no traffic tracking (GA4 ID, e.g. G-XXXXXXXXXX)')
    if not cfg.get('search_console_verification'):
        warnings.append('search_console_verification is empty (Google Search Console not verified)')
    if warnings:
        print('\n  ⚠️  CONFIG WARNINGS (data/config.json):')
        for w in warnings:
            print(f'     ⚠️  {w}')

    # Summary
    total = sum(1 for _ in DIST_DIR.rglob('*.html'))
    print(f'\n══════════════════════════════════════════════════')
    print(f'  ✓ Build complete: {total} HTML pages → dist/')
    print(f'══════════════════════════════════════════════════\n')


if __name__ == '__main__':
    build()
