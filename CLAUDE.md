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

GitHub Pages publishes `app/` with no build command (`.github/workflows/publicar_app.yml`); it is the official URL (the QR points there). Since 03/11 Netlify (`ciclo-udesa.netlify.app`, `netlify.toml`) publishes the same `app/` folder as a second host, deployed by hand: since 16/11 `deploy --prod` answers «Forbidden», so make a draft (`npx netlify-cli deploy --dir app`) and publish it with `npx netlify-cli api restoreSiteDeploy --data '{"site_id":"ccf2ee73-2400-4eb4-8d2f-b8f2ea43a5e8","deploy_id":"<draft id>"}'`. The only external dependency is Google Fonts.

## App architecture (`app/index.html`)

- **Data is embedded as JS constants** near the top of the script (`REC`, `KM`, `JE`, `LYST`, `SERIE`,
  `HIST`, `RDS`, `COL`, `KST`, `KPROTO`, `CALZ_PAS`, `CALZ_BUSQ`…), each written as a single-line `const NAME={...};`.
  `datasets_procesados/*.json` are exports of these constants, not inputs the app loads.
  `codigo/extraer_series_de_la_app.js` parses `const NAME=` up to the top-level `;`, so keep that form if
  you edit them.
- **Views** are sections `#v-<name>` (since 24/11: inicio = the home, cuenta = Mi cuenta; perfil = the old three-step gate, no longer shown; disenar, radar = «Mis ciclos», detalle, etapas, recorridos, marcas, retornos,
  lectura («Preguntale a CICLO», «Preguntar» in the nav, renamed on 16/11 from «Lectura», which had replaced «Tiza» (10/11), the merge of consulta and asistente), racional, mover («El brief», the Entrega 4 pirueta since 10/11, under Más), adivina (out of the nav since 10/11, direct link only); the old portada was removed on 26/10) toggled by `mostrar(v)`; nav links use `data-v`. Each view has a `pintar*()`
  renderer that builds SVG charts by hand (no chart library).
- **Home, projects and account (since 24/11, rediseño B+C; see `entregas/entrega_4/plan_rediseno.md`).** The app opens on
  `#v-inicio` (`pintarInicio()`; second version, 24/11, «una foto por idea», chosen by Felipe between two directions in
  `diseno/rediseno_2026-11-24/home2/`, logic from loopsii.com): left, one sticky runway photo that changes with the idea in
  the middle of the screen (`.hfoto`, IntersectionObserver); right, one idea per screen that appears on scroll (`.hrev`):
  qué es · cómo funciona · de dónde salen los datos (with country and period) · qué obtenés · «Crear tu proyecto» (`#crear`).
  Since vuelta K (24/11) the first screen only defines (etiqueta «Una herramienta de moda para diseñadores y marcas», H1
  «Cuándo usar una tendencia, y cuándo dejarla.», a bajada) and ends with «Bajá para ver cómo funciona ↓» (`.hbaja`,
  animated arrow, scrolls to `#in-que`); the create buttons live only at the end. The footer's source columns show only
  on the home (`body.on-inicio`); elsewhere the colofón is one line.
  No carousel and no credits over photos (credits in `.hcred`). On phones each idea carries its own photo (`.hmfoto`).
  `pintarForm()` is a clean block (`.pyform.limpio`): project name, email, three segmented options each with one line, one
  button; initials come from the email (or from the name set in Mi perfil). No server: everything is
  in localStorage (`ciclo.usuario`, `ciclo.proyectos`, `ciclo.activo`), stated next to the email field and in Acerca de.
  `abrirGate(destino)` no longer opens the gate: it scrolls to «Crear tu proyecto» and remembers where you were going
  (`pyDestino`). «Sólo estoy mirando» (`gateMirar()`, `[data-mirar]`) goes to Explorar ciclos without a project
  (`pyMirar()`: contemporary example profile, said on screen). Boot: a link with `c`, `v`, `pu` opens its view; else an
  active project opens Mis ciclos; else the home. Menu: CICLO · Mis ciclos (`radar`) · Diseñar · Explorar ciclos
  (`recorridos`) · Preguntar · El brief · Acerca de; «Más» and «Cambiar perfil» are gone. `#cuenta` (outside `#nav`, so
  it shows on phones too) holds the avatar with initials (`iniciales()`: Felipe Berney → FB, one name → one letter, else
  from the email) or «Crear proyecto»; the avatar opens Mis proyectos · Mi perfil · Salir / cambiar de proyecto. Mi cuenta
  (`pintarCuentaVista()`) edits the name/email and lists projects (open, edit, delete, new). Mis ciclos shows
  `PROYECTO <name> · Mujer · Para una marca · Fast fashion · Editar` (`pintarPerfilRadar()`).
