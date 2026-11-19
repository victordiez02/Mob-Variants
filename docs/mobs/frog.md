# frog

En la base: 20 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned, entity_transformed).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/frog.entity.json` sobre la vanilla `frog.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.frog` (RP/render_controllers/frog.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/frog.json`, `mv:variant` [0, 20], sorteo en: minecraft:entity_spawned, minecraft:entity_transformed

### `array.mv_skins` (skins, 40)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/frog/temperate_frog` (vanilla) | 1 (0.1%) |  |
| 2 | `mv_default2` | `textures/entity/frog/temperate_frog2` (pack) | 1 (0.1%) |  |
| 3 | `mv_default3` | `textures/entity/frog/temperate_frog3` (pack) | 1 (0.1%) |  |
| 4 | `mv_default4` | `textures/entity/frog/temperate_frog4` (pack) | 1 (0.1%) |  |
| 5 | `mv_default5` | `textures/entity/frog/temperate_frog5` (pack) | 1 (0.1%) |  |
| 6 | `mv_default6` | `textures/entity/frog/temperate_frog6` (pack) | 1 (0.1%) |  |
| 7 | `mv_default7` | `textures/entity/frog/temperate_frog7` (pack) | 1 (0.1%) |  |
| 8 | `mv_default8` | `textures/entity/frog/temperate_frog8` (pack) | 1 (0.1%) |  |
| 9 | `mv_default9` | `textures/entity/frog/temperate_frog9` (pack) | 1 (0.1%) |  |
| 10 | `mv_default10` | `textures/entity/frog/temperate_frog10` (pack) | 1 (0.1%) |  |
| 11 | `mv_default11` | `textures/entity/frog/cold_frog` (vanilla) | 100 (11.0%) |  |
| 12 | `mv_default12` | `textures/entity/frog/cold_frog2` (pack) | 100 (11.0%) |  |
| 13 | `mv_default13` | `textures/entity/frog/cold_frog3` (pack) | 100 (11.0%) |  |
| 14 | `mv_default14` | `textures/entity/frog/cold_frog4` (pack) | 100 (11.0%) |  |
| 15 | `mv_default15` | `textures/entity/frog/cold_frog5` (pack) | 100 (11.0%) |  |
| 16 | `mv_default16` | `textures/entity/frog/cold_frog6` (pack) | 100 (11.0%) |  |
| 17 | `mv_default17` | `textures/entity/frog/cold_frog7` (pack) | 100 (11.0%) |  |
| 18 | `mv_default18` | `textures/entity/frog/cold_frog8` (pack) | 100 (11.0%) |  |
| 19 | `mv_default19` | `textures/entity/frog/cold_frog9` (pack) | 100 (11.0%) |  |
| 20 | `mv_default20` | `textures/entity/frog/cold_frog10` (pack) | 1 (0.1%) |  |
| 21 | `mv_default21` | `textures/entity/frog/warm_frog` (vanilla) | — |  |
| 22 | `mv_default22` | `textures/entity/frog/warm_frog2` (pack) | — |  |
| 23 | `mv_default23` | `textures/entity/frog/warm_frog3` (pack) | — |  |
| 24 | `mv_default24` | `textures/entity/frog/warm_frog4` (pack) | — |  |
| 25 | `mv_default25` | `textures/entity/frog/warm_frog5` (pack) | — |  |
| 26 | `mv_default26` | `textures/entity/frog/warm_frog6` (pack) | — |  |
| 27 | `mv_default27` | `textures/entity/frog/warm_frog7` (pack) | — |  |
| 28 | `mv_default28` | `textures/entity/frog/warm_frog8` (pack) | — |  |
| 29 | `mv_default29` | `textures/entity/frog/warm_frog9` (pack) | — |  |
| 30 | `mv_default30` | `textures/entity/frog/warm_frog10` (pack) | — |  |
| 31 | `mv_default31` | `textures/entity/frog/special_frog` (pack) | — |  |
| 32 | `mv_default32` | `textures/entity/frog/special_frog2` (pack) | — |  |
| 33 | `mv_default33` | `textures/entity/frog/special_frog3` (pack) | — |  |
| 34 | `mv_default34` | `textures/entity/frog/special_frog4` (pack) | — |  |
| 35 | `mv_default35` | `textures/entity/frog/special_frog5` (pack) | — |  |
| 36 | `mv_default36` | `textures/entity/frog/special_frog6` (pack) | — |  |
| 37 | `mv_default37` | `textures/entity/frog/special_frog7` (pack) | — |  |
| 38 | `mv_default38` | `textures/entity/frog/special_frog8` (pack) | — |  |
| 39 | `mv_default39` | `textures/entity/frog/special_frog9` (pack) | — |  |
| 40 | `mv_default40` | `textures/entity/frog/cake_frog` (pack) | — |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- Cada clima (templado, frío, cálido) usa sus 10 skins; 11-20 son especiales para todos.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/frog.entity.json` (vanilla `frog.entity.json`)
- Render controller `controller.render.mv.frog` si `v.mv_active` (RP/render_controllers/frog.render_controllers.json)
- Render controller `controller.render.mv.frog_crown` si `v.mv_active` (RP/render_controllers/frog.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.frog_crown` → `geometry.mv.frog_crown` (RP/models/entity/frog_crown.geo.json, 1 cubos; cuelga de: body, root): `frog/frog_crown`

### BP

- Archivo: `BP/entities/frog.json`
- `mv:variant` [0, 20]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 10:1 11:100 12:100 13:100 14:100 15:100 16:100 17:100 18:100 19:100 20:1 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 10:1 11:100 12:100 13:100 14:100 15:100 16:100 17:100 18:100 19:100 20:1 (en minecraft:entity_spawned, minecraft:entity_transformed)
- `mv:mark_variant` [0, 2]: valor:peso 1:80 2:20 1:80 2:20 (en minecraft:entity_spawned, minecraft:entity_transformed)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
