# Arquitectura del sistema de variantes

## Visión general

```
BP (opcional)                         RP (obligatorio)
──────────────                        ─────────────────────────────────────────────
entidad vanilla 1.26.x                entidad de cliente = vanilla actual
 + propiedades mv:variant /             + claves mv_* (texturas, geometrías, materiales)
   mv:mark_variant (int, client_sync)   + render controllers controller.render.mv.*
 + nodos set_property en eventos        + scripts:
   (entity_spawned, …)                     initialize:   v.xvar = math.random(0, 99)  (sorteo local)
                                           pre_animation: v.mv_variant / v.mv_mark  (BP o 0)
                                                          v.mv_active               (¿aplicar skins?)
```

- **Con BP**: el servidor elige la variante al aparecer el mob y la guarda en `mv:variant` /
  `mv:mark_variant`. Todos los jugadores ven lo mismo y no cambia al recargar.
- **Sin BP** (solo RP): `q.has_property('mv:variant')` es falso, `v.mv_variant = 0` y el render controller
  usa el sorteo local `v.xvar` (0-99). Cada jugador ve una skin distinta y cambia al recargar.
  El valor 0 significa siempre "sin variante guardada" (por eso las variantes del BP empiezan en 1).

## Resource pack

### Entidad de cliente (`RP/entity/<mob>.entity.json`)

Se parte **siempre** de la entidad vanilla actual (el archivo con mayor `min_engine_version` en
`vanilla/resource_pack/entity/`, no el `*.v1.0`) y se le añade:

- Claves propias con prefijo `mv_` (`mv_default`, `mv_default2`, …, `mv_hat`, `mv_empty`…).
  Las claves vanilla se conservan sin tocar para los render controllers vanilla.
- `format_version` y `min_engine_version` **iguales a los del archivo vanilla**.
- Sus `animations`/`scripts` vanilla tal cual, más:
  ```json
  "initialize":   ["v.xvar = math.random(0,99);"],
  "pre_animation": [ "...líneas vanilla...",
    "v.mv_variant = q.has_property('mv:variant') ? q.property('mv:variant') : 0;",
    "v.mv_mark = q.has_property('mv:mark_variant') ? q.property('mv:mark_variant') : 0;",
    "v.mv_active = !q.is_baby && q.property('minecraft:climate_variant') == 'temperate';" ]
  ```
- `render_controllers`:
  - **Mobs con puerta** (tienen bebé o variantes vanilla): render controllers vanilla con condición
    `!v.mv_active` y los propios con `v.mv_active`.
  - **Mobs "siempre"** (sin bebé ni variantes): solo los propios, más capas vanilla necesarias
    (p. ej. `controller.render.creeper_armor` con `query.is_powered`).

Puertas actuales: `!q.is_baby` (+ `q.variant == 0` en gato/zorro, `q.variant == 0` en rana,
clima `temperate` en pollo/cerdo). Lista completa en STATUS.md.

### Render controllers (`RP/render_controllers/*.render_controllers.json`)

- IDs `controller.render.mv.<mob>[_capa]`; referencias `Texture.mv_*`, `Geometry.mv_*`, `Material.mv_*`.
- Patrón histórico (la mayoría):
  `"v.mv_variant ? array.xskins[v.mv_variant - 1] : array.xskins[variable.xvar]"` → con BP usa el
  valor guardado; sin BP, el sorteo (los arrays dan la vuelta: `xvar % tamaño`).
- Patrón recomendado (gato, zorro, rana): la entidad calcula **un solo** `v.mv_variant` en
  `pre_animation`, sea del BP o del sorteo, y el render controller solo lee esa variable:
  ```
  v.mv_variant = q.has_property('mv:variant') ? q.property('mv:variant') : (v.xvar < 5 ? 2 : (v.xvar < 20 ? 1 : 0));
  ```
  Así las probabilidades con y sin BP coinciden y el render controller queda simple.
