# warden

En la base: 6 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/warden.entity.json` sobre la vanilla `warden.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.warden` (RP/render_controllers/warden.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/warden.json`, `mv:variant` [0, 6], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 6)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/warden/warden` (vanilla) | 1 (16.7%) |  |
| 2 | `mv_default2` | `textures/entity/warden/warden2` (pack) | 1 (16.7%) |  |
| 3 | `mv_default3` | `textures/entity/warden/warden3` (pack) | 1 (16.7%) |  |
| 4 | `mv_default4` | `textures/entity/warden/warden4` (pack) | 1 (16.7%) |  |
| 5 | `mv_default5` | `textures/entity/warden/warden5` (pack) | 1 (16.7%) |  |
| 6 | `mv_default6` | `textures/entity/warden/warden6` (pack) | 1 (16.7%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/warden.entity.json` (vanilla `warden.entity.json`)
- Render controller `controller.render.mv.warden` (RP/render_controllers/warden.render_controllers.json)
- Render controller `controller.render.mv.warden_bioluminescent_layer` (RP/render_controllers/warden.render_controllers.json)
- Render controller `controller.render.mv.warden_spots_1` (RP/render_controllers/warden.render_controllers.json)
- Render controller `controller.render.mv.warden_spots_2` (RP/render_controllers/warden.render_controllers.json)
- Render controller `controller.render.mv.warden_tendrils` (RP/render_controllers/warden.render_controllers.json)
- Render controller `controller.render.mv.warden_heart` (RP/render_controllers/warden.render_controllers.json)

### BP

- Archivo: `BP/entities/warden.json`
- `mv:variant` [0, 6]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
