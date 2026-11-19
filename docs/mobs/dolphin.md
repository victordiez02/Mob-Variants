# dolphin

En la base: 7 skins sobre el modelo vanilla, puerta `!q.is_baby`; BP con `mv:variant` (sorteo en entity_spawned, entity_born).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/dolphin.entity.json` sobre la vanilla `dolphin.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby);`
- Render controller: `controller.render.mv.dolphin` (RP/render_controllers/dolphin.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/dolphin.json`, `mv:variant` [0, 7], sorteo en: minecraft:entity_born, minecraft:entity_spawned

### `array.mv_skins` (skins, 7)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/dolphin` (vanilla) | 1 (14.3%) |  |
| 2 | `mv_default2` | `textures/entity/dolphin/dolphin2` (pack) | 1 (14.3%) | a propósito (back_fin 0%) |
| 3 | `mv_default3` | `textures/entity/dolphin/dolphin3` (pack) | 1 (14.3%) | a propósito (nose 0%) |
| 4 | `mv_default4` | `textures/entity/dolphin/dolphin4` (pack) | 1 (14.3%) |  |
| 5 | `mv_default5` | `textures/entity/dolphin/dolphin5` (pack) | 1 (14.3%) | a propósito (nose 0%) |
| 6 | `mv_default6` | `textures/entity/dolphin/dolphin6` (pack) | 1 (14.3%) |  |
| 7 | `mv_default7` | `textures/entity/dolphin/dolphin7` (pack) | 1 (14.3%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- Revisadas (a propósito): `dolphin2`, `dolphin3`, `dolphin5` (narval sin aleta dorsal; ballena y orca sin
  nariz de delfín). Render con `--view all` el 19-11-2026.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/dolphin.entity.json` (vanilla `dolphin.entity.json`)
- Render controller `controller.render.dolphin.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.dolphin` si `v.mv_active` (RP/render_controllers/dolphin.render_controllers.json)

### BP

- Archivo: `BP/entities/dolphin.json`
- `mv:variant` [0, 7]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