- **Mis ciclos (`#v-radar`, since 24/11, rediseño D; vuelta K the same day).** The tool: the 65 `REC` attributes with a
  `GREL` series, not the old 8 `T` cards. Since vuelta K there is no bar and no selector: two titled sections, always
  visible, «Qué gana y qué pierde terreno» (`#mcgraf`, gana above pierde, full width, the «+50» line, a line saying Google
  has no gender or brand type, and under each chart the five names with their project signal, `.mcgit`) and «Mis
  tendencias» (`#mctend`, groups are H3). Search and category moved to Explorar; `mcLista()` always returns the 65.
  Since vuelta L (24/11, later) the chart block is short: one sentence, the «+50» line, a small line (`.mcfiltro`) saying the
  chart is worldwide Google and the same for every project (only the signal changes), charts 165 px high and side by side
  from 1000 px (`.mcdos`); no paragraph above the cards. Explorar hides the footer (`body[data-vista=recorridos]`).
  `FOTO_ATR` covers 63 of 65 attributes (vuelta L added 15 with `codigo/buscar_fotos_clip.mjs`; neoprene and espiga have no
  good candidate and keep their drawing).
  The text below describes the earlier version where it mentions the bar or Tendencias | Gráfica. Tendencias (`mcTend()`): cards (`mcFicha()`) grouped ▲ Entrar → ■ Esperar/Explorar →
  ▼ Salir by `señal()`, each with K-means stage, search 2022→2024 and Reddit **of the project's público only**
  (`mcReddit()`: `RDS` women, `RDH` men; «baggy jeans + mom jeans» falls back to «baggy jeans» in women and says so).
  Gráfica (`mcGrafica()`): one chart at a time with a one-sentence computed conclusion: «Gana y pierde terreno» (top 5
  each way, stacked, `moviPanel(…,ejes=true)` draws a fixed 0–100 axis; the unit line says 100 = the term's max year
  2004–2024) and «Cuándo picó cada uno» (`mcLineaTiempo()`, a year axis top and bottom, every dot carries `data-src`).
  «Qué está en su máximo», «Lo que vuelve» and «Uno contra otro» are gone, and so is the rotation and the photo band
  (`vistaBanda()` returns). What the project really filters: brand type and vínculo change the signal; público changes
  only Reddit; Google and Vogue have no gender, and the screen says so. A link profile that differs from the active
  project is shown as «Perfil de un link» with «Volver a <proyecto>».
- **Mis ciclos and Explorar show different things (since 24/11).** A card in Mis ciclos (and `abrirDetalle()` for any
  attribute with a series) opens `abrirFichaProyecto(id)` in `#v-detalle`: the project line, its signal, stage, search
  2022→2024, Reddit of the project's público only and «tu ventana», plus the layer chart drawn with
  `recContexto='proyecto'` (`recSeries()` drops the other forum; `recChart()` draws the window). Shareable as
  `#ficha/<id>?c=…&v=…&pu=…` (`fichaId`). Explorar (`pintarRecorridos()`, `recContexto='explorar'`) shows everything for
  everyone: both forums, no signal, no window (`pintarExplorarDatos()` replaces `pintarDecision()` there), and a link back
  to the attribute «para <proyecto>». Both show `comoSeLee(o)` under the chart, always visible: the stage comes from a
  K-means and does not predict, the dotted line is the cone (not a forecast), and 100 is the attribute's own max per source. `FUENTE_INFO` says where each source is from: Google Trends and Shopping worldwide
  with English terms (14 Argentine terms in Spanish), Reddit English-language forums with no country, Vogue Runway shows
  in Paris, Milan, New York, London and other weeks, Amazon = amazon.com, H&M dataset states no country.
