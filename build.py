#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sestaví statický web Apartmán Mili ve třech jazycích (CS, PL, DE).

Použití:   python3 build.py
Výstup:    index.html (CS), pl/index.html, de/index.html, robots.txt, sitemap.xml (jen s site_url)
Úpravy:    texty a konfigurace v content.py, vzhled v assets/css/style.css
"""
import json
import datetime
import html
from pathlib import Path

from content import CONFIG, T, LANG_ORDER, HERO_PHOTO, GALLERY, LOCATION_PHOTO, PHOTOS_WATERMARKED

ROOT = Path(__file__).parent
YEAR = datetime.date.today().year
esc = html.escape


def rel(lang):
    """Prefix cesty k assetům podle hloubky stránky."""
    return "" if T[lang]["path"] == "" else "../"


def page_href(src_lang, dst_lang):
    return rel(src_lang) + T[dst_lang]["path"] + "index.html"


def img(lang, photo, cls="", eager=False):
    """<img> s rozměry (kvůli CLS) a popisným alt textem v daném jazyce."""
    r = rel(lang)
    loading = "eager" if eager else "lazy"
    prio = ' fetchpriority="high"' if eager else ""
    c = f' class="{cls}"' if cls else ""
    return (
        f'<img{c} src="{r}assets/img/{photo["file"]}" width="{photo["w"]}" height="{photo["h"]}" '
        f'alt="{esc(photo["alt"][lang])}" loading="{loading}" decoding="async"{prio}>'
    )


def booking_link(t):
    url = CONFIG["booking_url"]
    if url:
        return f'href="{esc(url)}" target="_blank" rel="noopener"'
    return 'href="#contact"'


def mapy_url():
    return f'https://mapy.cz/zakladni?x={CONFIG["lon"]}&y={CONFIG["lat"]}&z=16&source=coor&id={CONFIG["lon"]}%2C{CONFIG["lat"]}'


def google_url():
    return f'https://www.google.com/maps/search/?api=1&query={CONFIG["lat"]},{CONFIG["lon"]}'


def gps_text():
    return f'{CONFIG["lat"]:.6f} N, {CONFIG["lon"]:.6f} E'


LOGO_MARK = (
    '<svg class="logo__mark" viewBox="0 0 32 32" width="30" height="30" aria-hidden="true" focusable="false">'
    '<path d="M3 26 L13 9 L18 17 L21 12 L29 26 Z" fill="currentColor"/>'
    '<path d="M13 9 L15.6 13.4 L13 12.2 L10.4 13.4 Z" fill="var(--paper)"/>'
    "</svg>"
)


def json_ld(lang):
    t = T[lang]
    data = {
        "@context": "https://schema.org",
        "@type": "LodgingBusiness",
        "name": CONFIG["name"],
        "description": t["jsonld_desc"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": CONFIG["street"],
            "addressLocality": CONFIG["locality"],
            "addressCountry": CONFIG["country"],
        },
        "geo": {"@type": "GeoCoordinates", "latitude": CONFIG["lat"], "longitude": CONFIG["lon"]},
        "hasMap": google_url(),
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": n, "value": True}
            for n in ("Wi-Fi", "TV", "Parking")
        ],
    }
    if CONFIG["postal_code"]:
        data["address"]["postalCode"] = CONFIG["postal_code"]
    if CONFIG["email"]:
        data["email"] = CONFIG["email"]
    if CONFIG["phone"]:
        data["telephone"] = CONFIG["phone"]
    if CONFIG["site_url"]:
        data["url"] = CONFIG["site_url"].rstrip("/") + "/" + t["path"]
    return json.dumps(data, ensure_ascii=False, indent=2)


def render(lang):
    t = T[lang]
    r = rel(lang)
    book = booking_link(t)

    # --- hlavička / navigace
    nav_items = "".join(
        f'<li><a href="#{k}">{esc(t["nav"][k])}</a></li>'
        for k in ("about", "gallery", "amenities", "location", "booking", "contact")
    )
    def lang_link(l):
        current = ' aria-current="true"' if l == lang else ""
        return (
            f'<a href="{page_href(lang, l)}" hreflang="{T[l]["html_lang"]}" lang="{T[l]["html_lang"]}"'
            f'{current} title="{esc(T[l]["lang_name"])}">{T[l]["code"]}</a>'
        )

    lang_links = "".join(lang_link(l) for l in LANG_ORDER)

    def lang_nav_link(l):
        current = ' aria-current="true"' if l == lang else ""
        return (
            f'<a href="{page_href(lang, l)}" hreflang="{T[l]["html_lang"]}" lang="{T[l]["html_lang"]}"'
            f'{current}>{esc(T[l]["lang_name"])}</a>'
        )

    lang_nav = "".join(lang_nav_link(l) for l in LANG_ORDER)

    # --- hero fakta
    facts = "".join(
        f'<li><strong>{esc(v)}</strong><span>{esc(lbl)}</span></li>' for v, lbl in t["facts"]
    )

    # --- galerie
    gal_items = []
    for i, photo in enumerate(GALLERY):
        gal_items.append(
            '<li class="gallery__item">'
            f'<button type="button" class="gallery__btn" data-index="{i}">'
            f'{img(lang, photo)}</button></li>'
        )
    gallery = "".join(gal_items)

    # --- vybavení
    amen = "".join(
        f'<div class="amen__group"><h3>{esc(title)}</h3><ul>'
        + "".join(f"<li>{esc(i)}</li>" for i in items)
        + "</ul></div>"
        for title, items in t["amen_groups"]
    )

    # --- lokalita
    def dl(rows):
        return "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in rows)

    getting = "".join(
        f"<li><strong>{esc(m)}</strong><span>{esc(txt)}</span></li>" for m, txt in t["getting"]
    )

    # --- kontakt
    contact_rows = [
        (t["address_label"], esc(CONFIG["street"] + (", " + CONFIG["postal_code"] if CONFIG["postal_code"] else "") + ", " + CONFIG["locality"]))
    ]
    if CONFIG["phone"]:
        tel = "".join(ch for ch in CONFIG["phone"] if ch.isdigit() or ch == "+")
        contact_rows.append((t["phone_label"], f'<a href="tel:{tel}">{esc(CONFIG["phone"])}</a>'))
    if CONFIG["whatsapp"]:
        wa = "".join(ch for ch in CONFIG["whatsapp"] if ch.isdigit())
        contact_rows.append((t["whatsapp_label"], f'<a href="https://wa.me/{wa}" rel="noopener">{esc(CONFIG["whatsapp"])}</a>'))
    if CONFIG["email"]:
        contact_rows.append((t["email_label"], f'<a href="mailto:{esc(CONFIG["email"])}">{esc(CONFIG["email"])}</a>'))
    contact_rows.append((t["gps_label"], esc(gps_text())))
    contact = "".join(f"<div><dt>{esc(a)}</dt><dd>{b}</dd></div>" for a, b in contact_rows)

    book_missing = (
        "" if CONFIG["booking_url"] else f'<p class="todo-note">{esc(t["book_missing"])}</p>'
    )

    # --- hreflang / canonical / robots
    head_extra = ""
    if CONFIG["site_url"]:
        base = CONFIG["site_url"].rstrip("/") + "/"
        head_extra += f'<link rel="canonical" href="{base}{t["path"]}">\n'
        for l in LANG_ORDER:
            head_extra += f'<link rel="alternate" hreflang="{T[l]["html_lang"]}" href="{base}{T[l]["path"]}">\n'
        head_extra += f'<link rel="alternate" hreflang="x-default" href="{base}">\n'
        head_extra += f'<meta property="og:url" content="{base}{t["path"]}">\n'
    robots = "index, follow" if CONFIG["indexing"] else "noindex, nofollow"

    fallbacks = json.dumps(
        {"prev": t["prev"], "next": t["next"], "close": t["close"], "menu": t["menu"]},
        ensure_ascii=False,
    )

    operator = f'<p>{esc(CONFIG["operator"])}</p>' if CONFIG["operator"] else ""

    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t['meta_title'])}</title>
<meta name="description" content="{esc(t['meta_desc'])}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#1f3a33">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(t['meta_title'])}">
<meta property="og:description" content="{esc(t['meta_desc'])}">
<meta property="og:locale" content="{t['html_lang']}">
{head_extra}<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{r}assets/css/style.css">
<script type="application/ld+json">
{json_ld(lang)}
</script>
</head>
<body>
<a class="skip" href="#main">{esc(t['skip'])}</a>

<header class="header" id="top">
  <div class="header__inner">
    <a class="logo" href="#top" aria-label="{esc(CONFIG['name'])}">{LOGO_MARK}<span>{esc(CONFIG['name'])}</span></a>
    <nav class="nav" id="nav" aria-label="Menu">
      <ul>{nav_items}</ul>
      <div class="langnav" role="group" aria-label="Language">{lang_nav}</div>
    </nav>
    <div class="header__tools">
      <div class="lang" role="group" aria-label="Language">{lang_links}</div>
      <a class="btn btn--small header__cta" {book}>{esc(t['cta_book_short'])}</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">{esc(t['menu'])}</button>
    </div>
  </div>
</header>

<main id="main">

<section class="hero">
  {img(lang, HERO_PHOTO, 'hero__img', eager=True)}
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="hero__content wrap">
    <p class="eyebrow eyebrow--light">{esc(t['hero_eyebrow'])}</p>
    <h1>{esc(t['hero_title'])}</h1>
    <p class="hero__lead">{esc(t['hero_lead'])}</p>
    <div class="hero__actions">
      <a class="btn btn--primary" {book}>{esc(t['cta_book'])} <span class="arrow" aria-hidden="true">→</span></a>
      <a class="btn btn--ghost" href="#about">{esc(t['hero_secondary'])}</a>
    </div>
  </div>
</section>

<section class="facts" aria-label="{esc(CONFIG['name'])}">
  <ul class="wrap facts__list">{facts}</ul>
</section>

<section class="section" id="about">
  <div class="wrap about">
    <div class="about__text reveal">
      <p class="eyebrow">{esc(t['about_eyebrow'])}</p>
      <h2>{esc(t['about_title'])}</h2>
      <p>{esc(t['about_p1'])}</p>
      <p>{esc(t['about_p2'])}</p>
    </div>
    <div class="about__side reveal">
      <h3>{esc(t['sleep_title'])}</h3>
      <ul class="plain">{''.join(f'<li>{esc(i)}</li>' for i in t['sleep_items'])}</ul>
      <p class="muted">{esc(t['sleep_note'])}</p>
      <h3>{esc(t['rooms_title'])}</h3>
      <ul class="plain">{''.join(f'<li>{esc(i)}</li>' for i in t['rooms'])}</ul>
    </div>
  </div>
</section>

<section class="section section--alt" id="gallery">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">{esc(t['gallery_eyebrow'])}</p>
      <h2>{esc(t['gallery_title'])}</h2>
      <p class="muted">{esc(t['gallery_hint'])}</p>
    </div>
    <ul class="gallery">{gallery}</ul>
  </div>
</section>

<section class="section" id="amenities">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">{esc(t['amen_eyebrow'])}</p>
      <h2>{esc(t['amen_title'])}</h2>
    </div>
    <div class="amen reveal">{amen}</div>
  </div>
</section>

<section class="section section--dark" id="location">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow eyebrow--light">{esc(t['loc_eyebrow'])}</p>
      <h2>{esc(t['loc_title'])}</h2>
      <p>{esc(t['loc_lead'])}</p>
    </div>
    <figure class="loc__photo reveal">{img(lang, LOCATION_PHOTO)}</figure>
    <div class="loc reveal">
      <div>
        <h3>{esc(t['dist_title'])}</h3>
        <dl class="dist">{dl(t['dist'])}</dl>
      </div>
      <div>
        <h3>{esc(t['far_title'])}</h3>
        <dl class="dist">{dl(t['far'])}</dl>
      </div>
      <div>
        <h3>{esc(t['getting_title'])}</h3>
        <ul class="getting">{getting}</ul>
      </div>
    </div>
    <div class="seasons reveal">
      <div>
        <p class="eyebrow eyebrow--light">{esc(t['seasons_eyebrow'])}</p>
        <h3>{esc(t['winter_title'])}</h3>
        <p>{esc(t['winter_text'])}</p>
      </div>
      <div>
        <p class="eyebrow eyebrow--light" aria-hidden="true">&nbsp;</p>
        <h3>{esc(t['summer_title'])}</h3>
        <p>{esc(t['summer_text'])}</p>
      </div>
    </div>
  </div>
</section>

<section class="section book" id="booking">
  <div class="wrap book__inner reveal">
    <div>
      <p class="eyebrow">{esc(t['book_eyebrow'])}</p>
      <h2>{esc(t['book_title'])}</h2>
      <p>{esc(t['book_text'])}</p>
      {book_missing}
    </div>
    <a class="btn btn--primary btn--large" {book}>{esc(t['book_cta'])} <span class="arrow" aria-hidden="true">→</span></a>
  </div>
</section>

<section class="section" id="contact">
  <div class="wrap contact">
    <div class="reveal">
      <p class="eyebrow">{esc(t['contact_eyebrow'])}</p>
      <h2>{esc(t['contact_title'])}</h2>
      <p>{esc(t['contact_lead'])}</p>
      <dl class="contact__list">{contact}</dl>
    </div>
    <div class="map reveal">
      <h3>{esc(t['map_title'])}</h3>
      <p class="muted">{esc(t['map_note'])}</p>
      <p class="map__links">
        <a class="btn btn--outline" href="{esc(mapy_url())}" target="_blank" rel="noopener">{esc(t['map_mapy'])}</a>
        <a class="btn btn--outline" href="{esc(google_url())}" target="_blank" rel="noopener">{esc(t['map_google'])}</a>
      </p>
    </div>
  </div>
</section>

</main>

<footer class="footer">
  <div class="wrap footer__inner">
    <a class="logo logo--light" href="#top" aria-label="{esc(CONFIG['name'])}">{LOGO_MARK}<span>{esc(CONFIG['name'])}</span></a>
    <div>
      <p>{esc(CONFIG['street'])}, {esc(CONFIG['locality'])}</p>
      {operator}
    </div>
    <div class="lang lang--light" role="group" aria-label="Language">{lang_links}</div>
  </div>
  <p class="wrap footer__legal">© {YEAR} {esc(CONFIG['name'])}. {esc(t['footer_rights'])}</p>
</footer>

<div class="sticky-cta"><a class="btn btn--primary" {book}>{esc(t['cta_book'])} <span class="arrow" aria-hidden="true">→</span></a></div>

<dialog class="lightbox" id="lightbox" aria-label="{esc(t['gallery_title'])}">
  <button class="lightbox__close" type="button" aria-label="{esc(t['close'])}">×</button>
  <button class="lightbox__nav lightbox__nav--prev" type="button" aria-label="{esc(t['prev'])}">‹</button>
  <figure class="lightbox__fig"><img alt=""></figure>
  <button class="lightbox__nav lightbox__nav--next" type="button" aria-label="{esc(t['next'])}">›</button>
</dialog>

<script>document.documentElement.classList.add('js');</script>
<script src="{r}assets/js/main.js" defer></script>
</body>
</html>
"""


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<rect width="32" height="32" rx="6" fill="#1f3a33"/>
<path d="M5 25 L14 9 L18.5 16.5 L21 12.5 L27 25 Z" fill="#f4f0e8"/>
<path d="M14 9 L16.2 12.8 L14 11.8 L11.8 12.8 Z" fill="#1f3a33"/>
</svg>
"""


def check_languages():
    """Každý jazyk musí mít stejné klíče jako čeština (a alt texty fotek). Užitečné při přidání EN."""
    base = set(T["cs"].keys())
    problems = []
    for lang in LANG_ORDER:
        if lang not in T:
            problems.append(f"{lang}: chybí slovník T['{lang}'] v content.py")
            continue
        missing = base - set(T[lang].keys())
        if missing:
            problems.append(f"{lang}: chybí klíče {sorted(missing)}")
        for p in [HERO_PHOTO, LOCATION_PHOTO] + GALLERY:
            if lang not in p["alt"]:
                problems.append(f"{lang}: chybí alt text u {p['file']}")
    if problems:
        raise SystemExit("Chyba v překladech:\n - " + "\n - ".join(problems))


def main():
    warnings = []
    check_languages()
    for lang in LANG_ORDER:
        out = ROOT / T[lang]["path"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(lang), encoding="utf-8")
        print("OK ", out.relative_to(ROOT))

    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8")

    # robots.txt a sitemap
    if CONFIG["indexing"] and CONFIG["site_url"]:
        base = CONFIG["site_url"].rstrip("/") + "/"
        (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n", encoding="utf-8")
        urls = "".join(f"<url><loc>{base}{T[l]['path']}</loc></url>" for l in LANG_ORDER)
        (ROOT / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
            encoding="utf-8",
        )
    else:
        (ROOT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")

    # TODO přehled
    if not CONFIG["booking_url"]:
        warnings.append("booking_url: chybí odkaz na rezervační systém (tlačítka míří na #contact)")
    if not CONFIG["email"] and not CONFIG["phone"]:
        warnings.append("email/phone: chybí kontakt")
    if not CONFIG["site_url"]:
        warnings.append("site_url: chybí, nevzniká canonical/hreflang/sitemap")
    if not CONFIG["indexing"]:
        warnings.append("indexing=False: web je pro vyhledávače zakázaný (noindex + robots.txt)")
    if not CONFIG["postal_code"]:
        warnings.append("postal_code: chybí PSČ")
    names = [p["file"] for p in [HERO_PHOTO, LOCATION_PHOTO] + GALLERY]
    missing = [n for n in names if not (ROOT / "assets" / "img" / n).exists()]
    if missing:
        warnings.append("chybí fotky v assets/img/: " + ", ".join(missing))
    if PHOTOS_WATERMARKED:
        warnings.append("fotky mají vodoznak ceskehory.cz: nahradit originály bez vodoznaku (stejné názvy souborů)")
    if warnings:
        print("\nTODO / upozornění:")
        for w in warnings:
            print(" -", w)


if __name__ == "__main__":
    main()
