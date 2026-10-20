# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

CICLO is a university project (UdeSA, *Sistemas generativos e IA para Diseño* K534/K576, 2026) that places
fashion **attributes** (a color, print, cut or material, never "a trend" or a garment) in one of five
lifecycle stages: emergente, en ascenso, en pico, saturada, en retorno. Everything is written in
**Spanish (Rioplatense)**: UI copy, docs, commit history, file names. Keep it that way.

## Running

There is no build, no package.json and no tests. The whole site is one file, `app/index.html` (~170 KB,
inline CSS + one inline `<script>`).

```bash
cd app && python3 -m http.server 8000
```

Netlify publishes `app/` with no build command. The only external dependency is Google Fonts.

## App architecture (`app/index.html`)

- **Data is embedded as JS constants** near the top of the script (`REC`, `KM`, `JE`, `LYST`, `SERIE`,
  `HIST`, `RDS`, `RETS`, `COL`, `KST`, `KPROTO`…), each written as a single-line `const NAME={...};`.
  `datasets_procesados/*.json` are exports of these constants, not inputs the app loads.
  `codigo/extraer_series_de_la_app.js` parses `const NAME=` up to the top-level `;`, so keep that form if
  you edit them.
- **Views** are sections `#v-<name>` (portada, radar, detalle, etapas, recorridos, marcas, retornos,
  consulta, asistente, racional) toggled by `mostrar(v)`; nav links use `data-v`. Each view has a `pintar*()`
  renderer that builds SVG charts by hand (no chart library).
- **K-means runs in the browser** (`kRand`/`kInit`/`kLloyd`/`kFit`/`kName`): 17 attributes (no footwear), 4
  standardized features (runway level/momentum, search level/momentum through 2024). k=4 starts from the stored `KM.cent` centroids so
  results are deterministic; other k use seeded random restarts. Clusters get stage names by nearest
  `KPROTO` prototype. New trends are **assigned to the nearest centroid, never retrained into the model**
  (a bug fixed earlier: retraining made each new trend its own cluster and renamed the rest).
- **«Preguntar» (`#v-asistente`)** is the class V2 pattern: the user pastes a Groq key (localStorage `groq_key`)
  and the browser calls Groq directly with `app/llm/ciclo_datos.md` as DATOS (only the parts the question names).
  That file is generated: run `node codigo/armar_datos_llm.js` after changing any data constant.
- The "cliente" selector (fast / premium / nicho) changes recommendations (`CONSEJO`, `PLAZO`) and re-renders.

## Design rules that apply in code

- **Salmon (`#FFAFA3`) = AI.** Black is measured; salmon is calculated or interpreted by a model. Holds in
  the app and in the presentation slides.
- **Stage is encoded as position on a track, not color.** The UI is monochrome (black, cream #F6F0EB, white)
  so the only color is the garments' own palette. The one exception: the recommendation word (Entrar green,
  Esperar/Explorar amber, Salir red, via `accCls()` and the `--act-*` tokens), always with the word itself.
  Nothing else gets those colors. Charts keep their series colors (`--s1`…`--s6`); everything else is monochrome. The editorial style block at the end of the CSS overrides the older rules.
- **Startup:** every `.view` starts `hidden`; only the boot code (wrapped in try/catch, plus a fallback
  `<script>`) decides what shows. A saved profile goes to Diseñar with the `#perfilinea` line, never silently.
- **No number without its source.** Each card states which data layer can and cannot answer.
- **The LLM never sees a data row**, only precomputed metrics (level, momentum, growth, distance to peak)
  plus client type; its output is shown labelled as interpretation. Prompts live in `prompts/` and are
  versioned: add `_v2.md` etc., never overwrite an existing version. No API keys in the repo; Groq uses
  `GROQ_API_KEY` in Netlify (IA-5 currently runs on a fixed prompt, not live).

## Scripts (`codigo/`)

Offline helpers, not part of the site. They use hard-coded relative paths from their original working
directory that don't match the repo layout, so adjust before running:

- `extraer_series_de_la_app.js` reads `app_recuperada.html` → writes `datos_app.json`
- `calcular_geometria_de_graficos.js` reads `./datos_app.json` → writes `geom.json`
- `generar_laminas_entrega_2.py` → 20 slide SVGs (1920×1080) into `entrega2_svg/`
- `renderizar_laminas_a_png.js` reads `entrega2_svg/` → PNG (Playwright)
- `capturar_pantallas_de_la_app.js` opens `repo/index.html` → screenshots (Playwright)

Requires `npm install playwright` / `pip install pillow`.

## Documentation conventions

- `decisiones.md` is a dated log of what was tried and discarded and why. Add an entry for meaningful
  model, data or design decisions.
- `historial.md` records project versions (v0, v0.1…), each tied to a dated commit.
- Original datasets are **not** in the repo (too large or need an account). Sources, download dates and
  licenses go in `datasets/fuentes_y_descargas.md`, column meanings in `datasets/diccionario.md`.
- Known limitations (Google Trends drift detrended and 2026 excluded, Lyst formula break at Q1-26 so
  metrics are computed within each segment, synthetic Zara 2018–22/Mix datasets used only to demonstrate
  method, no footwear, menswear and womenswear mixed) are stated in the app's Método view and `readme.md`.
  Don't present results in ways that contradict them.
