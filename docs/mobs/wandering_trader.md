# wandering_trader

En la base: 9 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/wandering_trader.entity.json` sobre la vanilla `wandering_trader.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.wandering_trader` (RP/render_controllers/wandering_trader.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/wandering_trader.json`, `mv:variant` [0, 9], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 9)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/wandering_trader` (vanilla) | 1 (11.1%) |  |
| 2 | `mv_default2` | `textures/entity/villager2/wandering_trader/wandering_trader2` (pack) | 1 (11.1%) |  |
| 3 | `mv_default3` | `textures/entity/villager2/wandering_trader/wandering_trader3` (pack) | 1 (11.1%) |  |
| 4 | `mv_default4` | `textures/entity/villager2/wandering_trader/wandering_trader4` (pack) | 1 (11.1%) |  |
| 5 | `mv_default5` | `textures/entity/villager2/wandering_trader/wandering_trader5` (pack) | 1 (11.1%) |  |
| 6 | `mv_default6` | `textures/entity/villager2/wandering_trader/wandering_trader6` (pack) | 1 (11.1%) |  |
| 7 | `mv_default7` | `textures/entity/villager2/wandering_trader/wandering_trader7` (pack) | 1 (11.1%) |  |
| 8 | `mv_default8` | `textures/entity/villager2/wandering_trader/wandering_trader8` (pack) | 1 (11.1%) |  |
| 9 | `mv_default9` | `textures/entity/villager2/wandering_trader/wandering_trader9` (pack) | 1 (11.1%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/wandering_trader.entity.json` (vanilla `wandering_trader.entity.json`)
- Render controller `controller.render.mv.wandering_trader` (RP/render_controllers/wandering_trader.render_controllers.json)
- Render controller `controller.render.mv.wandering_trader_backpack` (RP/render_controllers/wandering_trader.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.wandering_trader_backpack` → `geometry.mv.wandering_trader_backpack` (RP/models/entity/wandering_trader_backpack.geo.json, 16 cubos; cuelga de: body): `skeleton/backpack`

### BP

- Archivo: `BP/entities/wandering_trader.json`
- `mv:variant` [0, 9]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
