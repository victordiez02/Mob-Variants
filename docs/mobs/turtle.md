# turtle

En la base: 6 skins sobre el modelo vanilla, puerta `!q.is_baby`; BP con `mv:variant` (sorteo en entity_spawned, entity_born).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/turtle.entity.json` sobre la vanilla `turtle.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby);`
- Render controller: `controller.render.mv.turtle` (RP/render_controllers/turtle.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/turtle.json`, `mv:variant` [0, 6], sorteo en: minecraft:entity_born, minecraft:entity_spawned

### `array.mv_skins` (skins, 6)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/sea_turtle` (vanilla) | 80 (80.0%) |  |
| 2 | `mv_default2` | `textures/entity/sea_turtle/donatello` (pack) | 4 (4.0%) |  |
| 3 | `mv_default3` | `textures/entity/sea_turtle/leonardo` (pack) | 4 (4.0%) |  |
| 4 | `mv_default4` | `textures/entity/sea_turtle/michelangelo` (pack) | 4 (4.0%) |  |
| 5 | `mv_default5` | `textures/entity/sea_turtle/raphael` (pack) | 4 (4.0%) |  |
| 6 | `mv_default6` | `textures/entity/sea_turtle/squirtle` (pack) | 4 (4.0%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/turtle.entity.json` (vanilla `turtle.entity.json`)
- Render controller `controller.render.turtle.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.turtle` si `v.mv_active` (RP/render_controllers/turtle.render_controllers.json)

### BP

- Archivo: `BP/entities/turtle.json`
- `mv:variant` [0, 6]: valor:peso 1:80 2:4 3:4 4:4 5:4 6:4 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
