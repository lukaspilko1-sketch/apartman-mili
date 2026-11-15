# Apartmán Mili – pokyny pro Claude Code

Statický třijazyčný web (CS/PL/DE) apartmánu v Kořenově. Zadání a fáze: `SUPERPROMPT.md` (platí vždy, čti ho první). Komunikace česky, stručně, vykání v textech webu.

## Příkazy
```bash
python build.py            # přegeneruje index.html, pl/, de/, robots.txt (na Windows `python`, ne `python3`)
npm run screenshots        # screenshoty 390/768/1440 px × cs/pl/de do screenshots/
```
Po `npm install` + `npx playwright install chromium` (jednorázově). Žádný dev server, stačí otevřít HTML ze souboru.

## Struktura
- `content.py` – **jediný zdroj** textů (`T["cs"|"pl"|"de"]`), konfigurace (`CONFIG`), fotek (`HERO_PHOTO`, `LOCATION_PHOTO`, `GALLERY`)
- `build.py` – generátor HTML (šablona v `render()`), hlídá úplnost překladů (`check_languages`)
- `assets/css/style.css` – tokeny v `:root`, styly po sekcích; `assets/js/main.js` – menu, lightbox, reveal
- `assets/img/` – fotky; `podklady/` – originály a zálohy, **needitovat**
- `index.html`, `pl/index.html`, `de/index.html`, `robots.txt` – **generované**, neupravovat ručně
- `tools/screenshots.mjs` – Playwright screenshoty

## Jak změnit
- **Text:** upravit v `content.py` ve všech jazycích (nový klíč do všech, jinak build selže), pak `python build.py`. Změna CS = ukázat, co upravit v PL/DE.
- **Foto:** přepsat soubor v `assets/img/` pod stejným názvem, případně `w`/`h` v `content.py`; alt texty v CS/PL/DE.
- **Kontakt, rezervační URL, PSČ, provozovatel:** `CONFIG` v `content.py`. Prázdné se nezobrazí.
- **Angličtina později:** `T["en"]` se stejnými klíči + `"en"` do `ENABLED_LANGS`.

## Pravidla
- Nic si nevymýšlet (ceny, kontakty, vybavení). Chybějící údaje = `TODO(majitel)`, vymyšlené věty = komentář `NÁVRH: ke schválení`.
- Bez frameworku, bez Google Fonts CDN, bez trackerů/cookies/iframů, bez nového build řetězce bez souhlasu.
- Git: commity malé, česky (`feat:`, `fix:`, `content:`, `style:`). Repo je nadřazená složka `Weby`; `apartman-mili/` je zatím untracked. Nic necommitovat/neměnit bez pokynu.
- Na konci každé fáze: hotovo, screenshoty, nové TODO/NÁVRH, vlastní rozhodnutí, otázky; pak počkat na schválení.
