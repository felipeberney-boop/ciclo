# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

CICLO is a university project (UdeSA, *Sistemas generativos e IA para Diseño* K534/K576, 2026) that places
fashion **attributes** (a color, print, cut or material, never "a trend" or a garment) in one of five
lifecycle stages: emergente, en ascenso, en pico, saturada, en retorno. Everything is written in
**Spanish (Rioplatense)**: UI copy, docs, commit history, file names. Keep it that way.

## Running

There is no build, no package.json and no tests. The whole site is one file, `app/index.html` (~720 KB,
inline CSS + one inline `<script>`).

```bash
cd app && python3 -m http.server 8000
```

GitHub Pages publishes `app/` with no build command (`.github/workflows/publicar_app.yml`). The only external dependency is Google Fonts.

## App architecture (`app/index.html`)

- **Data is embedded as JS constants** near the top of the script (`REC`, `KM`, `JE`, `LYST`, `SERIE`,
  `HIST`, `RDS`, `COL`, `KST`, `KPROTO`, `CALZ_PAS`, `CALZ_BUSQ`…), each written as a single-line `const NAME={...};`.
  `datasets_procesados/*.json` are exports of these constants, not inputs the app loads.
  `codigo/extraer_series_de_la_app.js` parses `const NAME=` up to the top-level `;`, so keep that form if
  you edit them.
- **Views** are sections `#v-<name>` (perfil = the gate, disenar, radar, detalle, etapas, recorridos, marcas, retornos,
  consulta, asistente, racional; the old portada was removed on 26/10) toggled by `mostrar(v)`; nav links use `data-v`. Each view has a `pintar*()`
  renderer that builds SVG charts by hand (no chart library).
- **K-means runs in the browser** (`kRand`/`kInit`/`kLloyd`/`kFit`/`kName`): 17 attributes (no footwear), 4
  standardized features (runway level/momentum, search level/momentum through 2024). k=4 starts from the stored `KM.cent` centroids so
  results are deterministic; other k use seeded random restarts. Clusters get stage names by nearest
  `KPROTO` prototype. New trends are **assigned to the nearest centroid, never retrained into the model**
  (a bug fixed earlier: retraining made each new trend its own cluster and renamed the rest).
- **«Preguntar» (`#v-asistente`)** is the class V2 pattern: the user pastes a Groq key (localStorage `groq_key`)
  and the browser calls Groq directly with `app/llm/ciclo_datos.md` as DATOS (only the parts the question names).
  That file is generated: run `node codigo/armar_datos_llm.js` after changing any data constant.
- **Borrowed data:** taxonomy leaves without their own series carry `presta_de`/`presta_porque` (sibling → parent → loose
  attribute, never another family); the UI always says where a borrowed number comes from.
- **Diseñar** runs on `TAX` (from `codigo/taxonomia.py`; rerun it after touching drawings or tables). Every state color
  comes from `señal()` / `señalPalabra()` and the `s-<estado>` CSS classes; never assign a state color by hand.
  The app always opens on the 3-question gate; only a link with `c`, `v` and `pu` skips it. After it, the app lands on Tendencias (`radar`), the
  main screen; the CICLO mark goes to Tendencias and «Cambiar perfil» reopens the gate (`abrirGate(vista)`). Nav order:
  Tendencias · Diseñar · El ciclo · Buscar por imagen · Preguntar · Más. `tendencia(d)` describes (▲/■/▼ in ink, El ciclo and Tendencias; the one exception since 27/10: «▲ Gana presencia» text is
  green, class `t-entrar`, bars stay ink) and is otherwise never a state color; `señal()` decides, and without a K-means stage it says Entrar/Esperar/Salir from the trend.
- The "cliente" selector (fast / premium / nicho) changes recommendations (`CONSEJO`, `PLAZO`) and re-renders.

## Design rules that apply in code

- **Color means one thing: the signal** (`señal()`: entrar green, esperar amber, salir red, sin-dato neutral), always with
  its word and icon. Provenance is never a color: `● medido`, `◇ interpretado` (dashed), `↪ prestado` as text/icon/dashed
  line. The old salmon-for-AI rule is retired (tokens `--ia`/`--ia-t` are neutral now).
- **Stage is encoded as position on a track, not color.** The UI is monochrome (black, cream #F6F0EB, white)
  so the only color is the garments' own palette. The one exception: the recommendation word (Entrar green,
  Esperar/Explorar amber, Salir red, via `accCls()` and the `--act-*` tokens), always with the word itself.
  Nothing else gets those colors. Charts keep their series colors (`--s1`…`--s6`); everything else is monochrome. The editorial style block near the end of the CSS overrides the older rules, and the «capa de uso» block (27/10) comes last: sticky one-line header, sans for anything you click, «Más» as a card panel, «Menú» sheet on mobile, rounded cards (it uses `:not(#z)` to beat the old no-radius rule).
- **Startup:** every `.view` starts `hidden`; only the boot code (wrapped in try/catch, plus a fallback
  `<script>`) decides what shows. A saved profile goes to Diseñar with the `#perfilinea` line, never silently.
- **No number without its source.** Each card states which data layer can and cannot answer.
- **The LLM never sees a data row**, only precomputed metrics (level, momentum, growth, distance to peak)
  plus client type; its output is shown labelled as interpretation. Prompts live in `prompts/` and are
  versioned: add `_v2.md` etc., never overwrite an existing version. No API keys in the repo; IA-5 («Pedir lectura en vivo»,
  `lvPedir()`) and «Preguntar» both call Groq from the browser with the user's own key (localStorage `groq_key`).
  Netlify (`netlify.toml`, `netlify/functions/`) is paused and unused; the live deploy is GitHub Pages.

## Scripts (`codigo/`)

Offline helpers, not part of the site. Most use hard-coded relative paths from their original working
directory that don't match the repo layout, so adjust before running (`taxonomia.py`, `armar_datos_llm.js` and
`capturar_pantallas_de_la_app.js` run as-is from the repo root):

- `extraer_series_de_la_app.js` reads `app_recuperada.html` → writes `datos_app.json`
- `calcular_geometria_de_graficos.js` reads `./datos_app.json` → writes `geom.json`
- `generar_laminas_entrega_2.py` → 20 slide SVGs (1920×1080) into `entrega2_svg/`
- `renderizar_laminas_a_png.js` reads `entrega2_svg/` → PNG (Playwright)
- `capturar_pantallas_de_la_app.js` (run from the repo root, app served) → the 16 screenshots in
  `entregas/entrega_3/capturas/` used by the readme. It never shows an LLM answer (no simulated responses)

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
