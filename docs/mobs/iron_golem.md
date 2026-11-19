# iron_golem

En la base: 15 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/iron_golem.entity.json` sobre la vanilla `iron_golem.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.iron_golem` (RP/render_controllers/iron_golem.render_controllers.json)
- BP: `BP/entities/iron_golem.json`, `mv:variant` [0, 15], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 15)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/iron_golem/iron_golem` (vanilla) | 100 (6.7%) |  |
| 2 | `mv_default2` | `textures/entity/iron_golem/iron_golem2` (pack) | 100 (6.7%) |  |
| 3 | `mv_default3` | `textures/entity/iron_golem/iron_golem3` (pack) | 100 (6.7%) |  |
| 4 | `mv_default4` | `textures/entity/iron_golem/iron_golem4` (pack) | 100 (6.7%) |  |
| 5 | `mv_default5` | `textures/entity/iron_golem/iron_golem5` (pack) | 100 (6.7%) |  |
| 6 | `mv_default6` | `textures/entity/iron_golem/iron_golem6` (pack) | 100 (6.7%) |  |
| 7 | `mv_default7` | `textures/entity/iron_golem/iron_golem7` (pack) | 100 (6.7%) |  |
| 8 | `mv_default8` | `textures/entity/iron_golem/iron_golem8` (pack) | 100 (6.7%) |  |
| 9 | `mv_default9` | `textures/entity/iron_golem/iron_golem9` (pack) | 100 (6.7%) |  |
| 10 | `mv_default10` | `textures/entity/iron_golem/iron_golem10` (pack) | 100 (6.7%) |  |
| 11 | `mv_default11` | `textures/entity/iron_golem/iron_golem11` (pack) | 100 (6.7%) |  |
| 12 | `mv_default12` | `textures/entity/iron_golem/iron_golem12` (pack) | 100 (6.7%) |  |
| 13 | `mv_default13` | `textures/entity/iron_golem/iron_golem13` (pack) | 100 (6.7%) |  |
| 14 | `mv_default14` | `textures/entity/iron_golem/iron_golem14` (pack) | 100 (6.7%) |  |
| 15 | `mv_default15` | `textures/entity/iron_golem/iron_golem15` (pack) | 100 (6.7%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- `controller.render.iron_golem` no está en bedrock-samples: el render controller propio también dibuja la textura vanilla (variante 0) en vez de alternar con el vanilla.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/iron_golem.entity.json` (vanilla `iron_golem.entity.json`)
- Render controller `controller.render.mv.iron_golem` (RP/render_controllers/irongolem.render_controllers.json)
- Render controller `controller.render.mv.irongolem_rose` (RP/render_controllers/irongolem.render_controllers.json)
- Render controller `controller.render.iron_golem_cracks` (vanilla)

### Capas (accesorios)

- `controller.render.mv.irongolem_rose` → `geometry.mv.irongolem_rose` (RP/models/entity/irongolem_redflower.geo.json, 2 cubos; cuelga de: body, head): `iron_golem/iron_golem2`

### BP

- Archivo: `BP/entities/iron_golem.json`
- `mv:variant` [0, 16]: valor:peso 1:100 2:100 3:100 4:100 5:100 6:100 7:100 8:100 9:100 10:100 11:100 12:100 13:100 14:100 15:100 16:3 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 1]: valor:peso 0:7 1:3 (en minecraft:entity_spawned)

### Skins que no están en la base

- `iron_golem/iron_golem_item_sorter` (antes `mv:variant`=16): no pinta la cabeza (0 %)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