- **Explorar ciclos (`#v-recorridos`, since 24/11, rediseño E; vuelta K)** is the informative screen, without the project:
  title «Explorar ciclos» and one line; a bar (`.mcbarra.exbarra`, not sticky: search `#exq` / `exQ`, count `#excuenta`,
  category chips `#exchips`); the photo cards (`pintarCiclos()`, sorted by most recent peak, never by signal); and «El
  recorrido de <atributo>» with a select of the 65 (`#rsel`, grouped by `REC_ORDEN`; cards also change it). The jeans-by-cut
  charts, the lag chart, the animated timeline and the hidden `exsale` blocks were deleted with their renderers
  (`lagChart`, `jeansShare`, `jeansSub`, `pintarJeans`, `cicloTL`); `JE` stays (Diseñar and Acerca de use it).
- **K-means runs in the browser** (`kRand`/`kInit`/`kLloyd`/`kFit`/`kName`): 17 attributes (no footwear), 4
  standardized features (runway level/momentum, search level/momentum through 2024). k=4 starts from the stored `KM.cent` centroids so
  results are deterministic; other k use seeded random restarts. Clusters get stage names by nearest
  `KPROTO` prototype. New trends are **assigned to the nearest centroid, never retrained into the model**
  (a bug fixed earlier: retraining made each new trend its own cluster and renamed the rest).
- **«Preguntale a CICLO» (`#v-lectura`, «Preguntar» in the nav; named «Lectura» for a few hours on 16/11, then renamed because it did not say it is a chat; `#preguntar` opens it too; it replaced «Tiza» (10/11), which merged «Buscar por imagen» `#consulta` and «Preguntar» `#asistente`; `#tiza`, `#consulta`, `#asistente` and `#revision` open it via `mostrar()`)**: one thread, 760 px wide, the composer sticky at the bottom; no side panel. The script in `entregas/entrega_4/guion_seccion_lectura.md` was approved before coding. `as.hist` holds the thread; `asPintar()` renders it (`ltBurbuja()`, `ltYo()`, `ltVacio()`). An image dropped anywhere except the gate (`tzArrastre()`) becomes your message; the reply bubble (`tipo:'lectura'`) holds what CLIP read as editable chips with their `señal()` (`ltChips()`, `ltCorregir()` redoes the same bubble), the one curve that matters (`ltCurva()`), similar looks (`ltLooks()`) and the devolución (LLM with a key, `rvDevolucion()` rules without). A question (`tipo:'resp'`) carries its data piece inside (`ltPieza()`: Lyst per tramo via `tzLyst()`, Zara, or `tzFotos()` + `rvCurvas()`), between conclusion and detail. Suggested questions are fixed (`TZ_SUG`) plus three example looks (`LT_EJ`, `rvEjemplo()`). `RV_CLIP` maps the 17 CLIP names to REC ids and KM names; the dominant color comes from `app/clip/colores.json` (shown above 0.6, as interpreted, never with a signal). Groq calls go through `asLlamar()`: on 429 it waits what Groq asks, with a countdown in the bubble, and retries (each call is ~6,000 tokens; the free plan allows 8,000/min). The written answer is the class V2 pattern: the user pastes a Groq key (localStorage `groq_key`)
  and the browser calls Groq directly with `app/llm/ciclo_datos.md` as DATOS (only the parts the question names).
  That file is generated: run `node codigo/armar_datos_llm.js` after changing any data constant.
- **Runway series (`REC[].v`)** come from Vogue tags through 2021; since 18/11 the years 2022–2023 are read by a CLIP classifier (Vogue stopped tagging: 48 % of 2023 looks tagged, Fall 2023 none). `REC[].vclip` marks the first CLIP year (drawn dashed) and `vult` the last year. `KM.rows` pasarela features and `KM.sc`/`KM.cent` were recomputed from the corrected series (`codigo/pasarela_clip/`); `kName()` lets a group share its nearest stage when the forced one is >1.5× farther. Since 18/11 (later) the model also uses runway 2024–2025 (level 2024–25, momentum 2023–25 vs 2020–22; lunares and piel keep their 2023 windows); `KM.cent` is the best of 50 seeded restarts (`codigo/pasarela_clip/km_final_2025.js`).
- **Borrowed data:** taxonomy leaves without their own series carry `presta_de`/`presta_porque` (sibling → parent → loose
  attribute, never another family); the UI always says where a borrowed number comes from.
