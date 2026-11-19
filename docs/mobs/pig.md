# pig

En la base: 5 skins sobre el modelo vanilla, puerta `!q.is_baby && q.property('minecraft:climate_variant') == 'temperate'`; BP con `mv:variant` (sorteo en entity_spawned, entity_born).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/pig.entity.json` sobre la vanilla `pig.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby && q.property('minecraft:climate_variant') == 'temperate');`
- Render controller: `controller.render.mv.pig` (RP/render_controllers/pig.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/pig.json`, `mv:variant` [0, 5], sorteo en: minecraft:entity_born, minecraft:entity_spawned

### `array.mv_skins` (skins, 5)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/pig/pig` (pack) | 805 (20.0%) |  |
| 2 | `mv_default2` | `textures/entity/pig/pig2` (pack) | 805 (20.0%) |  |
| 3 | `mv_default3` | `textures/entity/pig/pig3` (pack) | 805 (20.0%) |  |
| 4 | `mv_default4` | `textures/entity/pig/pig4` (pack) | 805 (20.0%) |  |
| 5 | `mv_default5` | `textures/entity/pig/pig5` (pack) | 805 (20.0%) |  |

### `array.mv_saddled` (con silla, 5)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_saddled` | `textures/entity/pig/pig_saddle` (pack) | 805 (20.0%) |  |
| 2 | `mv_saddled2` | `textures/entity/pig/pig_saddle2` (pack) | 805 (20.0%) |  |
| 3 | `mv_saddled3` | `textures/entity/pig/pig_saddle3` (pack) | 805 (20.0%) |  |
| 4 | `mv_saddled4` | `textures/entity/pig/pig_saddle4` (pack) | 805 (20.0%) |  |
| 5 | `mv_saddled5` | `textures/entity/pig/pig_saddle5` (pack) | 805 (20.0%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- Las skins usan el layout del modelo antiguo 64×32: en la base se dibujan con la geometría vanilla antigua `geometry.pig` y `animation.pig.setup.v1.0` (vanilla, no propias).

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/pig.entity.json` (vanilla `pig.entity.json`)
- Render controller `controller.render.saddle` si `!v.mv_active` (vanilla)
- Render controller `controller.render.pig.v4` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.pig` si `v.mv_active` (RP/render_controllers/pig.render_controllers.json)
- Render controller `controller.render.mv.pig_extras` si `v.mv_active && v.mv_pig_shape` (RP/render_controllers/pig.render_controllers.json)
- Render controller `controller.render.mv.pig_chest` si `v.mv_active` (RP/render_controllers/pig.render_controllers.json)
- Render controller `controller.render.mv.pig_flower` si `v.mv_active` (RP/render_controllers/pig.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.pig` → `geometry.mv.capibara` (RP/models/entity/pig_capibara.geo.json, 12 cubos; cuelga de: body, head, leg0, leg1, leg2, leg3): `pig/capibara`, `pig/capibara_saddle`
- `controller.render.mv.pig` → `geometry.mv.snail` (RP/models/entity/pig_snail.geo.json, 7 cubos; cuelga de: head): `pig/snail`, `pig/snail_saddle`
- `controller.render.mv.pig_chest` → `geometry.mv.pig_chest` (RP/models/entity/pig_chest.geo.json, 5 cubos; cuelga de: body): `pig/pig_chest`
- `controller.render.mv.pig_flower` → `geometry.mv.pig_flower` (RP/models/entity/pig_flower.geo.json, 2 cubos; cuelga de: head): `iron_golem/iron_golem2`
- `controller.render.mv.pig_extras` → `geometry.mv.pig_extras` (RP/models/entity/pig_extras.geo.json, 7 cubos; cuelga de: body, head): 12 texturas (las skins del cuerpo: `pig/pig`, … )

### BP

- Archivo: `BP/entities/pig.json`
- `mv:variant` [0, 8]: valor:peso 1:805 2:805 3:805 4:805 5:805 6:100 7:100 8:5 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 3]: valor:peso 0:875 1:100 2:20 3:5 (en minecraft:entity_spawned)

### Skins que no están en la base

- `pig/capibara` (antes `mv:variant`=6): variante de modelo completo `geometry.mv.capibara`
- `pig/snail` (antes `mv:variant`=7): variante de modelo completo `geometry.mv.snail`
- `pig/pig_gold` (antes `mv:variant`=8): cerdo dorado: usaba el material `enderman` (brillo); con el material vanilla sale transparente

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
