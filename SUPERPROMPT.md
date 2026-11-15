# SUPERPROMPT – web Apartmán Mili (Kořenov)

> Zadání pro Claude Code. Verze 2.0 · 15. 11. 2026 · připravil Lukáš (webmaster) s Claude.
> Vychází z původního zadání pro ideTone.cz (záloha v `podklady/SUPERPROMPT-idetone-original.md`, jen pro inspiraci postupu, obsah z něj se nepřebírá).

---

## 0. Než začneš

1. Projdi `content.py` (texty, konfigurace), `build.py` (generátor), `assets/css/style.css`, `assets/js/main.js` a vygenerované `index.html`, `pl/index.html`, `de/index.html`. Verze 0.1 už existuje a funguje, **navazuj na ni, nepřepisuj ji od nuly**.
2. Pracuj po fázích (kapitola 10). Na konci každé fáze se zastav, ukaž screenshoty (390 / 768 / 1440 px, všechny 3 jazyky) a počkej na schválení.
3. **Nic si nevymýšlej.** Ceny, kontakty, vzdálenosti, vybavení a pravidla ber jen z podkladů (kapitola 3). Co chybí, nech prázdné v `CONFIG` nebo označ `TODO(majitel): …` a zapiš do seznamu otevřených bodů (kapitola 11).
4. Komunikuj se mnou česky, stručně, kroky číslované.

---

## 1. Kontext a cíl

**Apartmán Mili** je 1+1 apartmán (32 m²) v Kořenově v Jizerských horách, který pronajímají známí. Hosté jsou z **Česka, Polska a Německa**.

- **Cíl webu:** hosté si během pár vteřin udělají představu o apartmánu a lokalitě a **přejdou do rezervačního systému** (primární akce na každé stránce: „Rezervovat termín“). Web sám rezervace nepřijímá a neukazuje ceny, ty jsou v rezervačním systému.
- **Cílové skupiny:** páry, rodiny s dětmi, cyklisté, běžkaři a lyžaři, pěší turisté, majitelé psů (po domluvě). Většina návštěv bude z mobilu.
- **Tón:** klidný, přátelský, věcný. Vykání. Žádné superlativy („nejlepší“, „dokonalý“), žádné klišé o „oáze klidu“.
- **Kdo web spravuje:** Lukáš (webmaster). Texty a konfigurace se mění v `content.py`, web se přegeneruje příkazem `python3 build.py`.

---

## 2. Technologie a rozhodnutí

| Oblast | Řešení |
|---|---|
| Stack | **Čistě statické HTML/CSS/JS bez frameworku.** Tři jazykové verze generuje `build.py` z jednoho zdroje (`content.py`). Důvod: web má jednu stránku na jazyk, žádný CMS není potřeba. Když později vznikne potřeba admin panelu nebo mnoha stránek, zvaž migraci na Astro (viz původní zadání ideTone) a navrhni mi ji, neprováděj ji sám. |
| Jazyky | CS (kořen), PL (`/pl/`), DE (`/de/`). Přepínač v hlavičce a v patičce. **Bez automatického přesměrování podle jazyka prohlížeče** (škodí SEO i uživatelům). **Angličtina přijde později a architektura s ní počítá:** doplnit `T["en"]` (stejné klíče jako CS, včetně `alt` u fotek) a přidat `"en"` do `ENABLED_LANGS` v `content.py`. `build.py` hlídá úplnost překladů a vygeneruje `/en/`, hreflang i přepínač. Při návrhu nových prvků počítej se 4 jazyky (např. šířka přepínače v hlavičce na 320 px). |
| Styly | Vlastní CSS s custom properties (`:root` v `style.css`). Žádný Tailwind ani UI kit. |
| JavaScript | Minimum, vanilla: menu, lightbox galerie, odkrývání sekcí. Web musí fungovat i bez JS. |
| Písma | Teď systémový stack (serif nadpisy, system-ui text). Pokud přidáš webfont, **jen self-hosting** (`@fontsource` nebo vlastní woff2), `font-display: swap`. **Žádné Google Fonts CDN** (GDPR, hlavně kvůli německým návštěvníkům). |
| Hosting | **GitHub Pages**, nejdřív testovací provoz na `https://<uzivatel>.github.io/<repo>/`. Cesty jsou relativní (`assets/…`, `../`), takže podsložka nevadí. Testovací verze má `noindex` (řízeno `CONFIG["indexing"]`). |
| Kvalita | `python3 build.py` musí běžet bez chyb, Playwright pro screenshoty a základní testy, Prettier pro CSS/JS. |
| Git | Složka `apartman-mili` zatím není git repozitář. Na začátku mi řekni, jestli ho založit tady, nebo zda je nadřazená složka `Weby` repo s `.gitignore` (nic sám neměň). Commity malé, česky: `feat:`, `fix:`, `content:`, `style:`. |