- **Diseñar** runs on `TAX` (from `codigo/taxonomia.py`; rerun it after touching drawings or tables). Every state color
  comes from `señal()` / `señalPalabra()` and the `s-<estado>` CSS classes; never assign a state color by hand.
  Until 24/11 the app opened on the 3-question gate (since 17/11 a full-screen band of Vogue Runway photos, `GATE_FOTOS` from `codigo/armar_fotos_entrada.js`, `gateBanda()`, that change with each answer; the question sits on top in the system font) (each card shows only its label; what each answer changes lives in Método, `pintarMetodoGate()`); only a link with `c`, `v` and `pu` skips it (a 04/11 link with `d` instead of `v` still works: `d=disenar` maps to `v=propia`). The questions are: público, vínculo (para una marca / por mi cuenta: «por mi cuenta» turns Esperar into Explorar) and category. A gate by objective («¿Qué estás por decidir?») was tried and dropped on 04/11; don't bring it back. The app shows nothing about the course (no subject, school, teachers or delivery numbers): that lives in the readme and the racional. After it, the app lands on Tendencias (`radar`), the
  main screen; the CICLO mark goes to Tendencias and «Cambiar perfil» reopens the gate (`abrirGate(vista)`). Nav order:
  Tendencias · Diseñar · El ciclo · Preguntar · Más. Since 10/11 «Más» holds only El brief and Método (Adiviná vos left it; it still opens at `#adivina`), and Retornos opens from El ciclo via `data-vista="<vista>"` links; since 10/11 El modelo (`etapas`) and Marcas are out of the navigation (they still open by direct link, `#etapas`/`#marcas`). Método (view `racional`; since 17/11 it is called «Acerca de» in the menu and its title is «Acerca de CICLO», like a site's About page; it holds the racional summarized; since 24/11, rediseño I, eight closed parts, each one line, opened with a «+» that turns into «−» (`.methead`, `aria-expanded`): cómo se arma una señal · los datos · de dónde es cada dato (country, period, refresh) · el modelo · la hipótesis · las decisiones de diseño · tus datos y tu proyecto (localStorage) · el racional completo; the rotating photo wall `acercaPared()` is no longer called and the big diagrams only show when their part is open) opens with «Cómo se arma una señal» (`pintarLectura()`; it was «…una lectura» until 16/11), which replaced the static data schema. «El brief» (view `mover`, `pintarBrief()`, `BF_BRIEFS`, `BF_PTS`): a brief from a real house with a Vogue photo (hotlinked, never downloaded), for the season «<Otoño|Primavera> 2024» (since vuelta K the last year with search data, not the decision horizon `PERFIL.hasta`; the brief header is casa 600 · temporada as Etiqueta · prenda as gray subtitle, `.bfenc`), three picks (shape, material, print; no strip of picks so far, only «Volver»), and a verdict, everything centered (layer «El brief, centrado»): each pick's moment (sube/pico/quieto/baja) comes from its GREL search series 2022→2024; the per-house points are a game rule (luxury wins while rising, fast fashion at the peak), stated as such and separate from `CONSEJO`. Tendencias opens with a chart that rotates between five animated readings of the GREL series (`pintarTerreno()`, `TV_V`, `tvIr()`, 9 s each; no dark tile anymore). Every «?» (`details.qm`) sits top right of its block and opens as a floating card. The gate has a «Sólo estoy mirando» exit (`gateMirar()`, a general contemporary profile that Tendencias states); Tiza uses `prompts/prompt_asistente_v9.md` (conclusion → backing number → folded detail). Links between views use `data-vista` (not `data-ir`, which is the Diseñar step a chip returns to). `tendencia(d)` describes (▲/■/▼ in ink, El ciclo and Tendencias; the one exception since 27/10: «▲ Gana presencia» text is
  green and «▼ Pierde presencia» red, classes `t-entrar`/`t-salir`, bars and «Estable» stay ink) and is otherwise never a state color; `señal()` decides, and without a K-means stage it says Entrar/Esperar/Salir from the trend.
- Cards in Tendencias and El ciclo, and every option in El brief (`bfImg()`), show a Vogue Runway photo when `FOTO_ATR` has one (picked with CLIP text→look similarity and checked by eye, hotlinked via `vogueFoto()`, credited with `fotoCred()`); cuts keep their silhouette as a corner tag. Attributes without a photo keep their drawing.
- Tendencias lists only `T` attributes with measured data (`tieneDato()`: a K-means stage or a search series); the synthetic Zara 2018–22 catalog (palettes, estimated stage, its monthly chart) is no longer shown anywhere. Don't bring it back on screen.
- The "cliente" selector (fast / premium / nicho) changes recommendations (`CONSEJO`, `PLAZO`) and re-renders.

## Design rules that apply in code

- **Color means one thing: the signal** (`señal()`: entrar green, esperar amber, salir red, sin-dato neutral), always with
  its word and icon. Provenance is never a color: `● medido`, `◇ interpretado` (dashed), `↪ prestado` as text/icon/dashed
  line. The old salmon-for-AI rule is retired (tokens `--ia`/`--ia-t` are neutral now).
- **Stage is encoded as position on a track, not color.** Since 27/10 the look is an Apple-style product page
  (the system, never the brand; since 17/11 the canvas is white and the references are i-D and Vogue Runway; the earlier reference came from the cátedra, Iván Fardjoume: Apple's DESIGN.md on shadcn.io, saved in `diseno/referencias/`): system font stack `--sf` (SF Pro on Apple devices, Inter from Google Fonts elsewhere),
  #f5f5f7 canvas, white 18px cards, pills, uppercase-tracked text only for the Etiqueta style (since 24/11), no UI shadows, one dark tile (`.terreno`),
  always light (`<html data-theme="light">` disables the old dark mode). Colors: the garments' palettes, the signal
  (Entrar green, Esperar/Explorar amber, Salir red via `accCls()`/`--act-*`, always with the word), and **one blue
  (`--azul`, #0066cc) that only means «clickable»** (action buttons, links, the chosen option). Charts keep `--s1`…`--s6`.
  CSS layers, later wins: original → editorial (20/10) → «capa de uso» (27/10) → «capa Apple» (27/10) → «la letra de la moda» (17/11, last: `--moda` on titles, step questions, gate options, card names, deciding numbers, the logo with a five-dot ring; body text, buttons, labels and small chart numbers stay in `--sf`), then «los cinco estilos», «fina y derecha» and «la vibe de la entrada» (17/11, last: white background, titles left-aligned, a full-bleed moving row of Vogue Runway looks under the title of the main views via `vistaBanda()`, Tendencias cards as edge-to-edge photos without boxes), (17/11, last: Título 64/40, Subtítulo 24, Dato 34; Cuerpo 17 and Etiqueta 13 in `--sf` 400; no italics anywhere). **Since 24/11 the last layer is «el sistema»** (see «The system» below): Bodoni Moda only on the logo, everything else in `--sf`. A 032c-style layer (white, hard edges, the Tendencias chart repeated on every screen) was tried and reverted on 17/11: Felipe wants rounded pills and identity through type, not repetition. The old
  no-radius rule is beaten with `:not(#z)`. The Entrega 3 presentation lives in `entregas/entrega_3/presentacion/` (moved out of `app/` on 04/11). Since 16/11 `app/presentacion/` holds the short Entrega 4 making of (seven slides: data, system prompt, original prototype, «Muy IA», cómo quedó, El brief (the pirueta, from «Cómo se arma una lectura» and the discarded card game to the brief), links), a support page for the live demo, same look. Every slide except data and links is a turn: before · what happened · after, side by side (`giro:{pares,paso}`); the «before» shots come from `diseno/prototipos/versiones_de_la_app/`. Quotes are verbatim (spelling fixed, words and tone kept) and the ones by Felipe are craft corrections the model lacked.
- **The system (24/11, after the Entrega 4 devolución; sheet in `diseno/sistema_2026-11-24/`).** Last CSS layer «el sistema»,
  tokens in `:root`. Type scale, each style with one use: **H1** 56/36 600 −.025em (the screen's name) · **H2** 32/26 600
  (each block, the brief's verdict line) · **H3** 22/20 500 (what you touch: a card, an attribute, a step's question;
  `--t-sub`, `--h3-w`) · **H4** 18 600 (a chart's or group's title) · **Párrafo** 17 400 (secondary 16, gray;
  `--t-eti`/`--t-chico` are 16 now) · **Etiqueta** 12 600 UPPERCASE +.08em (`--t-lab`: `.lbl`, `.pkind`, `.dgk`, `.tde`…)
  · **Dato** 40/34 600 tabular. Photo credits 12 in normal case. Nothing that is read goes below 16 px; labels, credits
  and chart text never below 12 (`etiquetasSvg()` renders every SVG text at 13 screen px whatever the scale; don't put
  `!important` font sizes on SVG text, it breaks that). No weight above 600, no italics. Logo: Bodoni Moda 500, .14em,
  with the five-dot ring (Google Fonts loads Bodoni Moda only at 500, plus Archivo and Inter).
  **Palette by role:** *acción* `--accion` #0066cc, only what can be touched: a link is blue and underlined (`.lnk`,
  bare `a`, `.copiar`), a primary button is filled blue (`.kbtn`, `.mvacceso`, `.btn-pri`), a secondary one is a blue
  outline pill (`.gvolver`, `.cmplay`, `.ltejb`, `.btn-sec`), options/filters are ink pills (chosen = filled ink);
  over a photo a link is white and underlined. *info*: ink #1d1d1f, gray #6e6e73, lines #d2d2d7, blocks #f5f5f7, and
  the chart series `--s1`…`--s6` (they only tell curves apart). *señal*: entrar/esperar/salir green/amber/red, always
  with word and icon, nothing else. *foto*: Vogue Runway full-bleed, credit in white. *ilustración*: technical drawings
  in black line on white, never in a signal color. Never force `display` on buttons in this layer (it unhid the gate's
  «Volver»).
- **Startup:** every `.view` starts `hidden`; only the boot code (wrapped in try/catch, plus a fallback
  `<script>`) decides what shows. A saved profile goes to Diseñar with the `#perfilinea` line, never silently.
- **No number without its source.** Each card states which data layer can and cannot answer. Since 17/11 every measured number also carries `data-src="key|observations"` (keys in `FUENTES`, helper `src(k,n)`): hovering, or tapping on a phone, shows source, period and observations in `#tip`. Add it to any new measured number.
- **The LLM never sees a data row**, only precomputed metrics (level, momentum, growth, distance to peak)
  plus client type; its output is shown labelled as interpretation. Prompts live in `prompts/` and are
  versioned: add `_v2.md` etc., never overwrite an existing version. No API keys in the repo; IA-5 («Pedir lectura en vivo»,
  `lvPedir()`) and «Preguntale a CICLO» (`prompts/prompt_asistente_v9.md`) both call Groq from the browser with the user's own key (localStorage `groq_key`).
  Since 24/11 «Preguntale a CICLO» also works without a pasted key: `netlify/functions/preguntar.mjs` (path
  `/api/preguntar`, declared in `netlify.toml`) forwards the same request to Groq with `GROQ_API_KEY`, a Netlify environment
  variable (never in the repo); it allows only the two gpt-oss models, caps tokens and only accepts the GitHub Pages,
  Netlify and localhost origins. The app probes it with GET (`asServidor()`, `asServ`); `ltClave()` is true with a pasted
  key or a server key. A pasted key still goes straight to Groq. Deploy the draft with `--functions netlify/functions`.
  The empty thread shows two example conversations computed live by the rules (`ltEjemplos()`), labelled as such.

## Scripts (`codigo/`)

Offline helpers, not part of the site. Most use hard-coded relative paths from their original working
directory that don't match the repo layout, so adjust before running (`taxonomia.py`, `armar_datos_llm.js` and
`capturar_pantallas_de_la_app.js` run as-is from the repo root):

- `extraer_series_de_la_app.js` reads `app_recuperada.html` → writes `datos_app.json`
- `calcular_geometria_de_graficos.js` reads `./datos_app.json` → writes `geom.json`
- `generar_laminas_entrega_2.py` → 20 slide SVGs (1920×1080) into `entrega2_svg/`
- `renderizar_laminas_a_png.js` reads `entrega2_svg/` → PNG (Playwright)
- `probar_demo.js` (repo root, app served): the class demo, 8 steps; since 24/11 step 1 taps «Bajá para ver cómo funciona» and creates a project at the end of the home
- `capturar_pantallas_de_la_app.js` (run from the repo root, app served) → the 19 screenshots (01–17, 19 and 20, El brief) in
  `entregas/entrega_4/capturas/` used by the readme (the 03/11 set stays in `entregas/entrega_3/capturas/`). It never shows an LLM answer (no simulated responses)
- `capturar_recorrido.js` (same way) → the step-by-step walkthrough in `entregas/entrega_4/recorrido/` that the readme shows (since 24/11: home → crear tu proyecto → Mis ciclos → ficha → Diseñar → Explorar → Preguntar → El brief, desktop and phone, plus the «por mi cuenta» branch; it deletes the old PNGs first)
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
