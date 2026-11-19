# wither_skeleton

En la base: 9 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/wither_skeleton.entity.json` sobre la vanilla `wither_skeleton.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.wither_skeleton` (RP/render_controllers/wither_skeleton.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/wither_skeleton.json`, `mv:variant` [0, 9], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 9)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/skeleton/wither_skeleton` (vanilla) | 5 (11.1%) |  |
| 2 | `mv_default2` | `textures/entity/skeleton/wither_skeleton2` (pack) | 5 (11.1%) |  |
| 3 | `mv_default3` | `textures/entity/skeleton/wither_skeleton3` (pack) | 5 (11.1%) |  |
| 4 | `mv_default4` | `textures/entity/skeleton/wither_skeleton4` (pack) | 5 (11.1%) |  |
| 5 | `mv_default5` | `textures/entity/skeleton/wither_skeleton5` (pack) | 5 (11.1%) |  |
| 6 | `mv_default6` | `textures/entity/skeleton/wither_skeleton6` (pack) | 5 (11.1%) |  |
| 7 | `mv_default7` | `textures/entity/skeleton/wither_skeleton7` (pack) | 5 (11.1%) |  |
| 8 | `mv_default8` | `textures/entity/skeleton/wither_skeleton8` (pack) | 5 (11.1%) |  |
| 9 | `mv_default9` | `textures/entity/skeleton/wither_skeleton9` (pack) | 5 (11.1%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- En el juego (con capas): **no se veía la espada**. Comprobar con la base (sin capas).

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/wither_skeleton.entity.json` (vanilla `wither_skeleton.entity.json`)
- Render controller `controller.render.mv.wither_skeleton` (RP/render_controllers/wither_skeleton.render_controllers.json)
- Render controller `controller.render.mv.wither_skeleton_cape` (RP/render_controllers/wither_skeleton.render_controllers.json)
- Render controller `controller.render.mv.backpack` (RP/render_controllers/wither_skeleton.render_controllers.json)
- Render controller `controller.render.mv.piglin_heads` (RP/render_controllers/wither_skeleton.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.wither_skeleton_cape` → `geometry.mv.wither_skeleton_cape` (RP/models/entity/wither_skeleton_cape.geo.json, 5 cubos; cuelga de: body, head, rightArm, waist): `skeleton/wither_skeleton_cape`
- `controller.render.mv.backpack` → `geometry.mv.backpack` (RP/models/entity/backpack.geo.json, 16 cubos; cuelga de: body, head, waist): `skeleton/backpack`
- `controller.render.mv.piglin_heads` → `geometry.mv.piglin_heads` (RP/models/entity/piglin_heads.geo.json, 13 cubos; cuelga de: body, waist): `skeleton/piglin_heads`

### BP

- Archivo: `BP/entities/wither_skeleton.json`
- `mv:variant` [0, 9]: valor:peso 1:5 2:5 3:5 4:5 5:5 6:5 7:5 8:5 9:5 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 2]: valor:peso 0:60 1:20 2:15 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
