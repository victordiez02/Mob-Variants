# sniffer

En la base: 9 skins sobre el modelo vanilla, puerta `!q.is_baby`; BP con `mv:variant` (sorteo en entity_spawned, entity_born).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/sniffer.entity.json` sobre la vanilla `sniffer.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby);`
- Render controller: `controller.render.mv.sniffer` (RP/render_controllers/sniffer.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/sniffer.json`, `mv:variant` [0, 9], sorteo en: minecraft:entity_born, minecraft:entity_spawned

### `array.mv_skins` (skins, 9)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/sniffer/sniffer` (pack) | 1 (11.1%) |  |
| 2 | `mv_default2` | `textures/entity/sniffer/sniffer2` (pack) | 1 (11.1%) |  |
| 3 | `mv_default3` | `textures/entity/sniffer/sniffer3` (pack) | 1 (11.1%) |  |
| 4 | `mv_default4` | `textures/entity/sniffer/sniffer4` (pack) | 1 (11.1%) | left_ear 31%, right_ear 22% |
| 5 | `mv_default5` | `textures/entity/sniffer/sniffer5` (pack) | 1 (11.1%) |  |
| 6 | `mv_default6` | `textures/entity/sniffer/sniffer6` (pack) | 1 (11.1%) |  |
| 7 | `mv_default7` | `textures/entity/sniffer/sniffer7` (pack) | 1 (11.1%) |  |
| 8 | `mv_default8` | `textures/entity/sniffer/sniffer8` (pack) | 1 (11.1%) |  |
| 9 | `mv_default9` | `textures/entity/sniffer/sniffer9` (pack) | 1 (11.1%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/sniffer.entity.json` (vanilla `sniffer.entity.json`)
- Render controller `controller.render.sniffer.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.sniffer` si `v.mv_active` (RP/render_controllers/sniffer.render_controllers.json)
- Render controller `controller.render.mv.sniffer_flower` si `v.mv_active` (RP/render_controllers/sniffer.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.sniffer_flower` → `geometry.mv.sniffer_torchflower` (RP/models/entity/sniffer_torchflower.geo.json, 2 cubos; cuelga de: body, bone, head): `sniffer/sniffer`, `sniffer/sniffer9`
- `controller.render.mv.sniffer_flower` → `geometry.mv.sniffer_pitchflower` (RP/models/entity/sniffer_pitchflower.geo.json, 4 cubos; cuelga de: body, bone, flower, head, pitchFlower): `sniffer/sniffer`

### BP

- Archivo: `BP/entities/sniffer.json`
- `mv:variant` [0, 9]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 7]: valor:peso 0:50 1:30 4:20 (en minecraft:entity_spawned)
- Grupos propios: mv:torchflower_change_1to2, mv:torchflower_change_2to3, mv:pitchflower_change_1to2, mv:pitchflower_change_2to3, mv:pitchflower_change_3to4; eventos propios: mv:pitchflower_change_1to2_event, mv:torchflower_change_1to2_event, mv:torchflower_change_2to3_event, mv:pitchflower_change_2to3_event, mv:pitchflower_change_3to4_event

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
