# blaze

En la base: 8 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/blaze.entity.json` sobre la vanilla `blaze.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.blaze` (RP/render_controllers/blaze.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/blaze.json`, `mv:variant` [0, 8], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 8)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/blaze` (vanilla) | 1 (12.5%) |  |
| 2 | `mv_default2` | `textures/entity/blaze/blaze2` (pack) | 1 (12.5%) |  |
| 3 | `mv_default3` | `textures/entity/blaze/blaze3` (pack) | 1 (12.5%) |  |
| 4 | `mv_default4` | `textures/entity/blaze/blaze4` (pack) | 1 (12.5%) |  |
| 5 | `mv_default5` | `textures/entity/blaze/blaze5` (pack) | 1 (12.5%) |  |
| 6 | `mv_default6` | `textures/entity/blaze/blaze6` (pack) | 1 (12.5%) |  |
| 7 | `mv_default7` | `textures/entity/blaze/blaze7` (pack) | 1 (12.5%) | upperBodyParts0 57%, upperBodyParts1 57%, upperBodyParts2 57%, upperBodyParts3 57%, upperBodyParts4 57%, upperBodyParts5 57%, upperBodyParts6 57%, upperBodyParts7 57%, upperBodyParts8 57%, upperBodyParts9 57%, upperBodyParts10 57%, upperBodyParts11 57% |
| 8 | `mv_default8` | `textures/entity/blaze/blaze8` (pack) | 1 (12.5%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/blaze.entity.json` (vanilla `blaze.entity.json`)
- Render controller `controller.render.mv.blaze` (RP/render_controllers/blaze.render_controllers.json)

### BP

- Archivo: `BP/entities/blaze.json`
- `mv:variant` [0, 8]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
