# skeleton

En la base: 15 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/skeleton.entity.json` sobre la vanilla `skeleton.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.skeleton` (RP/render_controllers/skeleton.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/skeleton.json`, `mv:variant` [0, 15], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 15)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/skeleton/skeleton` (vanilla) | 1 (6.7%) |  |
| 2 | `mv_default2` | `textures/entity/skeleton/skeleton2` (pack) | 1 (6.7%) |  |
| 3 | `mv_default3` | `textures/entity/skeleton/skeleton3` (pack) | 1 (6.7%) |  |
| 4 | `mv_default4` | `textures/entity/skeleton/skeleton4` (pack) | 1 (6.7%) |  |
| 5 | `mv_default5` | `textures/entity/skeleton/skeleton5` (pack) | 1 (6.7%) |  |
| 6 | `mv_default6` | `textures/entity/skeleton/skeleton6` (pack) | 1 (6.7%) |  |
| 7 | `mv_default7` | `textures/entity/skeleton/skeleton7` (pack) | 1 (6.7%) |  |
| 8 | `mv_default8` | `textures/entity/skeleton/skeleton8` (pack) | 1 (6.7%) |  |
| 9 | `mv_default9` | `textures/entity/skeleton/skeleton9` (pack) | 1 (6.7%) |  |
| 10 | `mv_default10` | `textures/entity/skeleton/skeleton10` (pack) | 1 (6.7%) |  |
| 11 | `mv_default11` | `textures/entity/skeleton/skeleton11` (pack) | 1 (6.7%) |  |
| 12 | `mv_default12` | `textures/entity/skeleton/skeleton12` (pack) | 1 (6.7%) |  |
| 13 | `mv_default13` | `textures/entity/skeleton/skeleton13` (pack) | 1 (6.7%) |  |
| 14 | `mv_default14` | `textures/entity/skeleton/skeleton14` (pack) | 1 (6.7%) |  |
| 15 | `mv_default15` | `textures/entity/skeleton/skeleton15` (pack) | 1 (6.7%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/skeleton.entity.json` (vanilla `skeleton.entity.json`)
- Render controller `controller.render.mv.skeleton` (RP/render_controllers/skeleton.render_controllers.json)
- Render controller `controller.render.mv.skeleton_clothes` (RP/render_controllers/skeleton.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.skeleton_clothes` → `geometry.mv.skeleton.armor` (RP/models/entity/skeleton_armor.geo.json, 7 cubos; cuelga de: body, leftArm, rightArm, rightItem, waist): `skeleton/skeleton_overlay`
- `controller.render.mv.skeleton_clothes` → `geometry.mv.skeleton.armor2` (RP/models/entity/skeleton_armor2.geo.json, 8 cubos; cuelga de: arrows, body, bone, cape, head, leftArm, quiver, rightArm, root, spine, sticks): `skeleton/skeleton_overlay2`

### BP

- Archivo: `BP/entities/skeleton.json`
- `mv:variant` [0, 15]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 10:1 11:1 12:1 13:1 14:1 15:1 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 1]: valor:peso 0:1 1:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
