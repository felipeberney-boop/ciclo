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

GitHub Pages publishes `app/` with no build command (`.github/workflows/publicar_app.yml`); it is the official URL (the QR points there). Since 03/11 Netlify (`ciclo-udesa.netlify.app`, `netlify.toml`) publishes the same `app/` folder as a second host, deployed by hand with `npx netlify-cli deploy --prod --dir app`. The only external dependency is Google Fonts.

## App architecture (`app/index.html`)

- **Data is embedded as JS constants** near the top of the script (`REC`, `KM`, `JE`, `LYST`, `SERIE`,
  `HIST`, `RDS`, `COL`, `KST`, `KPROTO`, `CALZ_PAS`, `CALZ_BUSQ`…), each written as a single-line `const NAME={...};`.
  `datasets_procesados/*.json` are exports of these constants, not inputs the app loads.
  `codigo/extraer_series_de_la_app.js` parses `const NAME=` up to the top-level `;`, so keep that form if
  you edit them.
- **Views** are sections `#v-<name>` (perfil = the gate, disenar, radar, detalle, etapas, recorridos, marcas, retornos,
  revision («Revisión», since 10/11 the merge of consulta and asistente), racional, mover («El brief», the Entrega 4 pirueta since 10/11, under Más), adivina (out of the nav since 10/11, direct link only); the old portada was removed on 26/10) toggled by `mostrar(v)`; nav links use `data-v`. Each view has a `pintar*()`
  renderer that builds SVG charts by hand (no chart library).
- **K-means runs in the browser** (`kRand`/`kInit`/`kLloyd`/`kFit`/`kName`): 17 attributes (no footwear), 4
  standardized features (runway level/momentum, search level/momentum through 2024). k=4 starts from the stored `KM.cent` centroids so
  results are deterministic; other k use seeded random restarts. Clusters get stage names by nearest
  `KPROTO` prototype. New trends are **assigned to the nearest centroid, never retrained into the model**
  (a bug fixed earlier: retraining made each new trend its own cluster and renamed the rest).
- **«Revisión» (`#v-revision`, since 10/11; it merged «Buscar por imagen» `#consulta` and «Preguntar» `#asistente`, whose links still open it via `mostrar()`)**: one composer for an image, a question or both. CLIP reads the image into editable chips (`as.clip`, `rvLeerVector()`, `RV_CLIP` maps the 17 CLIP names to REC ids and KM names; since 10/11 it also reads the dominant color from `app/clip/colores.json`, shown only above 0.6 and as interpreted, never with a signal); `rvPintarLectura()` shows each chip's `señal()`, its `cicloDe()` sentence, the curves (`rvCurvas()`) and a rule-based devolución (`rvDevolucion()`, labelled as rules). The written devolución is the class V2 pattern: the user pastes a Groq key (localStorage `groq_key`)
  and the browser calls Groq directly with `app/llm/ciclo_datos.md` as DATOS (only the parts the question names).
  That file is generated: run `node codigo/armar_datos_llm.js` after changing any data constant.
- **Borrowed data:** taxonomy leaves without their own series carry `presta_de`/`presta_porque` (sibling → parent → loose
  attribute, never another family); the UI always says where a borrowed number comes from.
- **Diseñar** runs on `TAX` (from `codigo/taxonomia.py`; rerun it after touching drawings or tables). Every state color
  comes from `señal()` / `señalPalabra()` and the `s-<estado>` CSS classes; never assign a state color by hand.
  The app always opens on the 3-question gate (each card shows only its label; what each answer changes lives in Método, `pintarMetodoGate()`); only a link with `c`, `v` and `pu` skips it (a 04/11 link with `d` instead of `v` still works: `d=disenar` maps to `v=propia`). The questions are: público, vínculo (para una marca / por mi cuenta: «por mi cuenta» turns Esperar into Explorar) and category. A gate by objective («¿Qué estás por decidir?») was tried and dropped on 04/11; don't bring it back. The app shows nothing about the course (no subject, school, teachers or delivery numbers): that lives in the readme and the racional. After it, the app lands on Tendencias (`radar`), the
  main screen; the CICLO mark goes to Tendencias and «Cambiar perfil» reopens the gate (`abrirGate(vista)`). Nav order:
  Tendencias · Diseñar · El ciclo · Revisión · Más. Since 10/11 «Más» holds only El brief and Método (Adiviná vos left it; it still opens at `#adivina`), and Retornos opens from El ciclo via `data-vista="<vista>"` links; since 10/11 El modelo (`etapas`) and Marcas are out of the navigation (they still open by direct link, `#etapas`/`#marcas`). Método opens with «Cómo se arma una lectura» (`pintarLectura()`), which replaced the static data schema. «El brief» (view `mover`, `pintarBrief()`, `BF_BRIEFS`, `BF_PTS`): a brief from a real house with a Vogue photo (hotlinked, never downloaded), three picks (shape, material, print), and a verdict: each pick's moment (sube/pico/quieto/baja) comes from its GREL search series 2022→2024; the per-house points are a game rule (luxury wins while rising, fast fashion at the peak), stated as such and separate from `CONSEJO`. Tendencias opens with a chart that rotates between five animated readings of the GREL series (`pintarTerreno()`, `TV_V`, `tvIr()`, 9 s each; no dark tile anymore). Every «?» (`details.qm`) sits top right of its block and opens as a floating card. The gate has a «Sólo estoy mirando» exit (`gateMirar()`, a general contemporary profile that Tendencias states); Revisión uses `prompts/prompt_asistente_v8.md` (conclusion → backing number → folded detail). Links between views use `data-vista` (not `data-ir`, which is the Diseñar step a chip returns to). `tendencia(d)` describes (▲/■/▼ in ink, El ciclo and Tendencias; the one exception since 27/10: «▲ Gana presencia» text is
  green and «▼ Pierde presencia» red, classes `t-entrar`/`t-salir`, bars and «Estable» stay ink) and is otherwise never a state color; `señal()` decides, and without a K-means stage it says Entrar/Esperar/Salir from the trend.