- Comentario `//` de cabecera explicando qué significa cada valor de `v.mv_variant` / `v.mv_mark`
  (Bedrock acepta comentarios en JSON).

### Geometrías (`RP/models/entity/*.geo.json`)

- Formato `minecraft:geometry` ≥ 1.12.0, IDs `geometry.mv.*`.
- **Capas**: huesos raíz con nombre, pivote y padre del hueso vanilla; hijos `mv_*` con las piezas.
  Ejemplos: `witch_extras.geo.json` (sombrero, escoba…), `spider_fangs.geo.json`,
  `spider_giant_legs.geo.json` (prolonga `legN`), `pig_extras.geo.json` (orejas y cola).
  `tools/overlay.py` genera estas capas a partir de un modelo antiguo.
- `geometry.mv.zombie_empty` es una geometría vacía para "no dibujar nada" en un render controller.
- Las geometrías de variante completa (capibara, caracol, pato, oca, ornitorrinco, gatos especiales,
  zombis caídos…) se mantienen de momento; revisar con el usuario si chocan con la regla de "no
  sustituir el modelo" cuando se aborde la compatibilidad con A&S.

### Texturas

- Skins del addon en `RP/textures/entity/<mob>/`. Algunas están en rutas vanilla a propósito
  (retexturas: caballos, panda, slime, wither, stray, `cow`…); no las borres sin preguntar.
- Si una skin se pintó para un modelo re-rigueado con extremidades partidas, `tools/limbmerge.py`
  recoloca los píxeles en el layout de la extremidad vanilla (se usó en el cerdo).

### Modelos antiguos vanilla

Si las skins usan el layout de un modelo vanilla **antiguo** (cerdo 64×32), en modo activo se usa
esa geometría vanilla (`geometry.pig`) y su animación antigua (`animation.pig.setup.v1.0`) con
condición `v.mv_active`; la actual queda con `!v.mv_active`.

## Behavior pack

- Cada `BP/entities/<mob>.json` = archivo vanilla actual + :
  ```json
  "properties": { "mv:variant": { "type": "int", "range": [0, N], "default": 0, "client_sync": true } }
  ```
  y nodos añadidos al final del evento vanilla, envolviéndolo en `sequence` si hace falta:
  ```json
  { "randomize": [ { "weight": 70, "set_property": { "mv:variant": 1 } }, … ] }
  ```
- Grupos/eventos propios (no vanilla) con prefijo `mv:` (p. ej. temporizadores de flores del sniffer
  `mv:torchflower_change_1to2`, `mv:pickup_items` del zombi).
- Mecánicas propias conservadas: flores del sniffer que crecen; zombis con algo clavado
  (`mv:mark_variant` ≥ 100) no recogen objetos; araña gigante (`mv:mark_variant == 1`).
- Las probabilidades de diseño están en `docs/Probabilities.pdf` (algunas difieren ligeramente del
  sorteo sin BP; el BP manda).

## Cómo añadir una skin a un mob existente

1. Textura en `RP/textures/entity/<mob>/`.
2. Clave `mv_<nombre>` en `textures` de la entidad y entrada al final del array del render controller.
3. Si el mob tiene BP: ampliar `range` de la propiedad y añadir el `set_property` al `randomize`.
4. `tools/validate.py`, `tools/bpcheck.py`, `tools/simulate.py <mob>`.

## Cómo añadir un mob nuevo

1. Copia la entidad vanilla actual de `vanilla/resource_pack/entity/` (misma `format_version`).
2. Añade claves `mv_*`, `initialize`/`pre_animation` como arriba y `v.mv_active` si tiene bebé o variantes.
3. Render controller `controller.render.mv.<mob>` con `Geometry.mv_default` = la geometría vanilla.
4. (Opcional) BP: copia la entidad vanilla de `vanilla/behavior_pack/entities/`, añade la propiedad
   y los `set_property`. Nunca uses `minecraft:variant`/`mark_variant` para lo nuestro: vanilla los usa.
5. Valida y pide prueba en el juego.
