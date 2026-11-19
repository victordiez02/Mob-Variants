# spider

En la base: 25 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/spider.entity.json` sobre la vanilla `spider.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.spider` (RP/render_controllers/spider.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/spider.json`, `mv:variant` [0, 25], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 25)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/spider/spider` (pack) | 1 (4.0%) |  |
| 2 | `mv_default2` | `textures/entity/spider/spider2` (pack) | 1 (4.0%) |  |
| 3 | `mv_default3` | `textures/entity/spider/spider3` (pack) | 1 (4.0%) |  |
| 4 | `mv_default4` | `textures/entity/spider/spider4` (pack) | 1 (4.0%) |  |
| 5 | `mv_default5` | `textures/entity/spider/spider5` (pack) | 1 (4.0%) |  |
| 6 | `mv_default6` | `textures/entity/spider/spider6` (pack) | 1 (4.0%) |  |
| 7 | `mv_default7` | `textures/entity/spider/spider7` (pack) | 1 (4.0%) |  |
| 8 | `mv_default8` | `textures/entity/spider/spider8` (pack) | 1 (4.0%) |  |
| 9 | `mv_default9` | `textures/entity/spider/spider9` (pack) | 1 (4.0%) |  |
| 10 | `mv_default10` | `textures/entity/spider/spider10` (pack) | 1 (4.0%) |  |
| 11 | `mv_default11` | `textures/entity/spider/spider11` (pack) | 1 (4.0%) |  |
| 12 | `mv_default12` | `textures/entity/spider/spider12` (pack) | 1 (4.0%) |  |
| 13 | `mv_default13` | `textures/entity/spider/spider13` (pack) | 1 (4.0%) |  |
| 14 | `mv_default14` | `textures/entity/spider/spider14` (pack) | 1 (4.0%) |  |
| 15 | `mv_default15` | `textures/entity/spider/spider15` (pack) | 1 (4.0%) |  |
| 16 | `mv_default16` | `textures/entity/spider/spider17` (pack) | 1 (4.0%) |  |
| 17 | `mv_default17` | `textures/entity/spider/spider18` (pack) | 1 (4.0%) |  |
| 18 | `mv_default18` | `textures/entity/spider/spider19` (pack) | 1 (4.0%) | head 35%, leg0 44%, leg1 44%, leg2 44%, leg3 44%, leg4 44%, leg5 44%, leg6 44%, leg7 44% |
| 19 | `mv_default19` | `textures/entity/spider/spider20` (pack) | 1 (4.0%) |  |
| 20 | `mv_default20` | `textures/entity/spider/spider21` (pack) | 1 (4.0%) |  |
| 21 | `mv_default21` | `textures/entity/spider/spider22` (pack) | 1 (4.0%) |  |
| 22 | `mv_default22` | `textures/entity/spider/spider23` (pack) | 1 (4.0%) |  |
| 23 | `mv_default23` | `textures/entity/spider/spider24` (pack) | 1 (4.0%) |  |
| 24 | `mv_default24` | `textures/entity/spider/spider25` (pack) | 1 (4.0%) |  |
| 25 | `mv_default25` | `textures/entity/spider/spider26` (pack) | 1 (4.0%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/spider.entity.json` (vanilla `spider.entity.json`)
- Render controller `controller.render.mv.spider` (RP/render_controllers/spider.render_controllers.json)
- Render controller `controller.render.mv.spider_fangs` (RP/render_controllers/spider.render_controllers.json)
- Render controller `controller.render.mv.spider_giant_legs` si `v.mv_giant` (RP/render_controllers/spider.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.spider_fangs` → `geometry.mv.spider_fangs` (RP/models/entity/spider_fangs.geo.json, 2 cubos; cuelga de: body0, head): 26 texturas (las skins del cuerpo: `spider/spider`, … )
- `controller.render.mv.spider_giant_legs` → `geometry.mv.spider_giant_legs` (RP/models/entity/spider_giant_legs.geo.json, 16 cubos; cuelga de: body0, leg0, leg1, leg2, leg3, leg4, leg5, leg6, leg7): 26 texturas (las skins del cuerpo: `spider/spider`, … )

### BP

- Archivo: `BP/entities/spider.json`
- `mv:variant` [0, 26]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 10:1 11:1 12:1 13:1 14:1 15:1 16:1 17:1 18:1 19:1 20:1 21:1 22:1 23:1 24:1 25:1 26:1 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 1]: valor:peso 0:85 1:15 (en minecraft:entity_spawned)

### Skins que no están en la base

- `spider/spider16` (antes `mv:variant`=16): pintada para otro modelo: cabeza 13 %, patas 30 %

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
