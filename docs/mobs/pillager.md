# pillager

En la base: 23 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/pillager.entity.json` sobre la vanilla `pillager.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.pillager` (RP/render_controllers/pillager.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/pillager.json`, `mv:variant` [0, 23], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 23)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/pillager` (vanilla) | 100 (4.5%) |  |
| 2 | `mv_default2` | `textures/entity/pillager/pillager2` (pack) | 100 (4.5%) |  |
| 3 | `mv_default3` | `textures/entity/pillager/pillager3` (pack) | 100 (4.5%) |  |
| 4 | `mv_default4` | `textures/entity/pillager/pillager4` (pack) | 100 (4.5%) |  |
| 5 | `mv_default5` | `textures/entity/pillager/pillager5` (pack) | 100 (4.5%) |  |
| 6 | `mv_default6` | `textures/entity/pillager/pillager6` (pack) | 100 (4.5%) |  |
| 7 | `mv_default7` | `textures/entity/pillager/pillager7` (pack) | 100 (4.5%) |  |
| 8 | `mv_default8` | `textures/entity/pillager/pillager8` (pack) | 100 (4.5%) |  |
| 9 | `mv_default9` | `textures/entity/pillager/pillager9` (pack) | 100 (4.5%) |  |
| 10 | `mv_default10` | `textures/entity/pillager/pillager10` (pack) | 100 (4.5%) |  |
| 11 | `mv_default11` | `textures/entity/pillager/pillager11` (pack) | 100 (4.5%) |  |
| 12 | `mv_default12` | `textures/entity/pillager/pillager12` (pack) | 100 (4.5%) |  |
| 13 | `mv_default13` | `textures/entity/pillager/pillager13` (pack) | 100 (4.5%) |  |
| 14 | `mv_default14` | `textures/entity/pillager/pillager14` (pack) | 100 (4.5%) |  |
| 15 | `mv_default15` | `textures/entity/pillager/pillager15` (pack) | 100 (4.5%) |  |
| 16 | `mv_default16` | `textures/entity/pillager/pillager16` (pack) | 100 (4.5%) |  |
| 17 | `mv_default17` | `textures/entity/pillager/pillager17` (pack) | 100 (4.5%) |  |
| 18 | `mv_default18` | `textures/entity/pillager/pillager18` (pack) | 100 (4.5%) |  |
| 19 | `mv_default19` | `textures/entity/pillager/pillager19` (pack) | 100 (4.5%) |  |
| 20 | `mv_default20` | `textures/entity/pillager/pillager20` (pack) | 100 (4.5%) |  |
| 21 | `mv_default21` | `textures/entity/pillager/pillager21` (pack) | 100 (4.5%) |  |
| 22 | `mv_default22` | `textures/entity/pillager/pillager22` (pack) | 100 (4.5%) |  |
| 23 | `mv_default23` | `textures/entity/pillager/pillager_totem` (pack) | 2 (0.1%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- En el juego (con la capa de casco): la ballesta sí se veía.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/pillager.entity.json` (vanilla `pillager.entity.json`)
- Render controller `controller.render.mv.pillager` (RP/render_controllers/pillager.render_controllers.json)
- Render controller `controller.render.mv.pillager_helmet` (RP/render_controllers/pillager.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.pillager_helmet` → `geometry.mv.pillager_helmet` (RP/models/entity/pillager_helmet.geo.json, 4 cubos; cuelga de: body, head, waist): `pillager/helmet_d`, `pillager/helmet_g`, `pillager/helmet_r`

### BP

- Archivo: `BP/entities/pillager.json`
- `mv:variant` [0, 23]: valor:peso 1:100 2:100 3:100 4:100 5:100 6:100 7:100 8:100 9:100 10:100 11:100 12:100 13:100 14:100 15:100 16:100 17:100 18:100 19:100 20:100 21:100 22:100 23:2 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 4]: valor:peso 0:6 1:1 2:1 3:1 4:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