---

## 3. Zdroje pravdy o apartmánu

Jediný dosavadní zdroj je inzerát na ceskehory.cz (https://www.ceskehory.cz/ubytovani/apartman-mili-korenov.html). **Inzerát je označen jako archivovaný a může být neaktuální**, všechny údaje proto ověř s majiteli (`TODO(majitel)`).

| Údaj | Hodnota z inzerátu | Poznámka |
|---|---|---|
| Typ, plocha | 1+1, 32 m², přízemí, dům „Beruška“ | |
| Adresa, GPS | Kořenov 659; 50.761286 N, 15.384355 E | PSČ chybí |
| Lůžka | 1 manželská postel, 1 samostatné lůžko, 1 rozkládací pohovka, 1 přistýlka | **Počet hostů: 4** (potvrzeno zadavatelem 15. 11. 2026) |
| Dispozice | předsíň, koupelna (sprchový kout, WC), kuchyně s jídelním stolem, obývací/ložnicový pokoj | **Pozor:** fotky ukazují obývák s pohovkou, pokoj s manželskou postelí a zvlášť pokoj s jednolůžkem, což neodpovídá „1+1“. `TODO(majitel)`: ověřit skutečnou dispozici a podle ní upravit „Spaní“ a „Dispozice“ v `content.py` |
| Kuchyň | sporák s troubou, mikrovlnka, myčka, lednice, rychlovarná konvice, kompletní nádobí | |
| Ostatní | Wi-Fi, TV, ložní prádlo, ručníky, fén, sušák na obuv, parkování zdarma u domu, ohniště | |
| Pravidla | domácí mazlíčci po domluvě; vhodné pro rodiny a cyklisty; bez stravy | |
| Vzdálenosti | cyklostezka 100 m, běžecké tratě 1 km, vleky 1,4 km, COOP 900 m, restaurace 900 m, bus 300 m, nádraží Kořenov 2 km | orientační |
| Výlety | Harrachov 5 km, Jizerka 6 km, Rejdice (areál) 7 km, Rokytnice n. J. (areál) 11 km | |
| Příjezd | silnice č. 10 směr Harrachov, pak 300 m po udržované cestě; přímý autobus z Prahy (Černý Most) | |
| **Chybí** | ceny, kontakt (telefon, e-mail), odkaz na rezervační systém, PSČ, provozovatel (jméno/IČO), pravidla příjezdu/odjezdu, storno podmínky | `CONFIG` + `TODO(majitel)` |

Texty, které nejsou v inzerátu (např. věty o atmosféře), označ v kódu komentářem `NÁVRH: ke schválení`.

---

## 4. Vizuální směr (verze 0.1)

**Horský domov, ne hotel:** tmavá smrková zeleň, teplá březová/krémová, měděný akcent pro akce. Klidné, vzdušné, čitelné na mobilu.

| Token | Hex | Použití |
|---|---|---|
| `--spruce` | `#1f3a33` | Logo, tmavé sekce (Lokalita), patička |
| `--paper` | `#fbf9f4` | Pozadí stránky |
| `--birch` | `#f1ede3` | Alternativní plochy, pruh faktů |
| `--ink` | `#1d2623` | Text |
| `--muted` | `#55625a` | Sekundární text |
| `--copper` / `--copper-dark` | `#a5552a` / `#8a4521` | Tlačítka „Rezervovat“, drobné akcenty (kontrast s bílým textem ≥ 4,5:1) |
| `--sand`, `--line` | `#d9c7a6`, `#ddd5c4` | Placeholdery, linky |

- Hero: velká fotka přes celou šířku, tmavý přechod jen pro čitelnost textu, jedna primární a jedna sekundární akce.
- Nadpisy serif, text bez patek. Zaoblení minimální (3–4 px), žádné stíny u každého bloku.
- Pohyb jen dvakrát: jemné odkrytí sekcí při scrollu a posun šipky na tlačítku. Vše vypnuté při `prefers-reduced-motion`.
- Bez emoji a ikon v kolečkách, žádné stock obrázky ani AI generované fotky apartmánu.
- Logo je zatím textové + znak hory (inline SVG). Majitelé mohou dodat vlastní, výměna = přepsání `LOGO_MARK` v `build.py` a `favicon.svg`.

---

## 5. Obsah a jazyky

Struktura jedné stránky (kotvy): Hero → Fakta → **O apartmánu** (`#about`) → **Fotogalerie** (`#gallery`) → **Vybavení** (`#amenities`) → **Lokalita** (`#location`, vzdálenosti, příjezd, zima/léto) → **Rezervace** (`#booking`) → **Kontakt** (`#contact`, adresa, mapové odkazy).

- Texty všech jazyků jsou v `content.py` pod klíči `cs`, `pl`, `de`. Nový klíč vždy přidej do všech jazyků (build to hlídá).
- **Polštinu a němčinu před spuštěním projde rodilý mluvčí** (`TODO(majitel)`). Do té doby ber překlady jako pracovní. Při změnách CS ukaž, co je třeba upravit v PL a DE.
- Kontrola terminologie: česká místní jména beze změny (Kořenov, Harrachov, Jizerka); Jizerské hory = PL *Góry Izerskie*, DE *Isergebirge*.
- Údaje v PL/DE nesmí obsahovat nic, co není v CS (žádné „vylepšování“ faktů při překladu).
- Ceny a měny: web ceny neukazuje. Pokud o to majitelé požádají, ukládej ceny jako čísla a formátuj přes `Intl.NumberFormat` podle jazyka (CZK / PLN / EUR) a vždy uveď, odkud jsou a k jakému datu.
- Hlavní tlačítko, kontakt a patička se renderují jen z vyplněných údajů v `CONFIG` (prázdné se nezobrazí).

---

## 6. Rezervační systém

- **Jedna adresa** v `CONFIG["booking_url"]`, kterou používají všechna tlačítka (hlavička, hero, sticky lišta na mobilu, sekce Rezervace). Otevírá se v nové záložce (`rel="noopener"`).
- `TODO(majitel)`: **který systém to bude** (vlastní, Smoobu, Beds24, Previo, Booking/Airbnb apod.) a zda umí:
  - předvyplnit jazyk (pak v `build.py` doplň odkaz pro každý jazyk zvlášť: `booking_url` jako slovník `{cs, pl, de}`),
  - předvyplnit termín nebo UTM parametry (`utm_source=web`) pro měření.
- Dokud odkaz chybí, tlačítka míří na `#contact` a v sekci Rezervace je viditelná poznámka. Před spuštěním musí zmizet.

---

## 7. Fotky

- **Stav:** ve webu je 11 fotek z inzerátu na ceskehory.cz (originály ve `podklady/x1.jpg`–`x11.jpg`, 1024 px, **s vodoznakem ceskehory.cz**). Jsou zkopírované do `assets/img/` pod popisnými názvy a zapojené v `content.py` (`HERO_PHOTO`, `LOCATION_PHOTO`, `GALLERY`, včetně alt textů v CS/PL/DE a rozměrů):

  | Soubor | Z | Obsah |
  |---|---|---|
  | `hero-okoli.jpg` | x2 | dům a hory z ptačí perspektivy (hero) |
  | `okoli.jpg` | x3 | údolí s domem (sekce Lokalita) |
  | `dum.jpg` | x1 | dům s parkovištěm |
  | `obyvak.jpg` | x4 | obývací pokoj s pohovkou |
  | `kuchyn.jpg`, `kuchyn-roh.jpg` | x5, x7 | kuchyně, kuchyňský kout |
  | `jidelni-stul.jpg` | x6 | jídelní stůl u okna |
  | `predsin.jpg` | x8 | předsíň |
  | `postel-dvoulozko.jpg`, `postel-jednolozko.jpg` | x9, x10 | pokoje s lůžky |
  | `koupelna.jpg` | x11 | koupelna |

- **Až dorazí fotky bez vodoznaku:** přepiš soubory v `assets/img/` pod **stejnými názvy**, případně uprav `w`/`h` v `content.py`, nastav `PHOTOS_WATERMARKED = False` a přegeneruj. Dokud je vodoznak, web není na ostré spuštění.
- **Autorská práva:** fotky patří majitelům apartmánu. Fotky okolí od jiných uživatelů ceskehory.cz (kaple Tesařov) **nepoužívej** bez souhlasu autorů.
- Při výměně za originály udělej:
  1. zkontroluj výběr a pořadí galerie (galerie je mozaika bez ořezu, hero je ořezaný přes `object-position`),
  2. překontroluj alt texty podle toho, co je na nových fotkách,
  3. vyrob `srcset` verze (např. 640 / 1024 / 1600 px, WebP + JPEG, dostupný je ImageMagick `convert`), zachovej `width`/`height` kvůli CLS,
  4. hero obrázek preloaduj, ostatní `loading="lazy"` (už je).
- Pro sezónní atmosféru (zima/léto) navrhni, jaké fotky chybí (např. exteriér domu, výhled, vybavení kuchyně, okolí v zimě a v létě), a zapiš je do otevřených bodů.

---

## 8. SEO, GDPR, měření

- Každý jazyk: unikátní `<title>` a meta description (≤ 155 znaků), `lang`, JSON-LD `LodgingBusiness` (už v `build.py`).
- Po vyplnění `site_url`: canonical, `hreflang` (cs, pl, de, x-default), `sitemap.xml`, `robots.txt` bez `Disallow`. Přepni `CONFIG["indexing"]` na `True` **až při ostrém spuštění**.
- OG obrázek 1200×630 pro sdílení (z hlavní fotky, `TODO` až budou originály).
- Žádné cookies, žádné trackery, žádné iframy (mapy, YouTube) bez souhlasu. Mapa jsou jen odkazy na Mapy.cz a Google Maps.
- Měření návštěvnosti: zatím žádné. Pokud majitelé budou chtít, navrhni nástroj bez cookies (Plausible / Umami) a připrav místo v `build.py`.
- Právní údaje (provozovatel, IČO, případné zásady ochrany osobních údajů) jen z podkladů od majitelů, nic nevymýšlej (`TODO(majitel)`).

---

## 9. Kvalita, přístupnost, výkon

- Lighthouse (mobil): Performance ≥ 95, Accessibility 100, Best Practices 100, SEO 100.
- WCAG 2.2 AA: jeden H1 na stránku, skip-link (už je), viditelný focus (už je), kontrast textu min. 4,5:1, alt texty, ovládání menu a galerie klávesnicí (Esc, šipky), `aria-expanded` u menu.
- Funkční od 320 px bez vodorovného scrollu (teď ověřeno na 390 px, ověř i 320 px).
- Bez layout shiftu (rozměry obrázků).
- Váha úvodu do ~1 MB bez lazy obrázků.
- Playwright test: pro každý ze 3 jazyků načtení bez chyb v konzoli, funkční menu, lightbox, přepínač jazyků, žádný vodorovný scroll na 390 px.

---

## 10. Postup po fázích

| Fáze | Obsah | Výstup ke schválení |
|---|---|---|
| **F0 – Příprava** | Přečíst kód verze 0.1, rozhodnout o git repozitáři, `CLAUDE.md` (příkazy, struktura, jak změnit text/foto), `npm`/Playwright pro screenshoty | Strom projektu, `python3 build.py` běží |
| **F1 – Fotky** | Výměna fotek za verze bez vodoznaku, optimalizace (`srcset`, WebP), kontrola alt textů a pořadí galerie | Screenshoty hero a galerie (390/768/1440) |
| **F2 – Obsah** | Ověřit fakta s majiteli, doplnit `CONFIG` (rezervační URL, kontakt, PSČ, provozovatel), doladit texty, případně FAQ (příjezd/odjezd, psi, parkování), jen z podkladů | Seznam `TODO(majitel)` a `NÁVRH`, screenshoty CS |
| **F3 – Jazyky a SEO** | Review PL a DE (rodilý mluvčí), hreflang, sitemap, OG obrázek, JSON-LD | Screenshoty PL a DE, výpis meta tagů |
| **F4 – QA a testovací nasazení** | Playwright, Lighthouse, kontrola odkazů a přístupnosti, nasazení na GitHub Pages s `noindex` | Report: skóre, výsledky testů, URL náhledu |
| **F5 – Ostré spuštění** | Doména, `site_url`, `indexing=True`, DNS a HTTPS (návod v `docs/SPRAVA.md`), kontrola indexace | Návod hotový, web na ostré doméně |

Na konci každé fáze napiš: 1. co je hotové, 2. screenshoty, 3. nové `TODO(majitel)` / `NÁVRH`, 4. rozhodnutí, která jsi udělal sám, a proč, 5. otázky na mě.

---

## 11. Otevřené body (k 15. 11. 2026)

- Odkaz a typ **rezervačního systému**: zatím neznámý, doplní se (jazykové verze odkazu?).
- **Kontakt** (telefon, e-mail, případně WhatsApp), **PSČ**, provozovatel/IČO.
- **Skutečná dispozice** (fotky vs. „1+1“, viz kapitola 3). Počet hostů je potvrzený: 4.
- Aktuálnost údajů z inzerátu (vybavení, vzdálenosti, psi).
- **Fotky bez vodoznaku** od majitelů (teď jsou z inzerátu s vodoznakem ceskehory.cz).
- Rodilý mluvčí pro **PL a DE**.
- **Angličtina**: doplní se později (viz kapitola 2).
- Zda majitelé chtějí **ceník, FAQ, recenze** (jen skutečné, se souhlasem hostů).
- **Doména zatím neexistuje**: testovací provoz na GitHub Pages s `noindex`, doména a `site_url` až před ostrým spuštěním.

---

## 12. Co nedělat

- Žádné vymyšlené ceny, recenze, ocenění, parametry ani akce.
- Žádné stock ani AI generované fotky apartmánu, žádné cizí fotky bez souhlasu autora.
- Žádné Google Fonts CDN, trackery, cookie lišty bez důvodu, iframy.
- Žádný carousel v hero, žádné automatické přehrávání.
- Neměň obsah `podklady/` (originály fotek z inzerátu, záloha původního zadání a skript `stahnout-fotky.ps1`, který už není potřeba).
- Nepřidávej framework ani build řetězec bez mého souhlasu.
