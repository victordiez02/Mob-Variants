# vindicator

En la base: 21 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/vindicator.entity.json` sobre la vanilla `vindicator.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.vindicator` (RP/render_controllers/vindicator.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/vindicator.json`, `mv:variant` [0, 21], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 21)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/vindicator` (vanilla) | 1000 (5.0%) |  |
| 2 | `mv_default2` | `textures/entity/vindicator/vindicator2` (pack) | 1000 (5.0%) |  |
| 3 | `mv_default3` | `textures/entity/vindicator/vindicator3` (pack) | 1000 (5.0%) |  |
| 4 | `mv_default4` | `textures/entity/vindicator/vindicator4` (pack) | 1000 (5.0%) |  |
| 5 | `mv_default5` | `textures/entity/vindicator/vindicator5` (pack) | 1000 (5.0%) |  |
| 6 | `mv_default6` | `textures/entity/vindicator/vindicator6` (pack) | 1000 (5.0%) |  |
| 7 | `mv_default7` | `textures/entity/vindicator/vindicator7` (pack) | 1000 (5.0%) |  |
| 8 | `mv_default8` | `textures/entity/vindicator/vindicator8` (pack) | 1000 (5.0%) |  |
| 9 | `mv_default9` | `textures/entity/vindicator/vindicator9` (pack) | 1000 (5.0%) |  |
| 10 | `mv_default10` | `textures/entity/vindicator/vindicator10` (pack) | 1000 (5.0%) | nose 0% |
| 11 | `mv_default11` | `textures/entity/vindicator/vindicator11` (pack) | 1000 (5.0%) |  |
| 12 | `mv_default12` | `textures/entity/vindicator/vindicator13` (pack) | 1000 (5.0%) |  |
| 13 | `mv_default13` | `textures/entity/vindicator/vindicator14` (pack) | 1000 (5.0%) | nose 0% |
| 14 | `mv_default14` | `textures/entity/vindicator/vindicator15` (pack) | 1000 (5.0%) |  |
| 15 | `mv_default15` | `textures/entity/vindicator/vindicator16` (pack) | 1000 (5.0%) |  |
| 16 | `mv_default16` | `textures/entity/vindicator/vindicator17` (pack) | 1000 (5.0%) |  |
| 17 | `mv_default17` | `textures/entity/vindicator/vindicator18` (pack) | 1000 (5.0%) |  |
| 18 | `mv_default18` | `textures/entity/vindicator/vindicator19` (pack) | 1000 (5.0%) |  |
| 19 | `mv_default19` | `textures/entity/vindicator/vindicator20` (pack) | 1000 (5.0%) |  |
| 20 | `mv_default20` | `textures/entity/vindicator/vindicator21` (pack) | 1000 (5.0%) |  |
| 21 | `mv_default21` | `textures/entity/vindicator/vindicator_clown` (pack) | 5 (0.0%) | nose 40% |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- En el juego (19-11-2026, con capas): el **hacha no se veía nunca** al enfadarse. El BP da el hacha igual que el vanilla (`vindicator_gear`). Sospecha sin confirmar: el objeto se engancha a `rightItem` de una geometría que no lo tiene (capas de armadura / vacía). Comprobar primero con la base.
- Las armaduras (capa) no se adaptaban a los brazos cruzados (`arms`): solo colgaban de `rightArm`/`leftArm`.
- Antes salían dos pares de brazos: faltaba la `part_visibility` vanilla en los render controllers propios.
- Skins 2, 3, 4, 19 y 20 no pintaban los brazos cruzados: arreglado en d4a47a1 (copiados de los sueltos).

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/vindicator.entity.json` (vanilla `vindicator.entity.json`)
- Render controller `controller.render.mv.vindicator` (RP/render_controllers/vindicator.render_controllers.json)
- Render controller `controller.render.mv.vindicator_armor` (RP/render_controllers/vindicator.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.vindicator_armor` → `geometry.mv.vindicator_armor` (RP/models/entity/vindicator_armor.geo.json, 16 cubos; cuelga de: body, head, leftArm, leg0, leg1, rightArm): `vindicator/vindicator_armor`, `vindicator/vindicator_armor2`, `vindicator/vindicator_armor3`
- `controller.render.mv.vindicator_armor` → `geometry.mv.vindicator_armor2` (RP/models/entity/vindicator_armor2.geo.json, 15 cubos; cuelga de: body, leftArm, rightArm): `vindicator/vindicator_armor4`

### BP

- Archivo: `BP/entities/vindicator.json`
- `mv:variant` [0, 21]: valor:peso 1:1000 2:1000 3:1000 4:1000 5:1000 6:1000 7:1000 8:1000 9:1000 10:1000 11:1000 12:1000 13:1000 14:1000 15:1000 16:1000 17:1000 18:1000 19:1000 20:1000 21:5 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 4]: valor:peso 0:60 1:10 2:10 3:10 4:10 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
