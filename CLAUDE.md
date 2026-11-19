# CLAUDE.md — Mob Variants

Add-on de Minecraft Bedrock que da skins aleatorias a los mobs vanilla.
Objetivo actual: **1.26.60**, y en el futuro ser compatible con *Actions & Stuff* (A&S).

**Estado (rama `skins-base`)**: base **solo de skins** (entidad vanilla + un render controller que solo
cambia la textura). Capas, variantes de modelo completo y animaciones propias están en la etiqueta
`legacy-v5` y vuelven **de uno en uno**, con el usuario y probadas en el juego (skill **mv-mob**).

Lee también:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): cómo funciona el sistema de variantes (léelo antes de tocar un mob).
- [docs/mobs/](docs/mobs/README.md): **una ficha por mob** (estado actual generado, notas, lo que había
  en `legacy-v5` y plan). Léela antes de tocar un mob.
- [docs/STATUS.md](docs/STATUS.md) y [docs/PLAN.md](docs/PLAN.md): estado general, plan y decisiones.
- [docs/TOOLS.md](docs/TOOLS.md): herramientas de `tools/` (validación, simulación, render, BDS, paquetes).

## Estructura

| Ruta | Qué es |
|---|---|
| `RP/` | Resource pack. **Debe funcionar solo** (las skins se sortean en el cliente). |
| `BP/` | Behavior pack opcional. Solo guarda la variante elegida en propiedades de entidad. Depende del RP. |
| `vanilla/` | Packs vanilla de referencia ([Mojang/bedrock-samples](https://github.com/Mojang/bedrock-samples), release estable). **Gitignored**; ver "Plantilla vanilla". |
| `tools/` | Herramientas Python (ver docs/TOOLS.md), el BP de pruebas para BDS (`tools/bds/`) y el cargador de escenas de Blockbench (`tools/bb/`). |
| `.claude/skills/` | Skills de Claude para este proyecto (ver "Skills"). |
| `docs/` | Documentación y `Probabilities.pdf` (fuera de los packs para que no se empaquete). |

El desarrollador trabaja en este repo; Minecraft lee `BP/` y `RP/` mediante **junctions** en
`%APPDATA%\Minecraft Bedrock\Users\Shared\games\com.mojang\development_{behavior,resource}_packs\`.
No hay que copiar nada: guardar y volver a entrar al mundo basta.

## Reglas del proyecto (decididas con el usuario; no las cambies sin preguntar)

1. **Modelo y animaciones vanilla.** Las entidades son las vanilla actuales y llevan solo sus
   animaciones vanilla. Nada de modelos re-rigueados (codos/rodillas partidos, párpados).
   Extras que pueden volver (de uno en uno, regla 7): **variantes de modelo completo** (pato, oca,
   capibara, caracol, ornitorrinco, gatos especiales, creeper esqueleto, zombi que se arrastra), dibujadas
   en lugar del cuerpo vanilla con los **huesos renombrados a los vanilla** (`geotool rebone`) para que
   las animaciones vanilla las muevan; únicas animaciones propias admitidas, porque son de una geometría
   propia: el **zombi que se arrastra** (`animation.mv.zombie_crawl.*`) y el **wither**.
2. **Lo nuevo va en capas.** Sombreros, flores, colmillos, etc. son geometrías aparte cuyos huesos
   **se llaman como los huesos vanilla** (`head`, `body`, `leg0`, …) con su mismo pivote y jerarquía
   de padres, para que sigan cualquier animación (vanilla o A&S). Las piezas propias van como hijos
   con prefijo `mv_`. Para esconder una pieza vanilla, `part_visibility` en el render controller.
3. **Skins solo en la variante vanilla por defecto y en adultos** (vaca templada, gato blanco, zorro
   rojo, rana templada…). Bebés y otras variantes vanilla se ven 100 % vanilla. Se controla con
   `v.mv_active` (ver ARCHITECTURE).
4. **Namespace `mv`** para todo lo propio: `geometry.mv.*`, `controller.render.mv.*`,
   `animation.mv.*`, propiedades `mv:*`, grupos/eventos de BP `mv:*`, claves de entidad `mv_*`.
   Nunca redefinas un ID vanilla: afecta a otros mobs (pasó con el guardián anciano y el zoglin).
5. **El BP se construye sobre el archivo vanilla actual**, añadiendo solo propiedades y nodos
   `set_property` a los eventos vanilla. Nunca copies un archivo vanilla antiguo.
6. **Retexturas puras** (sin entidad) cuando la skin encaja en el UV vanilla y no hay aleatoriedad:
   texturas en la ruta vanilla (stray, caballos, panda, slime, oveja).
7. **Base primero, extras de uno en uno.** Cada skin de la base pinta todas las piezas del modelo
   vanilla (`tools/inventory.py`, columna "Revisar"); si no, se arregla o queda fuera. Cada extra (capa,
   variante de modelo completo, mecánica del BP) entra en su propio commit, solo con el visto bueno del
   usuario y después de que lo pruebe en el juego. Procedimiento: skill **mv-mob**.

## Skills (úsalas en vez de redescubrir las herramientas)

- **mv-mob**: trabajar un mob de la base (revisar skins, recuperar un extra de `legacy-v5`). Una conversación
  o agente por mob: solo toca los archivos de su ficha.
- **mv-verify**: comprobar cualquier cambio (check, render, Content Log, BDS, CI).
- **mv-skin**: skins nuevas (`addskin.py`), cosméticos como capa y mobs nuevos.
- **mv-release**: commits, versiones, paquetes, releases y Minecraft nuevo.
- **mv-texture**: texturas: plantillas UV, migrar skins a otro modelo (`texuv.py retarget`), recolorear,
  `lint`, pintar en Blockbench.
- **mv-blockbench**: Blockbench por MCP: variantes con animaciones en movimiento, editar capas, texturas.
  No arranques Blockbench ni el MCP tú (está denegado en `.claude/settings.json`): pídeselo al usuario.

Están en `.claude/skills/`. Si al usarlas ves que falta algo, sobra algo o un paso ya no es cierto,
puedes **sugerir** al usuario el cambio en la skill (solo si de verdad hace falta; no es obligatorio).
Referencia completa de las herramientas: docs/TOOLS.md.

### Las herramientas son nuevas: pueden tener fallos

Casi todo `tools/` y las skills se escribieron en noviembre de 2026 y se han usado poco; al usarlas de
verdad ya aparecieron varios fallos (filtros que ocultaban avisos, nombres de huesos mal emparejados…).
- No te fíes a ciegas de un resultado raro: contrástalo con otra herramienta o con los datos
  (p. ej. una separación de `bbcheck --measure` con los avisos de pivote de `validate.py`).
- Si crees que una herramienta falla, **demuéstralo antes** (caso mínimo que lo reproduzca, o la causa
  exacta en el código) y entonces **propón** la corrección al usuario explicando la prueba. Si no estás
  seguro, dilo como sospecha, no como fallo.
- Las salidas deben dar la información necesaria y no más (cada línea son tokens en cada uso). Si al
  usarla ves que en algún caso sobra o falta información, propón la opción (`--verbose`, un filtro…)
  explicando qué ahorra o qué aporta.

### Imágenes en el resumen

Si generas imágenes (render.py, bbcheck.py, texuv.py…), enséñaselas al usuario en el resumen final
con enlaces markdown (`![descripción](tools/out/...png)`), las relevantes, para que vea lo que has hecho.

## Blockbench (MCP)

Hay un servidor MCP `blockbench` (86 herramientas: `new_project`, `add_cubes`, `paint_texture`,
`screenshot_views`, `check_model`, `export_model`, `execute_script`…) configurado en el scope local
de este proyecto (`~/.claude.json`), no en el repo. Código en `C:\Users\victo\Desktop\projects\blockbench-mcp`
(`node dist/index.js`).

- Requiere **Blockbench abierto** con el plugin del MCP instalado; el servidor habla con él por
  `http://127.0.0.1:8787` (`curl` a esa URL devuelve `{"ok":true,...}` si está vivo).
- Las herramientas solo aparecen al **iniciar una sesión nueva** de Claude Code tras añadir el MCP.
- Úsalo para crear/ajustar **capas cosméticas** (regla 2): huesos con nombre vanilla, mismo pivote y
  padre, piezas propias como hijas `mv_*`. Exporta como Bedrock entity (`geometry.mv.*`) y pasa luego
  por la skill **mv-verify**. No lo uses para modificar el modelo base vanilla (regla 1).
- Empieza con `get_guide` (topics `modeling`, `texturing`, `inspection`…) antes de construir.

## Flujo de trabajo

1. Antes de tocar un mob, lee su ficha `docs/mobs/<mob>.md`; al acabar, `python tools/inventory.py <mob>`
   y actualiza sus notas y su plan.
2. Después de cualquier cambio: skill **mv-verify** (`python -I tools/check.py <mob>` hasta
   `RESULT: OK` y `python tools/render.py <mob>`, mirando tú el PNG).
3. **Pruebas en el juego: las hace el usuario**, solo para lo que no cubren las herramientas
   (animaciones en movimiento, materiales). El Content Log lo lees tú con `tools/contentlog.py`.
   Recuerda probar con mobs **recién aparecidos** (los antiguos no tienen la propiedad del BP guardada).
4. Commits **atómicos** (un cambio lógico por commit), en español, estilo conventional (`fix(<mob>):`,
   `feat(tools):`, `docs:`…) y **sin** línea `Co-Authored-By`. Súbelos con push a `main` y comprueba
   la CI. Hook de pre-commit: `git config core.hooksPath tools/hooks`.

## Trampas conocidas (todas han roto el pack alguna vez)

- **`format_version` de las entidades de cliente = la de su archivo vanilla.** Las de 1.26.0 reparten
  Molang en varias líneas (`(cond) ? {` … `};`); con 1.10.0 la entidad no carga y el mob sale vanilla.
- **No uses `animation_controllers`** (lista antigua): el juego la rechaza en entidades de packs y se
  pierde la pose base (enderman con la cabeza separada). Mete los controladores en `animations` y
  lánzalos desde `scripts.animate`.
  En formato ≥ 1.10 esa lista es un duplicado de `scripts.animate`: bórrala, no la conviertas (se
  duplican las animaciones: cabezas que giran de más, brazos raros del gólem). Solo en 1.8.0 es la real.
- **Copia la `part_visibility` vanilla** en cada render controller `mv` que dibuje el cuerpo (brazos
  cruzados o sueltos del vindicador/evocador; si no, salen dos pares de brazos).
- **Un solo array de texturas por render controller** cuando el índice cambia de array: la rana con
  varios fue rechazada (`child 'Array.cold' not valid here`). Calcula el índice en la entidad.
- **Materiales inexistentes invalidan la entidad entera** (`[Json][error] Material "x" ... not defined`).
  Usa materiales vanilla (`entity_alphatest`, `enderman`, `stray_clothes`, …). No hay materiales propios.
- **`minecraft:add_attributes` no es un evento del motor**: nada que pongas ahí se ejecuta.
  Los sorteos van en `minecraft:entity_spawned` (y `entity_transformed` si procede).
- Índices de arrays en render controllers: `max(0, x) % tamaño` (dan la vuelta, no se recortan).
- `q.property('x')` sobre una propiedad que no existe da error: protégelo con `q.has_property('x')`.
- Claves que usa el motor por nombre y no deben llevar prefijo: `beam`, `beam_material`,
  `death_material` (dragón, guardián). Copia las claves vanilla que ningún render controller usa.
- Huesos de capas: copia **pivote y padre** del hueso vanilla. Si la pose vanilla mueve `body` (enderman
  sube 11 px), una capa sin ese padre queda descolocada.
- Windows: carpetas con `[ ]` rompen `glob` y `New-Item -Target` (comodines); VS Code bloquea archivos
  un instante al escribir (los `save()` de tools reintentan).

## Plantilla vanilla

`vanilla/` no está en git. Para regenerarla: `python -I tools/getvanilla.py` (descarga
`bedrock-samples-<versión>-full.zip` de [Mojang/bedrock-samples](https://github.com/Mojang/bedrock-samples/releases)).
La versión está en la constante `VERSION` de ese script (v1.26.60.5); para pasar a otra versión de
Minecraft, cámbiala y ejecuta `--force`. La CI usa el mismo script y cachea por versión.

## CI

`.github/workflows/checks.yml` se ejecuta en cada push a `main` y en cada PR: ruff + pyright sobre
`tools/`, y `validate`, `bpcheck`, `simulate`, `package` y `render` (de todos los mobs) sobre los packs.
Un tag `vX.Y.Z` lanza `release.yml`, que publica la release con los `.mcpack` y el `.mcaddon`. Los
renders quedan como artefacto `renders` del run (14 días): sirven para revisar visualmente un cambio.
