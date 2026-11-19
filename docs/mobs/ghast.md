# ghast

En la base: 13 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/ghast.entity.json` sobre la vanilla `ghast.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.ghast` (RP/render_controllers/ghast.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/ghast.json`, `mv:variant` [0, 13], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 13)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/ghast/ghast` (vanilla) | 1 (7.7%) |  |
| 2 | `mv_default2` | `textures/entity/ghast/ghast2` (pack) | 1 (7.7%) |  |
| 3 | `mv_default3` | `textures/entity/ghast/ghast3` (pack) | 1 (7.7%) |  |
| 4 | `mv_default4` | `textures/entity/ghast/ghast4` (pack) | 1 (7.7%) |  |
| 5 | `mv_default5` | `textures/entity/ghast/ghast5` (pack) | 1 (7.7%) |  |
| 6 | `mv_default6` | `textures/entity/ghast/ghast6` (pack) | 1 (7.7%) |  |
| 7 | `mv_default7` | `textures/entity/ghast/ghast7` (pack) | 1 (7.7%) | tentacles_4 56%, tentacles_8 56% |
| 8 | `mv_default8` | `textures/entity/ghast/ghast8` (pack) | 1 (7.7%) |  |
| 9 | `mv_default9` | `textures/entity/ghast/ghast9` (pack) | 1 (7.7%) |  |
| 10 | `mv_default10` | `textures/entity/ghast/ghast10` (pack) | 1 (7.7%) |  |
| 11 | `mv_default11` | `textures/entity/ghast/ghast11` (pack) | 1 (7.7%) |  |
| 12 | `mv_default12` | `textures/entity/ghast/ghast12` (pack) | 1 (7.7%) |  |
| 13 | `mv_default13` | `textures/entity/ghast/ghast13` (pack) | 1 (7.7%) |  |

### `array.mv_charging` (disparando, 13)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_charging` | `textures/entity/ghast/ghast_shooting` (vanilla) | 1 (7.7%) |  |
| 2 | `mv_charging2` | `textures/entity/ghast/ghast2s` (pack) | 1 (7.7%) |  |
| 3 | `mv_charging3` | `textures/entity/ghast/ghast3s` (pack) | 1 (7.7%) |  |
| 4 | `mv_charging4` | `textures/entity/ghast/ghast4s` (pack) | 1 (7.7%) |  |
| 5 | `mv_charging5` | `textures/entity/ghast/ghast5s` (pack) | 1 (7.7%) |  |
| 6 | `mv_charging6` | `textures/entity/ghast/ghast6s` (pack) | 1 (7.7%) |  |
| 7 | `mv_charging7` | `textures/entity/ghast/ghast7s` (pack) | 1 (7.7%) |  |
| 8 | `mv_charging8` | `textures/entity/ghast/ghast8s` (pack) | 1 (7.7%) |  |
| 9 | `mv_charging9` | `textures/entity/ghast/ghast9s` (pack) | 1 (7.7%) |  |
| 10 | `mv_charging10` | `textures/entity/ghast/ghast10s` (pack) | 1 (7.7%) |  |
| 11 | `mv_charging11` | `textures/entity/ghast/ghast11s` (pack) | 1 (7.7%) |  |
| 12 | `mv_charging12` | `textures/entity/ghast/ghast12s` (pack) | 1 (7.7%) |  |
| 13 | `mv_charging13` | `textures/entity/ghast/ghast13s` (pack) | 1 (7.7%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/ghast.entity.json` (vanilla `ghast.entity.json`)
- Render controller `controller.render.mv.ghast` (RP/render_controllers/ghast.render_controllers.json)

### BP

- Archivo: `BP/entities/ghast.json`
- `mv:variant` [0, 13]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 10:1 11:1 12:1 13:1 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
