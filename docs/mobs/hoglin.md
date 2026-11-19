# hoglin

En la base: 11 skins sobre el modelo vanilla, puerta `!q.is_baby`; BP con `mv:variant` (sorteo en entity_spawned, entity_born).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/hoglin.entity.json` sobre la vanilla `hoglin.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby);`
- Render controller: `controller.render.mv.hoglin` (RP/render_controllers/hoglin.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/hoglin.json`, `mv:variant` [0, 11], sorteo en: minecraft:entity_born, minecraft:entity_spawned

### `array.mv_skins` (skins, 11)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/hoglin/hoglin` (vanilla) | 1 (9.1%) |  |
| 2 | `mv_default2` | `textures/entity/hoglin/hoglin2` (pack) | 1 (9.1%) |  |
| 3 | `mv_default3` | `textures/entity/hoglin/hoglin3` (pack) | 1 (9.1%) |  |
| 4 | `mv_default4` | `textures/entity/hoglin/hoglin4` (pack) | 1 (9.1%) |  |
| 5 | `mv_default5` | `textures/entity/hoglin/hoglin5` (pack) | 1 (9.1%) |  |
| 6 | `mv_default6` | `textures/entity/hoglin/hoglin6` (pack) | 1 (9.1%) |  |
| 7 | `mv_default7` | `textures/entity/hoglin/hoglin7` (pack) | 1 (9.1%) |  |
| 8 | `mv_default8` | `textures/entity/hoglin/hoglin8` (pack) | 1 (9.1%) |  |
| 9 | `mv_default9` | `textures/entity/hoglin/hoglin9` (pack) | 1 (9.1%) |  |
| 10 | `mv_default10` | `textures/entity/hoglin/hoglin10` (pack) | 1 (9.1%) |  |
| 11 | `mv_default11` | `textures/entity/hoglin/hoglin11` (pack) | 1 (9.1%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/hoglin.entity.json` (vanilla `hoglin.entity.json`)
- Render controller `controller.render.hoglin.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.hoglin` si `v.mv_active` (RP/render_controllers/hoglin.render_controllers.json)
- Render controller `controller.render.mv.hoglin_piglinhead` si `v.mv_active` (RP/render_controllers/hoglin.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.hoglin_piglinhead` → `geometry.mv.hoglin_piglinhead` (RP/models/entity/hoglin_piglinhead.geo.json, 7 cubos; cuelga de: body, head): `skeleton/piglin_heads`
- `controller.render.mv.hoglin_piglinhead` → `geometry.mv.hoglin_piglinhead2` (RP/models/entity/hoglin_piglinhead2.geo.json, 6 cubos; cuelga de: body, head): `skeleton/piglin_heads`
- `controller.render.mv.hoglin_piglinhead` → `geometry.mv.hoglin_wither_skull` (RP/models/entity/hoglin_wither_skull.geo.json, 2 cubos; cuelga de: body, head, wither_skeleton_head): `skeleton/piglin_heads`

### BP

- Archivo: `BP/entities/hoglin.json`
- `mv:variant` [0, 11]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 10:1 11:1 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 3]: valor:peso 0:1 1:1 2:1 3:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
