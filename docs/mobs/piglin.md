# piglin

En la base: 13 skins sobre el modelo vanilla, puerta `!q.is_baby`; BP con `mv:variant` (sorteo en entity_spawned, entity_born).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/piglin.entity.json` sobre la vanilla `piglin.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby);`
- Render controller: `controller.render.mv.piglin` (RP/render_controllers/piglin.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/piglin.json`, `mv:variant` [0, 13], sorteo en: minecraft:entity_born, minecraft:entity_spawned

### `array.mv_skins` (skins, 13)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/piglin/piglin` (vanilla) | 1 (7.7%) |  |
| 2 | `mv_default2` | `textures/entity/piglin/piglin2` (pack) | 1 (7.7%) |  |
| 3 | `mv_default3` | `textures/entity/piglin/piglin3` (pack) | 1 (7.7%) |  |
| 4 | `mv_default4` | `textures/entity/piglin/piglin4` (pack) | 1 (7.7%) | leftear 57%, rightear 0% |
| 5 | `mv_default5` | `textures/entity/piglin/piglin5` (pack) | 1 (7.7%) |  |
| 6 | `mv_default6` | `textures/entity/piglin/piglin6` (pack) | 1 (7.7%) | leftear 57%, rightear 0% |
| 7 | `mv_default7` | `textures/entity/piglin/piglin7` (pack) | 1 (7.7%) | rightear 52% |
| 8 | `mv_default8` | `textures/entity/piglin/piglin8` (pack) | 1 (7.7%) | rightear 0% |
| 9 | `mv_default9` | `textures/entity/piglin/piglin9` (pack) | 1 (7.7%) |  |
| 10 | `mv_default10` | `textures/entity/piglin/piglin10` (pack) | 1 (7.7%) | leftear 31%, rightear 0% |
| 11 | `mv_default11` | `textures/entity/piglin/piglin11` (pack) | 1 (7.7%) |  |
| 12 | `mv_default12` | `textures/entity/piglin/piglin12` (pack) | 1 (7.7%) |  |
| 13 | `mv_default13` | `textures/entity/piglin/piglin13` (pack) | 1 (7.7%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/piglin.entity.json` (vanilla `piglin.entity.json`)
- Render controller `controller.render.piglin.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.piglin` si `v.mv_active` (RP/render_controllers/piglin.render_controllers.json)

### BP

- Archivo: `BP/entities/piglin.json`
- `mv:mark_variant` [0, 13]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 10:1 11:1 12:1 13:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