- Cards in Tendencias and El ciclo, and every option in El brief (`bfImg()`), show a Vogue Runway photo when `FOTO_ATR` has one (picked with CLIP text→look similarity and checked by eye, hotlinked via `vogueFoto()`, credited with `fotoCred()`); cuts keep their silhouette as a corner tag. Attributes without a photo keep their drawing.
- Tendencias lists only `T` attributes with measured data (`tieneDato()`: a K-means stage or a search series); the synthetic Zara 2018–22 catalog (palettes, estimated stage, its monthly chart) is no longer shown anywhere. Don't bring it back on screen.
- The "cliente" selector (fast / premium / nicho) changes recommendations (`CONSEJO`, `PLAZO`) and re-renders.

## Design rules that apply in code

- **Color means one thing: the signal** (`señal()`: entrar green, esperar amber, salir red, sin-dato neutral), always with
  its word and icon. Provenance is never a color: `● medido`, `◇ interpretado` (dashed), `↪ prestado` as text/icon/dashed
  line. The old salmon-for-AI rule is retired (tokens `--ia`/`--ia-t` are neutral now).
- **Stage is encoded as position on a track, not color.** Since 27/10 the look is an Apple-style product page
  (the system, never the brand; the reference came from the cátedra, Iván Fardjoume: Apple's DESIGN.md on shadcn.io, saved in `diseno/referencias/`): system font stack `--sf` (SF Pro on Apple devices, Inter from Google Fonts elsewhere),
  #f5f5f7 canvas, white 18px cards, pills, no uppercase-tracked labels, no UI shadows, one dark tile (`.terreno`),
  always light (`<html data-theme="light">` disables the old dark mode). Colors: the garments' palettes, the signal
  (Entrar green, Esperar/Explorar amber, Salir red via `accCls()`/`--act-*`, always with the word), and **one blue
  (`--azul`, #0066cc) that only means «clickable»** (action buttons, links, the chosen option). Charts keep `--s1`…`--s6`.
  CSS layers, later wins: original → editorial (20/10) → «capa de uso» (27/10) → «capa Apple» (27/10, last). The old
  no-radius rule is beaten with `:not(#z)`. The Entrega 3 presentation lives in `entregas/entrega_3/presentacion/` (moved out of `app/` on 04/11: the published site is the product only) and uses the same look.
- **Startup:** every `.view` starts `hidden`; only the boot code (wrapped in try/catch, plus a fallback
  `<script>`) decides what shows. A saved profile goes to Diseñar with the `#perfilinea` line, never silently.
- **No number without its source.** Each card states which data layer can and cannot answer.
- **The LLM never sees a data row**, only precomputed metrics (level, momentum, growth, distance to peak)
  plus client type; its output is shown labelled as interpretation. Prompts live in `prompts/` and are
  versioned: add `_v2.md` etc., never overwrite an existing version. No API keys in the repo; IA-5 («Pedir lectura en vivo»,
  `lvPedir()`) and «Revisión» (`prompts/prompt_asistente_v8.md`) both call Groq from the browser with the user's own key (localStorage `groq_key`).
  `netlify/functions/` was deleted on 04/11 (the app needs no server; it is in git history).

## Scripts (`codigo/`)

Offline helpers, not part of the site. Most use hard-coded relative paths from their original working
directory that don't match the repo layout, so adjust before running (`taxonomia.py`, `armar_datos_llm.js` and
`capturar_pantallas_de_la_app.js` run as-is from the repo root):

- `extraer_series_de_la_app.js` reads `app_recuperada.html` → writes `datos_app.json`
- `calcular_geometria_de_graficos.js` reads `./datos_app.json` → writes `geom.json`
- `generar_laminas_entrega_2.py` → 20 slide SVGs (1920×1080) into `entrega2_svg/`
- `renderizar_laminas_a_png.js` reads `entrega2_svg/` → PNG (Playwright)
- `capturar_pantallas_de_la_app.js` (run from the repo root, app served) → the 19 screenshots (01–17, 19 and 20, El brief) in
  `entregas/entrega_4/capturas/` used by the readme (the 03/11 set stays in `entregas/entrega_3/capturas/`). It never shows an LLM answer (no simulated responses)
- `capturar_recorrido.js` (same way) → the step-by-step walkthrough in `entregas/entrega_4/recorrido/` that the readme shows
- `exportar_racional_pdf.js` (from the repo root) → `entregas/entrega_4/racional.pdf` from `racional.md`; rerun it after editing the racional. Needs `marked` besides Playwright

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
