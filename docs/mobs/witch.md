# witch

En la base: 9 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/witch.entity.json` sobre la vanilla `witch.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.witch` (RP/render_controllers/witch.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/witch.json`, `mv:variant` [0, 9], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 9)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/witch/witch` (pack) | 1 (11.1%) | hat2 53%, hat3 45% |
| 2 | `mv_default2` | `textures/entity/witch/witch2` (pack) | 1 (11.1%) | hat2 53%, hat3 45% |
| 3 | `mv_default3` | `textures/entity/witch/witch3` (pack) | 1 (11.1%) | hat2 53%, hat3 45% |
| 4 | `mv_default4` | `textures/entity/witch/witch4` (pack) | 1 (11.1%) | hat2 53%, hat3 45% |
| 5 | `mv_default5` | `textures/entity/witch/witch5` (pack) | 1 (11.1%) | hat2 53%, hat3 45% |
| 6 | `mv_default6` | `textures/entity/witch/witch6` (pack) | 1 (11.1%) | hat2 53%, hat3 45% |
| 7 | `mv_default7` | `textures/entity/witch/witch7` (pack) | 1 (11.1%) | hat2 53% |
| 8 | `mv_default8` | `textures/entity/witch/witch8` (pack) | 1 (11.1%) | hat2 53%, hat3 45% |
| 9 | `mv_default9` | `textures/entity/witch/witch9` (pack) | 1 (11.1%) | hat2 53%, hat3 45% |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- Las skins solo pintan en parte el sombrero vanilla (`hat2` 53 %, `hat3` 45 %): antes el sombrero era una capa (`witch_extras`) y el vanilla estaba oculto. En la base se ve el vanilla con su textura: revisar.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/witch.entity.json` (vanilla `witch.entity.json`)
- Render controller `controller.render.mv.witch` (RP/render_controllers/witch.render_controllers.json)
- Render controller `controller.render.mv.witch_extras` (RP/render_controllers/witch.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.witch_extras` → `geometry.mv.witch_extras` (RP/models/entity/witch_extras.geo.json, 25 cubos; cuelga de: body, head, leg0, leg1): 9 texturas (las skins del cuerpo: `witch/witch`, … )

### BP

- Archivo: `BP/entities/witch.json`
- `mv:variant` [0, 9]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
