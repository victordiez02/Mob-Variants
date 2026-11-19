# Arquitectura del sistema de variantes

Base actual (rama `skins-base`): **solo skins**. Cada mob con skins es su entidad vanilla actual con un
render controller propio que es una copia del vanilla en la que solo cambia la textura. Todo lo demás
(capas, variantes de modelo completo, animaciones propias) está en la etiqueta `legacy-v5` y vuelve de
uno en uno (skill `mv-mob`, fichas en [docs/mobs/](mobs/README.md)).

## Visión general

```
BP (opcional)                              RP (obligatorio)
──────────────                             ──────────────────────────────────────────────────
entidad vanilla actual                     entidad de cliente = vanilla actual
 + propiedad mv:variant (int, client_sync)   + claves mv_default, mv_default2… (texturas)
 + randomize con set_property al final de    + initialize:    v.xvar = math.random_integer(1, N)
   entity_spawned (y entity_born /           + pre_animation: v.mv_variant = BP o v.xvar
   entity_transformed si existen)                             v.mv_active  = v.mv_variant > 0 && puerta
                                             + render controllers: el vanilla con !v.mv_active,
                                               controller.render.mv.<mob> con v.mv_active
```

- **Con BP**: el servidor elige la skin al aparecer el mob (1..N, con los pesos del `randomize`) y la
  guarda en `mv:variant`. Todos los jugadores ven lo mismo y no cambia al recargar. Un mob que ya existía
  antes de instalar el BP tiene `mv:variant = 0` y se ve vanilla.
- **Sin BP** (solo RP): `q.has_property('mv:variant')` es falso y se usa el sorteo local `v.xvar`
  (uniforme, sin pesos). Cada jugador ve una skin distinta y cambia al recargar.
- `mv:variant` **N** usa `array.mv_skins[N - 1]`. La skin 1 suele ser la textura vanilla (o su retextura
  en la ruta vanilla), así que sale también "el mob de siempre".

## Resource pack

### Entidad de cliente (`RP/entity/<mob>.entity.json`)

Copia del archivo vanilla actual (`mvlib.vanilla_client_entity`: el de mayor `min_engine_version`, no el
`*.v1.0`) con:

- Texturas `mv_default`, `mv_default2`, … en el orden de `mv:variant`. Mobs con un segundo juego de
  texturas por estado: `mv_angry*` (abeja enfadada), `mv_charging*` (ghast disparando), `mv_saddled*`
  (cerdo con silla).
- `initialize` + `v.xvar = math.random_integer(1, N);` (rana: `math.random(0, 100)`, ver su ficha).
- Al principio de `pre_animation`:
  ```
  v.mv_variant = q.has_property('mv:variant') ? q.property('mv:variant') : v.xvar;
  v.mv_active = v.mv_variant > 0 && (!q.is_baby);      // puerta del mob, si tiene
  ```
  La puerta (regla 3) deja vanilla a los bebés y a las variantes vanilla que no son la de por defecto
  (pollo y cerdo: solo clima templado).
- `render_controllers`: el render controller vanilla del cuerpo con `!v.mv_active` (sumado a su condición
  vanilla, p. ej. el dragón `(query.death_ticks <= 1.0) && !v.mv_active`) y justo detrás el propio con
  `v.mv_active`. El resto de render controllers vanilla (carga del creeper, grietas del gólem, capas del
  warden, ropa de los aldeanos zombi…) se quedan como en vanilla.
- `format_version` como el vanilla, salvo los 1.8.0 con lista `animation_controllers`, que se convierten
  a `animations` + `scripts.animate` y pasan a 1.10.0 (trampa de CLAUDE.md).

### Render controller (`RP/render_controllers/<mob>.render_controllers.json`)

`controller.render.mv.<mob>` = **copia exacta del render controller vanilla** del cuerpo (geometría,
`part_visibility`, materiales, arrays de geometrías) cambiando solo la textura:

- Si el vanilla usa `Texture.default`, se sustituye ese token por `array.mv_skins[v.mv_variant - 1]`
  (conserva ramas vanilla como `query.is_elder ? Texture.elder : …`).
