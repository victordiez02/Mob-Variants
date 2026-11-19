# ender_dragon

En la base: 7 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/ender_dragon.entity.json` sobre la vanilla `ender_dragon.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.ender_dragon` (RP/render_controllers/ender_dragon.render_controllers.json) con condición `(query.death_ticks <= 1.0) && v.mv_active`
- BP: `BP/entities/ender_dragon.json`, `mv:variant` [0, 7], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 7)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/dragon/dragon` (vanilla) | 1 (14.3%) |  |
| 2 | `mv_default2` | `textures/entity/dragon/dragon2` (pack) | 1 (14.3%) |  |
| 3 | `mv_default3` | `textures/entity/dragon/dragon3` (pack) | 1 (14.3%) |  |
| 4 | `mv_default4` | `textures/entity/dragon/dragon4` (pack) | 1 (14.3%) |  |
| 5 | `mv_default5` | `textures/entity/dragon/dragon5` (pack) | 1 (14.3%) |  |
| 6 | `mv_default6` | `textures/entity/dragon/dragon6` (pack) | 1 (14.3%) | wing 47%, wing1 47% |
| 7 | `mv_default7` | `textures/entity/dragon/dragon7` (pack) | 1 (14.3%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/ender_dragon.entity.json` (vanilla `ender_dragon.entity.json`)
- Render controller `controller.render.mv.ender_dragon_death_pre_pass` si `query.death_ticks > 1.0` (RP/render_controllers/ender_dragon.render_controllers.json)
- Render controller `controller.render.mv.ender_dragon_death_main_pass` si `query.death_ticks > 1.0` (RP/render_controllers/ender_dragon.render_controllers.json)
- Render controller `controller.render.mv.ender_dragon_default` si `query.death_ticks <= 1.0` (RP/render_controllers/ender_dragon.render_controllers.json)

### BP

- Archivo: `BP/entities/ender_dragon.json`
- `mv:variant` [0, 7]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
