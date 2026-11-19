# enderman

En la base: 26 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/enderman.entity.json` sobre la vanilla `enderman.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.enderman` (RP/render_controllers/enderman.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/enderman.json`, `mv:variant` [0, 26], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 26)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/enderman/enderman` (vanilla) | 1 (3.8%) |  |
| 2 | `mv_default2` | `textures/entity/enderman/enderman2` (pack) | 1 (3.8%) |  |
| 3 | `mv_default3` | `textures/entity/enderman/enderman3` (pack) | 1 (3.8%) |  |
| 4 | `mv_default4` | `textures/entity/enderman/enderman4` (pack) | 1 (3.8%) |  |
| 5 | `mv_default5` | `textures/entity/enderman/enderman5` (pack) | 1 (3.8%) |  |
| 6 | `mv_default6` | `textures/entity/enderman/enderman6` (pack) | 1 (3.8%) |  |
| 7 | `mv_default7` | `textures/entity/enderman/enderman7` (pack) | 1 (3.8%) |  |
| 8 | `mv_default8` | `textures/entity/enderman/enderman8` (pack) | 1 (3.8%) | body 47% |
| 9 | `mv_default9` | `textures/entity/enderman/enderman9` (pack) | 1 (3.8%) |  |
| 10 | `mv_default10` | `textures/entity/enderman/enderman10` (pack) | 1 (3.8%) |  |
| 11 | `mv_default11` | `textures/entity/enderman/enderman11` (pack) | 1 (3.8%) |  |
| 12 | `mv_default12` | `textures/entity/enderman/enderman12` (pack) | 1 (3.8%) |  |
| 13 | `mv_default13` | `textures/entity/enderman/enderman13` (pack) | 1 (3.8%) | rightArm 56%, leftArm 56%, rightLeg 56%, leftLeg 56% |
| 14 | `mv_default14` | `textures/entity/enderman/enderman14` (pack) | 1 (3.8%) |  |
| 15 | `mv_default15` | `textures/entity/enderman/enderman15` (pack) | 1 (3.8%) |  |
| 16 | `mv_default16` | `textures/entity/enderman/enderman16` (pack) | 1 (3.8%) |  |
| 17 | `mv_default17` | `textures/entity/enderman/enderman17` (pack) | 1 (3.8%) |  |
| 18 | `mv_default18` | `textures/entity/enderman/enderman18` (pack) | 1 (3.8%) |  |
| 19 | `mv_default19` | `textures/entity/enderman/enderman19` (pack) | 1 (3.8%) |  |
| 20 | `mv_default20` | `textures/entity/enderman/enderman20` (pack) | 1 (3.8%) |  |
| 21 | `mv_default21` | `textures/entity/enderman/enderman21` (pack) | 1 (3.8%) |  |
| 22 | `mv_default22` | `textures/entity/enderman/enderman22` (pack) | 1 (3.8%) |  |
| 23 | `mv_default23` | `textures/entity/enderman/enderman23` (pack) | 1 (3.8%) |  |
| 24 | `mv_default24` | `textures/entity/enderman/enderman24` (pack) | 1 (3.8%) |  |
| 25 | `mv_default25` | `textures/entity/enderman/enderman25` (pack) | 1 (3.8%) |  |
| 26 | `mv_default26` | `textures/entity/enderman/enderman26` (pack) | 1 (3.8%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- Aplazado por el usuario (recordárselo): dientes y lengua al enfadarse. Propuesta: pintarlos en la zona `hat` (UV 0,16) de cada skin con `enderman_jaw.png`, sin geometría.
- Tenía sonidos propios en `RP/sounds/mob/endermen/` (ruta vanilla): quitados de la base.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/enderman.entity.json` (vanilla `enderman.entity.json`)
- Render controller `controller.render.mv.enderman` (RP/render_controllers/enderman.render_controllers.json)

### BP

- Archivo: `BP/entities/enderman.json`
- `mv:variant` [0, 26]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 10:1 11:1 12:1 13:1 14:1 15:1 16:1 17:1 18:1 19:1 20:1 21:1 22:1 23:1 24:1 25:1 26:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