- Si el vanilla elige la textura con un array (abeja, pollo, rana, ghast, cerdo), la expresión se
  escribe a mano: p. ej. `query.is_angry ? array.mv_angry[v.mv_variant - 1] : array.mv_skins[v.mv_variant - 1]`.
- Casos especiales (detalle en su ficha):
  - **Cerdo**: sus skins usan el layout del modelo antiguo 64×32, así que el render controller propio
    dibuja la geometría vanilla antigua `geometry.pig` (clave `mv_legacy`, material `pig`) y la entidad
    lanza `animation.pig.setup.v1.0` (`mv_setup_legacy`) en vez de `setup` cuando `v.mv_active`.
  - **Gólem de hierro**: `controller.render.iron_golem` no está en bedrock-samples, así que el propio
    sustituye al vanilla y dibuja `Texture.default` cuando `!v.mv_active`.
  - **Rana**: un solo array de 40 (`temperate1-10`, `cold1-10`, `warm1-10`, especiales); la entidad
    calcula el índice `v.mv_skin` con el clima (`q.variant`).

Sin materiales propios: se usan las claves de material vanilla de la entidad.

### Texturas

- Skins en `RP/textures/entity/<mob>/` (algunas carpetas vanilla compartidas: `illager/`, `piglin/`…).
- Retexturas en la ruta vanilla (regla 6): `horse2/`, `panda/`, `slime/slime`, `skeleton/stray*`,
  `sheep/sheep.tga`, y las skin 1 de pollo, cerdo, sniffer y zombi (`chicken/chicken`, `pig/pig`, …),
  que también cambian el mob cuando se ve vanilla.
- Toda skin debe **pintar todas las piezas del modelo vanilla** que pinta la textura vanilla:
  `python tools/inventory.py` lo comprueba (columna "Revisar" de la ficha).

## Behavior pack (`BP/entities/<archivo vanilla>.json`)

Copia del archivo vanilla actual (regla 5) con:

```json
"properties": { "mv:variant": { "type": "int", "range": [0, N], "default": 0, "client_sync": true } }
```

y un `{"randomize": [{"weight": w, "set_property": {"mv:variant": i}}, …]}` al final de
`minecraft:entity_spawned` (envolviendo el evento en `sequence` si hace falta, o creándolo), y de
`minecraft:entity_born` / `minecraft:entity_transformed` si el vanilla los tiene (crías, renacuajo → rana,
aldeano → aldeano zombi). `bpcheck.py` comprueba que el resto es idéntico al vanilla.

## Cómo añadir una skin

`python -I tools/addskin.py <mob> <png> --dry-run` y luego sin `--dry-run` (skill `mv-skin`): copia el PNG,
añade la clave, la entrada del array, sube el `N` del sorteo local y el `range` y los `randomize` del BP.
Después `python tools/inventory.py <mob>` (cobertura) y la skill `mv-verify`.

## Cómo añadir un mob

1. Entidad vanilla actual + claves, `initialize`, `pre_animation` y render controllers como arriba.
2. `controller.render.mv.<mob>`: copia del render controller vanilla del cuerpo cambiando la textura.
3. BP: archivo vanilla + propiedad + `randomize`. Nunca uses `minecraft:variant`/`mark_variant` (vanilla).
4. `python tools/inventory.py <mob>`, skill `mv-verify` y prueba en el juego.

## Cuando vuelvan los extras

Reglas que siguen valiendo (CLAUDE.md, reglas 1 y 2): capas con huesos de nombre, pivote y padre vanilla
y piezas `mv_*`; variantes de modelo completo con los huesos renombrados a los vanilla (`geotool rebone`);
`part_visibility` vanilla copiada en cada render controller que dibuje el cuerpo; cada propiedad del BP
que dependa de otra se sortea en un evento posterior (los filtros `int_property` del mismo evento leen el
valor antiguo, sospecha del casco de minero en zombis tumbados). Procedimiento: skill `mv-mob`.
