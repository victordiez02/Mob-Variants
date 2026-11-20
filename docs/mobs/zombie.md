# zombie

En la base: 33 skins sobre el modelo vanilla, puerta `!q.is_baby`; BP con `mv:variant` (sorteo en entity_spawned, entity_born).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/zombie.entity.json` sobre la vanilla `zombie.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0 && (!q.is_baby);`
- Render controller: `controller.render.mv.zombie` (RP/render_controllers/zombie.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/zombie.json`, `mv:variant` [0, 33], sorteo en: minecraft:entity_born, minecraft:entity_spawned

### `array.mv_skins` (skins, 33)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/zombie/zombie` (pack) | 100 (3.0%) |  |
| 2 | `mv_default2` | `textures/entity/zombie/zombie2` (pack) | 100 (3.0%) |  |
| 3 | `mv_default3` | `textures/entity/zombie/zombie3` (pack) | 100 (3.0%) |  |
| 4 | `mv_default4` | `textures/entity/zombie/zombie4` (pack) | 100 (3.0%) |  |
| 5 | `mv_default5` | `textures/entity/zombie/zombie5` (pack) | 100 (3.0%) |  |
| 6 | `mv_default6` | `textures/entity/zombie/zombie6` (pack) | 100 (3.0%) |  |
| 7 | `mv_default7` | `textures/entity/zombie/zombie7` (pack) | 100 (3.0%) |  |
| 8 | `mv_default8` | `textures/entity/zombie/zombie8` (pack) | 100 (3.0%) |  |
| 9 | `mv_default9` | `textures/entity/zombie/zombie9` (pack) | 100 (3.0%) |  |
| 10 | `mv_default10` | `textures/entity/zombie/zombie10` (pack) | 100 (3.0%) |  |
| 11 | `mv_default11` | `textures/entity/zombie/zombie11` (pack) | 100 (3.0%) |  |
| 12 | `mv_default12` | `textures/entity/zombie/zombie12` (pack) | 100 (3.0%) |  |
| 13 | `mv_default13` | `textures/entity/zombie/zombie13` (pack) | 100 (3.0%) |  |
| 14 | `mv_default14` | `textures/entity/zombie/zombie14` (pack) | 100 (3.0%) |  |
| 15 | `mv_default15` | `textures/entity/zombie/zombie15` (pack) | 100 (3.0%) |  |
| 16 | `mv_default16` | `textures/entity/zombie/zombie16` (pack) | 100 (3.0%) |  |
| 17 | `mv_default17` | `textures/entity/zombie/zombie17` (pack) | 100 (3.0%) |  |
| 18 | `mv_default18` | `textures/entity/zombie/zombie18` (pack) | 100 (3.0%) |  |
| 19 | `mv_default19` | `textures/entity/zombie/zombie19` (pack) | 100 (3.0%) |  |
| 20 | `mv_default20` | `textures/entity/zombie/zombie20` (pack) | 100 (3.0%) |  |
| 21 | `mv_default21` | `textures/entity/zombie/zombie21` (pack) | 100 (3.0%) |  |
| 22 | `mv_default22` | `textures/entity/zombie/zombie22` (pack) | 100 (3.0%) |  |
| 23 | `mv_default23` | `textures/entity/zombie/zombie23` (pack) | 100 (3.0%) |  |
| 24 | `mv_default24` | `textures/entity/zombie/zombie24` (pack) | 100 (3.0%) |  |
| 25 | `mv_default25` | `textures/entity/zombie/zombie25` (pack) | 100 (3.0%) |  |
| 26 | `mv_default26` | `textures/entity/zombie/zombie26` (pack) | 100 (3.0%) |  |
| 27 | `mv_default27` | `textures/entity/zombie/zombie27` (pack) | 100 (3.0%) |  |
| 28 | `mv_default28` | `textures/entity/zombie/zombie28` (pack) | 100 (3.0%) |  |
| 29 | `mv_default29` | `textures/entity/zombie/zombie29` (pack) | 100 (3.0%) |  |
| 30 | `mv_default30` | `textures/entity/zombie/zombie30` (pack) | 100 (3.0%) |  |
| 31 | `mv_default31` | `textures/entity/zombie/zombie31` (pack) | 100 (3.0%) |  |
| 32 | `mv_default32` | `textures/entity/zombie/zombie32` (pack) | 100 (3.0%) |  |
| 33 | `mv_default33` | `textures/entity/zombie/zombie33` (pack) | 100 (3.0%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- En el juego: el **casco de minero salía en zombis tumbados** como si estuvieran de pie. Sospecha: los filtros `int_property mv:pose < 3` del mismo evento leen la propiedad antes de que se aplique el `set_property` de la pose; por la misma razón saldrían espadas y flechas en los tumbados.
- Antes solo salían espadas de madera y nunca flechas (codificación en dos números): arreglado con una propiedad por rasgo (be1cf62).
- **Actions & Stuff (SP0)**: primer mob de la prueba de compatibilidad (docs/ANS.md). Su modelo no tiene sombrero y usa esa zona de la textura (x 40-56, y 0-16) para hombreras y pies: `ans_patch.py` limpia esa zona en zombie3, 4, 6, 7, 11, 17, 19, 20, 24, 25, 26, 27, 29 y 31 (pierden el sombrero con A&S). Pendiente de probar en el juego.
- El zombi que se arrastra (zombie2-5) tenía animación propia `animation.mv.zombie_crawl.*`: el usuario quiere conservarla cuando vuelva (es propia de esa geometría).

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/zombie.entity.json` (vanilla `zombie.entity.json`)
- Render controller `controller.render.zombie.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.zombie` si `v.mv_active` (RP/render_controllers/zombie.render_controllers.json)
- Render controller `controller.render.mv.zombie_leg` si `v.mv_active` (RP/render_controllers/zombie.render_controllers.json)
- Render controller `controller.render.mv.zombie_sword` si `v.mv_active` (RP/render_controllers/zombie.render_controllers.json)
- Render controller `controller.render.mv.zombie_arrow` si `v.mv_active` (RP/render_controllers/zombie.render_controllers.json)
- Render controller `controller.render.mv.zombie_arrow2` si `v.mv_active` (RP/render_controllers/zombie.render_controllers.json)
- Render controller `controller.render.mv.zombie_miner` si `v.mv_active` (RP/render_controllers/zombie.render_controllers.json)
- Render controller `controller.render.mv.zombie_miner_pickaxe` si `v.mv_active` (RP/render_controllers/zombie.render_controllers.json)

### Variantes de modelo completo

Geometría propia dibujada en lugar del cuerpo vanilla (huesos con nombre vanilla para que la animen las animaciones vanilla; ver `geotool rebone`).

- `geometry.mv.zombie_brokenjaw2` (RP/models/entity/zombie_brokenjaw2.geo.json, 13 cubos; huesos: body, hat, head, leftArm, leftItem, leftLeg, rightArm, rightItem, rightLeg, waist): 34 texturas (las skins del cuerpo: `zombie/zombie`, … )
- `geometry.mv.zombie_brokenjaw` (RP/models/entity/zombie_brokenjaw.geo.json, 13 cubos; huesos: body, hat, head, leftArm, leftItem, leftLeg, rightArm, rightItem, rightLeg, waist): 33 texturas (las skins del cuerpo: `zombie/zombie`, … )
- `geometry.mv.zombie2` (RP/models/entity/zombie2.geo.json, 11 cubos; huesos: body_z2, bone, elbow2_z2, elbow_z2, hat_z2, head_z2, knee2_z2, knee_z2, leftArm_z2, leftItem, leftLeg_z2, rightArm_z2, rightItem, rightLeg_z2, root_z2, spine_z2, waist_z2): 33 texturas (las skins del cuerpo: `zombie/zombie`, … )
- `geometry.mv.zombie3` (RP/models/entity/zombie3.geo.json, 10 cubos; huesos: body_z2, bone, elbow2_z2, elbow_z2, hat_z2, head_z2, knee2_z2, knee_z2, leftArm_z2, leftItem, leftLeg_z2, rightArm_z2, rightItem, rightLeg_z2, root_z2, spine_z2, waist_z2): 33 texturas (las skins del cuerpo: `zombie/zombie`, … )
- `geometry.mv.zombie4` (RP/models/entity/zombie4.geo.json, 10 cubos; huesos: body_z2, bone, elbow2_z2, elbow_z2, hat_z2, head_z2, knee2_z2, leftArm_z2, leftItem, leftLeg_z2, rightArm_z2, rightItem, rightLeg_z2, root_z2, spine_z2, waist_z2): 33 texturas (las skins del cuerpo: `zombie/zombie`, … )
- `geometry.mv.zombie5` (RP/models/entity/zombie5.geo.json, 9 cubos; huesos: body_z2, bone, elbow2_z2, elbow_z2, hat_z2, head_z2, knee2_z2, leftArm_z2, leftItem, leftLeg_z2, rightArm_z2, rightItem, rightLeg_z2, root_z2, spine_z2, waist_z2): 33 texturas (las skins del cuerpo: `zombie/zombie`, … )

### Capas (accesorios)

- `controller.render.mv.zombie_leg` → `geometry.mv.zombie_leg` (RP/models/entity/zombie_leg.geo.json, 2 cubos; cuelga de: bloodl_z2, bloodr_z2, bone, leftLeg_z2, rightLeg_z2, root_z2, waist_z2): `zombie/zombie_leg`
- `controller.render.mv.zombie_sword` → `geometry.mv.zombie_sword_chest` (RP/models/entity/zombie_sword_chest.geo.json, 104 cubos; cuelga de: body, waist): `zombie/zombie_wsword_chest`
- `controller.render.mv.zombie_sword` → `geometry.mv.zombie_sword_chest2` (RP/models/entity/zombie_sword_chest2.geo.json, 104 cubos; cuelga de: body, waist): `zombie/zombie_wsword_chest`
- `controller.render.mv.zombie_sword` → `geometry.mv.zombie_sword_head` (RP/models/entity/zombie_sword_head.geo.json, 84 cubos; cuelga de: body, head, waist): `zombie/zombie_wsword_chest`
- `controller.render.mv.zombie_arrow` → `geometry.mv.arrow_head_2` (RP/models/entity/arrow_head_2.geo.json, 3 cubos; cuelga de: body, head, waist): `arrows`
- `controller.render.mv.zombie_arrow` → `geometry.mv.arrow_chest_1` (RP/models/entity/arrow_chest_1.geo.json, 3 cubos; cuelga de: body, waist): `arrows`
- `controller.render.mv.zombie_arrow` → `geometry.mv.arrow_chest_2` (RP/models/entity/arrow_chest_2.geo.json, 3 cubos; cuelga de: body, waist): `arrows`
- `controller.render.mv.zombie_arrow` → `geometry.mv.arrow_knee` (RP/models/entity/arrow_knee.geo.json, 3 cubos; cuelga de: body, rightLeg, waist): `arrows`
- `controller.render.mv.zombie_arrow` → `geometry.mv.arrow_head_1` (RP/models/entity/arrow_head_1.geo.json, 3 cubos; cuelga de: body, head, waist): `arrows`
- `controller.render.mv.zombie_arrow2` → `geometry.mv.arrow_head_2` (RP/models/entity/arrow_head_2.geo.json, 3 cubos; cuelga de: body, head, waist): `arrows`
- `controller.render.mv.zombie_arrow2` → `geometry.mv.arrow_chest_1` (RP/models/entity/arrow_chest_1.geo.json, 3 cubos; cuelga de: body, waist): `arrows`
- `controller.render.mv.zombie_arrow2` → `geometry.mv.arrow_chest_2` (RP/models/entity/arrow_chest_2.geo.json, 3 cubos; cuelga de: body, waist): `arrows`
- `controller.render.mv.zombie_arrow2` → `geometry.mv.arrow_knee` (RP/models/entity/arrow_knee.geo.json, 3 cubos; cuelga de: body, rightLeg, waist): `arrows`
- `controller.render.mv.zombie_arrow2` → `geometry.mv.arrow_head_1` (RP/models/entity/arrow_head_1.geo.json, 3 cubos; cuelga de: body, head, waist): `arrows`
- `controller.render.mv.zombie_miner` → `geometry.mv.miner` (RP/models/entity/miner.geo.json, 7 cubos; cuelga de: body, hat, head, waist): `zombie/miner`
- `controller.render.mv.zombie_miner_pickaxe` → `geometry.mv.miner_pickaxe` (RP/models/entity/miner_pickaxe.geo.json, 84 cubos; cuelga de: body, leftArm, leftItem, waist): `zombie/zombie_gsword_chest`, `zombie/zombie_isword_chest`, `zombie/zombie_ssword_chest`, `zombie/zombie_wsword_chest`

### Animaciones propias

- `mv_crawl_idle`: `animation.mv.zombie_crawl.idle`
- `mv_crawl_walk`: `animation.mv.zombie_crawl.walk`
- `mv_crawl_attack`: `animation.mv.zombie_crawl.attack`
- `mv_crawl_death`: `animation.mv.zombie_crawl.death`

### BP

- Archivo: `BP/entities/zombie.json`
- `mv:variant` [0, 34]: valor:peso 1:100 2:100 3:100 4:100 5:100 6:100 7:100 8:100 9:100 10:100 11:100 12:100 13:100 14:100 15:100 16:100 17:100 18:100 19:100 20:100 21:100 22:100 23:100 24:100 25:100 26:100 27:100 28:100 29:100 30:100 31:100 32:100 33:100 34:1 (en minecraft:entity_spawned)
- `mv:pose` [0, 6]: valor:peso 0:23.4 1:23.3 2:23.3 3:7.5 4:7.5 5:7.5 6:7.5 (en minecraft:entity_spawned)
- `mv:miner` [0, 1]: valor:peso 0:70 1:30 (en minecraft:entity_spawned)
- `mv:sword` [0, 3]: valor:peso 0:80 1:7.5 2:7.5 3:5 (en minecraft:entity_spawned)
- `mv:sword_type` [0, 5]: valor:peso 0:25 1:25 2:20 3:25 4:4 5:1 (en minecraft:entity_spawned)
- `mv:arrow` [0, 5]: valor:peso 0:76 1:4 2:5 3:5 4:5 5:5 (en minecraft:entity_spawned)
- `mv:arrow2` [0, 5]: valor:peso 0:76 1:4 2:5 3:5 4:5 5:5 (en minecraft:entity_spawned)
- Filtros sobre propiedades propias: mv:pose

### Skins que no están en la base

- `zombie/zombie_gold` (antes `mv:variant`=34): zombi dorado: usaba el material `enderman` (alfa = brillo); con el material vanilla sale transparente

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
