# zombie_villager_v2

En la base: 9 skins sobre el modelo vanilla, puerta `!q.is_baby`; BP con `mv:variant` (sorteo en entity_spawned, entity_born, entity_transformed).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/zombie_villager_v2.entity.json` sobre la vanilla `zombie_villager_v2.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby);`
- Render controller: `controller.render.mv.zombie_villager_v2` (RP/render_controllers/zombie_villager_v2.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/zombie_villager_v2.json`, `mv:variant` [0, 9], sorteo en: minecraft:entity_born, minecraft:entity_spawned, minecraft:entity_transformed

### `array.mv_skins` (skins, 9)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/zombie_villager2/zombie-villager` (vanilla) | 1 (11.1%) |  |
| 2 | `mv_default2` | `textures/entity/zombie_villager2/zombie-villager2` (pack) | 1 (11.1%) |  |
| 3 | `mv_default3` | `textures/entity/zombie_villager2/zombie-villager3` (pack) | 1 (11.1%) |  |
| 4 | `mv_default4` | `textures/entity/zombie_villager2/zombie-villager4` (pack) | 1 (11.1%) |  |
| 5 | `mv_default5` | `textures/entity/zombie_villager2/zombie-villager5` (pack) | 1 (11.1%) |  |
| 6 | `mv_default6` | `textures/entity/zombie_villager2/zombie-villager6` (pack) | 1 (11.1%) |  |
| 7 | `mv_default7` | `textures/entity/zombie_villager2/zombie-villager7` (pack) | 1 (11.1%) |  |
| 8 | `mv_default8` | `textures/entity/zombie_villager2/zombie-villager8` (pack) | 1 (11.1%) |  |
| 9 | `mv_default9` | `textures/entity/zombie_villager2/zombie-villager9` (pack) | 1 (11.1%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/zombie_villager_v2.entity.json` (vanilla `zombie_villager_v2.entity.json`)
- Render controller `controller.render.zombie_villager_v3_base` si `!v.mv_active` (vanilla)
- Render controller `controller.render.zombie_villager_v3_masked` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.zombie_villager_v2_base` si `v.mv_active` (RP/render_controllers/zombie_villager_v2.render_controllers.json)
- Render controller `controller.render.mv.zombie_villager_v2_masked` si `v.mv_active` (RP/render_controllers/zombie_villager_v2.render_controllers.json)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
