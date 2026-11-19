# chicken

En la base: 4 skins sobre el modelo vanilla, puerta `!q.is_baby && q.property('minecraft:climate_variant') == 'temperate'`; BP con `mv:variant` (sorteo en entity_spawned, entity_born).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/chicken.entity.json` sobre la vanilla `chicken.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby && q.property('minecraft:climate_variant') == 'temperate');`
- Render controller: `controller.render.mv.chicken` (RP/render_controllers/chicken.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/chicken.json`, `mv:variant` [0, 4], sorteo en: minecraft:entity_born, minecraft:entity_spawned

### `array.mv_skins` (skins, 4)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/chicken/chicken` (pack) | 7 (25.0%) |  |
| 2 | `mv_default2` | `textures/entity/chicken/chicken3` (pack) | 7 (25.0%) |  |
| 3 | `mv_default3` | `textures/entity/chicken/chicken4` (pack) | 7 (25.0%) |  |
| 4 | `mv_default4` | `textures/entity/chicken/chicken5` (pack) | 7 (25.0%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- En el juego: la oca bien; el pato no movía las patas (arreglado renombrando huesos con `geotool rebone`). El usuario pidió quitar la skin de pollito (`chicken2`).

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/chicken.entity.json` (vanilla `chicken.entity.json`)
- Render controller `controller.render.chicken.v3` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.chicken` si `v.mv_active` (RP/render_controllers/chicken.render_controllers.json)
- Render controller `controller.render.mv.chicken_extras` si `v.mv_active && v.mv_is_chicken` (RP/render_controllers/chicken.render_controllers.json)

### Variantes de modelo completo

Geometría propia dibujada en lugar del cuerpo vanilla (huesos con nombre vanilla para que la animen las animaciones vanilla; ver `geotool rebone`).

- `geometry.mv.duck` (RP/models/entity/duck.geo.json, 11 cubos; huesos: beak, body, head, leg0, leg1, wing0, wing1): `chicken/duck`, `chicken/duck2`, `chicken/duck3`
- `geometry.mv.goose` (RP/models/entity/goose.geo.json, 14 cubos; huesos: body, head, leg0, leg1, wing0, wing1): `chicken/goose`, `chicken/goose2`, `chicken/goose3`, `chicken/goose4`

### Capas (accesorios)

- `controller.render.mv.chicken_extras` → `geometry.mv.chicken_extras` (RP/models/entity/chicken_extras.geo.json, 4 cubos; cuelga de: body, head): `chicken/chicken`, `chicken/chicken3`, `chicken/chicken4`, `chicken/chicken5`

### BP

- Archivo: `BP/entities/chicken.json`
- `mv:variant` [0, 11]: valor:peso 1:7 2:7 3:7 4:7 5:1.5 6:1.5 7:1.5 8:1.5 9:1.5 10:1.5 11:1.5 (en minecraft:entity_spawned)

### Skins que no están en la base

- `chicken/goose` (antes `mv:variant`=5): variante de modelo completo `geometry.mv.goose`
- `chicken/goose2` (antes `mv:variant`=6): variante de modelo completo `geometry.mv.goose`
- `chicken/goose3` (antes `mv:variant`=7): variante de modelo completo `geometry.mv.goose`
- `chicken/goose4` (antes `mv:variant`=8): variante de modelo completo `geometry.mv.goose`
- `chicken/duck` (antes `mv:variant`=9): variante de modelo completo `geometry.mv.duck`
- `chicken/duck2` (antes `mv:variant`=10): variante de modelo completo `geometry.mv.duck`
- `chicken/duck3` (antes `mv:variant`=11): variante de modelo completo `geometry.mv.duck`

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
