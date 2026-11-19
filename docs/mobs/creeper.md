# creeper

En la base: 18 skins sobre el modelo vanilla; BP con `mv:variant` (sorteo en entity_spawned).

<!-- inventory:start -->

## Estado actual (generado por `tools/inventory.py`, no editar a mano)

- Entidad: `RP/entity/creeper.entity.json` sobre la vanilla `creeper.entity.json`
- Puerta: `v.mv_active = v.mv_variant > 0;`
- Render controller: `controller.render.mv.creeper` (RP/render_controllers/creeper.render_controllers.json) con condición `v.mv_active`
- BP: `BP/entities/creeper.json`, `mv:variant` [0, 18], sorteo en: minecraft:entity_spawned

### `array.mv_skins` (skins, 18)

| `mv:variant` | Clave | Textura | Peso BP | Revisar |
|---|---|---|---|---|
| 1 | `mv_default` | `textures/entity/creeper/creeper` (vanilla) | 70 (5.6%) |  |
| 2 | `mv_default2` | `textures/entity/creeper/creeper2` (pack) | 70 (5.6%) |  |
| 3 | `mv_default3` | `textures/entity/creeper/creeper3` (pack) | 70 (5.6%) |  |
| 4 | `mv_default4` | `textures/entity/creeper/creeper4` (pack) | 70 (5.6%) |  |
| 5 | `mv_default5` | `textures/entity/creeper/creeper5` (pack) | 70 (5.6%) |  |
| 6 | `mv_default6` | `textures/entity/creeper/creeper6` (pack) | 70 (5.6%) |  |
| 7 | `mv_default7` | `textures/entity/creeper/creeper7` (pack) | 70 (5.6%) |  |
| 8 | `mv_default8` | `textures/entity/creeper/creeper8` (pack) | 70 (5.6%) |  |
| 9 | `mv_default9` | `textures/entity/creeper/creeper9` (pack) | 70 (5.6%) |  |
| 10 | `mv_default10` | `textures/entity/creeper/creeper10` (pack) | 70 (5.6%) |  |
| 11 | `mv_default11` | `textures/entity/creeper/creeper11` (pack) | 70 (5.6%) |  |
| 12 | `mv_default12` | `textures/entity/creeper/creeper12` (pack) | 70 (5.6%) |  |
| 13 | `mv_default13` | `textures/entity/creeper/creeper13` (pack) | 70 (5.6%) |  |
| 14 | `mv_default14` | `textures/entity/creeper/creeper14` (pack) | 70 (5.6%) |  |
| 15 | `mv_default15` | `textures/entity/creeper/creeper15` (pack) | 70 (5.6%) |  |
| 16 | `mv_default16` | `textures/entity/creeper/creeper17` (pack) | 70 (5.6%) |  |
| 17 | `mv_default17` | `textures/entity/creeper/creeper18` (pack) | 70 (5.6%) |  |
| 18 | `mv_default18` | `textures/entity/creeper/creeper19` (pack) | 70 (5.6%) |  |

<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- En el juego: el creeper esqueleto se animaba mal (arreglado con `geotool rebone`).

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/creeper.entity.json` (vanilla `creeper.entity.json`)
- Render controller `controller.render.mv.creeper` (RP/render_controllers/creeper.render_controllers.json)
- Render controller `controller.render.mv.creeper_extras` si `!v.mv_skeleton` (RP/render_controllers/creeper.render_controllers.json)
- Render controller `controller.render.mv.creeper_hat` (RP/render_controllers/creeper.render_controllers.json)
- Render controller `controller.render.mv.creeper_TnT_s` (RP/render_controllers/creeper.render_controllers.json)
- Render controller `controller.render.creeper_armor` si `query.is_powered` (vanilla)

### Variantes de modelo completo

Geometría propia dibujada en lugar del cuerpo vanilla (huesos con nombre vanilla para que la animen las animaciones vanilla; ver `geotool rebone`).

- `geometry.mv.creeper_s` (RP/models/entity/creeper_s.geo.json, 11 cubos; huesos: body, head, leg0, leg1, leg2, leg3): 15 texturas (las skins del cuerpo: `skeleton/skeleton`, … )

### Capas (accesorios)

- `controller.render.mv.creeper_extras` → `geometry.mv.creeper_extras` (RP/models/entity/creeper_extras.geo.json, 11 cubos; cuelga de: body, head): 19 texturas (las skins del cuerpo: `creeper/creeper`, … )
- `controller.render.mv.creeper_hat` → `geometry.mv.creeper_TnT` (RP/models/entity/creeper_TnT.geo.json, 2 cubos; cuelga de: body, head): `creeper/creeper_TnT`
- `controller.render.mv.creeper_hat` → `geometry.mv.creeper_cactus` (RP/models/entity/creeper_cactus.geo.json, 3 cubos; cuelga de: body, head): `creeper/creeper_cactus`
- `controller.render.mv.creeper_hat` → `geometry.mv.creeper_stone` (RP/models/entity/creeper_stone.json, 2 cubos; cuelga de: body, head): `creeper/creeper_stone`
- `controller.render.mv.creeper_hat` → `geometry.mv.creeper_shells` (RP/models/entity/creeper_shells.geo.json, 2 cubos; cuelga de: body, head): `creeper/creeper_shells`
- `controller.render.mv.creeper_TnT_s` → `geometry.mv.creeper_ribs_TnT` (RP/models/entity/creeper_ribs_TnT.geo.json, 1 cubos; cuelga de: body): `creeper/creeper_TnT`
- `controller.render.mv.creeper_TnT_s` → `geometry.mv.creeper_TnT_s` (RP/models/entity/creeper_TnT_s.geo.json, 2 cubos; cuelga de: body, leg2): `creeper/creeper_TnT`

### BP

- Archivo: `BP/entities/creeper.json`
- `mv:variant` [0, 34]: valor:peso 1:70 2:70 3:70 4:70 5:70 6:70 7:70 8:70 9:70 10:70 11:70 12:70 13:70 14:70 15:70 16:70 17:70 18:70 19:70 20:30 21:30 22:30 23:30 24:30 25:30 26:30 27:30 28:30 29:30 30:30 31:30 32:30 33:30 34:30 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 4]: valor:peso 0:700 1:75 2:75 3:75 4:75 (en minecraft:entity_spawned)

### Skins que no están en la base

- `creeper/creeper16` (antes `mv:variant`=16): creeper esqueleto pensado para la capa de costillas `creeper_extras`: sin ella no tiene cuerpo (body 50 %)
- `skeleton/skeleton` (antes `mv:variant`=20): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton2` (antes `mv:variant`=21): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton3` (antes `mv:variant`=22): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton4` (antes `mv:variant`=23): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton5` (antes `mv:variant`=24): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton6` (antes `mv:variant`=25): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton7` (antes `mv:variant`=26): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton8` (antes `mv:variant`=27): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton9` (antes `mv:variant`=28): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton10` (antes `mv:variant`=29): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton11` (antes `mv:variant`=30): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton12` (antes `mv:variant`=31): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton13` (antes `mv:variant`=32): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton14` (antes `mv:variant`=33): variante de modelo completo `geometry.mv.creeper_s`
- `skeleton/skeleton15` (antes `mv:variant`=34): variante de modelo completo `geometry.mv.creeper_s`

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
