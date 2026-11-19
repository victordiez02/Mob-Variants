# bee

En la base: 7 skins sobre el modelo vanilla, puerta `!q.is_baby`; BP con `mv:variant` (sorteo en entity_spawned, entity_born).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/bee.entity.json` sobre la vanilla `bee.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby);`
- Render controller: `controller.render.mv.bee` (RP/render_controllers/bee.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/bee.json`, `mv:variant` [0, 7], sorteo en: minecraft:entity_born, minecraft:entity_spawned

### `array.mv_skins` (skins, 7)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/bee/bee` (vanilla) | 1 (14.3%) |  |
| 2 | `mv_default2` | `textures/entity/bee/bee2` (pack) | 1 (14.3%) |  |
| 3 | `mv_default3` | `textures/entity/bee/bee3` (pack) | 1 (14.3%) |  |
| 4 | `mv_default4` | `textures/entity/bee/bee4` (pack) | 1 (14.3%) |  |
| 5 | `mv_default5` | `textures/entity/bee/bee5` (pack) | 1 (14.3%) |  |
| 6 | `mv_default6` | `textures/entity/bee/bee6` (pack) | 1 (14.3%) |  |
| 7 | `mv_default7` | `textures/entity/bee/bee7` (pack) | 1 (14.3%) |  |

### `array.mv_angry` (enfadada, 7)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_angry` | `textures/entity/bee/bee_angry` (vanilla) | 1 (14.3%) |  |
| 2 | `mv_angry2` | `textures/entity/bee/bee_angry2` (pack) | 1 (14.3%) |  |
| 3 | `mv_angry3` | `textures/entity/bee/bee_angry3` (pack) | 1 (14.3%) |  |
| 4 | `mv_angry4` | `textures/entity/bee/bee_angry4` (pack) | 1 (14.3%) |  |
| 5 | `mv_angry5` | `textures/entity/bee/bee_angry5` (pack) | 1 (14.3%) |  |
| 6 | `mv_angry6` | `textures/entity/bee/bee_angry6` (pack) | 1 (14.3%) |  |
| 7 | `mv_angry7` | `textures/entity/bee/bee_angry7` (pack) | 1 (14.3%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/bee.entity.json` (vanilla `bee.entity.json`)
- Render controller `controller.render.bee.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.bee` si `v.mv_active` (RP/render_controllers/bee.render_controllers.json)
- Render controller `controller.render.mv.bee_nectar` si `v.mv_active && q.property('minecraft:has_nectar')` (RP/render_controllers/bee.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.bee_nectar` → `geometry.mv.bee_nectar` (RP/models/entity/bee_nectar.geo.json, 1 cubos; cuelga de: body): `bee/nectar`

### BP

- Archivo: `BP/entities/bee.json`
- `mv:variant` [0, 7]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
