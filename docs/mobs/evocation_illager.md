# evocation_illager

En la base: 31 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/evocation_illager.entity.json` sobre la vanilla `evocation_illager.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.evocation_illager` (RP/render_controllers/evocation_illager.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/evocation_illager.json`, `mv:variant` [0, 31], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 31)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/illager/evoker` (vanilla) | 1 (3.2%) |  |
| 2 | `mv_default2` | `textures/entity/illager/evoker2` (pack) | 1 (3.2%) |  |
| 3 | `mv_default3` | `textures/entity/illager/evoker3` (pack) | 1 (3.2%) |  |
| 4 | `mv_default4` | `textures/entity/illager/evoker4` (pack) | 1 (3.2%) |  |
| 5 | `mv_default5` | `textures/entity/illager/evoker5` (pack) | 1 (3.2%) |  |
| 6 | `mv_default6` | `textures/entity/illager/evoker6` (pack) | 1 (3.2%) |  |
| 7 | `mv_default7` | `textures/entity/illager/evoker7` (pack) | 1 (3.2%) |  |
| 8 | `mv_default8` | `textures/entity/illager/evoker8` (pack) | 1 (3.2%) |  |
| 9 | `mv_default9` | `textures/entity/illager/evoker9` (pack) | 1 (3.2%) |  |
| 10 | `mv_default10` | `textures/entity/illager/evoker10` (pack) | 1 (3.2%) |  |
| 11 | `mv_default11` | `textures/entity/illager/evoker11` (pack) | 1 (3.2%) |  |
| 12 | `mv_default12` | `textures/entity/illager/evoker12` (pack) | 1 (3.2%) |  |
| 13 | `mv_default13` | `textures/entity/illager/evoker13` (pack) | 1 (3.2%) |  |
| 14 | `mv_default14` | `textures/entity/illager/evoker14` (pack) | 1 (3.2%) |  |
| 15 | `mv_default15` | `textures/entity/illager/evoker15` (pack) | 1 (3.2%) |  |
| 16 | `mv_default16` | `textures/entity/illager/evoker16` (pack) | 1 (3.2%) |  |
| 17 | `mv_default17` | `textures/entity/illager/evoker17` (pack) | 1 (3.2%) |  |
| 18 | `mv_default18` | `textures/entity/illager/evoker18` (pack) | 1 (3.2%) |  |
| 19 | `mv_default19` | `textures/entity/illager/evoker19` (pack) | 1 (3.2%) |  |
| 20 | `mv_default20` | `textures/entity/illager/evoker20` (pack) | 1 (3.2%) |  |
| 21 | `mv_default21` | `textures/entity/illager/evoker21` (pack) | 1 (3.2%) |  |
| 22 | `mv_default22` | `textures/entity/illager/evoker22` (pack) | 1 (3.2%) |  |
| 23 | `mv_default23` | `textures/entity/illager/evoker23` (pack) | 1 (3.2%) |  |
| 24 | `mv_default24` | `textures/entity/illager/evoker24` (pack) | 1 (3.2%) |  |
| 25 | `mv_default25` | `textures/entity/illager/evoker25` (pack) | 1 (3.2%) |  |
| 26 | `mv_default26` | `textures/entity/illager/evoker26` (pack) | 1 (3.2%) |  |
| 27 | `mv_default27` | `textures/entity/illager/evoker27` (pack) | 1 (3.2%) |  |
| 28 | `mv_default28` | `textures/entity/illager/evoker29` (pack) | 1 (3.2%) |  |
| 29 | `mv_default29` | `textures/entity/illager/evoker30` (pack) | 1 (3.2%) |  |
| 30 | `mv_default30` | `textures/entity/illager/evoker31` (pack) | 1 (3.2%) |  |
| 31 | `mv_default31` | `textures/entity/illager/evoker32` (pack) | 1 (3.2%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- Skins 5 y 10 no pintaban los brazos cruzados: arreglado en d4a47a1.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/evocation_illager.entity.json` (vanilla `evocation_illager.entity.json`)
- Render controller `controller.render.mv.evoker` (RP/render_controllers/evoker.render_controllers.json)
- Render controller `controller.render.mv.evoker_hat` (RP/render_controllers/evoker.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.evoker_hat` → `geometry.mv.evoker_wizard` (RP/models/entity/evoker_wizard.geo.json, 32 cubos; cuelga de: body, head, leftArm, leftLeg, rightArm, rightItem, rightLeg): `illager/evoker_wizard`
- `controller.render.mv.evoker_hat` → `geometry.mv.evoker_windcaller` (RP/models/entity/evoker_windcaller.geo.json, 21 cubos; cuelga de: body, cape, head, leftArm, rightArm, rightItem, root, staff, staff_item, waist): `illager/evoker_windcaller`
- `controller.render.mv.evoker_hat` → `geometry.mv.evoker_enchanter` (RP/models/entity/evoker_enchanter.geo.json, 18 cubos; cuelga de: body, bone, book, cover_back, cover_front, head, leftArm, paper, paper1, paper2, paper3, paper4, paper5, rightArm, root, waist): `illager/evoker_enchanter`
- `controller.render.mv.evoker_hat` → `geometry.mv.evoker_geomancer` (RP/models/entity/evoker_geomancer.geo.json, 17 cubos; cuelga de: body, head, left_eyebrow, nose, rightArm, rightItem, right_eyebrow, root, waist): `illager/evoker_geomancer`
- `controller.render.mv.evoker_hat` → `geometry.mv.evoker_chef` (RP/models/entity/evoker_chef.geo.json, 3 cubos; cuelga de: body, head): `illager/evoker_chef`
- `controller.render.mv.evoker_hat` → `geometry.mv.evoker_hat` (RP/models/entity/evoker_hat.geo.json, 27 cubos; cuelga de: body, head, leftArm, rightArm, rightItem): `illager/evoker_hat`, `illager/evoker_hat2`, `illager/evoker_hat3`, `illager/evoker_no_hat`

### BP

- Archivo: `BP/entities/evocation_illager.json`
- `mv:variant` [0, 32]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 10:1 11:1 12:1 13:1 14:1 15:1 16:1 17:1 18:1 19:1 20:1 21:1 22:1 23:1 24:1 25:1 26:1 27:1 28:1 29:1 30:1 31:1 32:1 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 8]: valor:peso 0:40 1:1 2:1 3:1 4:245 5:245 6:245 7:245 8:2 (en minecraft:entity_spawned)

### Skins que no están en la base

- `illager/evoker28` (antes `mv:variant`=28): no pinta las piernas (0 %): sale flotando

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
