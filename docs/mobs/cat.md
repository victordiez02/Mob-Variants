# cat

Mob vanilla de momento: sus únicas variantes eran gatos especiales de modelo completo.

<!-- inventory:start -->
<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/cat.entity.json` (vanilla `cat.entity.json`)
- Render controller `controller.render.cat.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.cat` si `v.mv_active` (RP/render_controllers/cat.render_controllers.json)

### Variantes de modelo completo

Geometría propia dibujada en lugar del cuerpo vanilla (huesos con nombre vanilla para que la animen las animaciones vanilla; ver `geotool rebone`).

- `geometry.mv.cat_garfield` (RP/models/entity/cat_garfield.geo.json, 10 cubos; huesos: backLegL, backLegR, body, frontLegL, frontLegR, head, tail1, tail2): `cat/cat_garfield`, `cat/cat_garfield_tame`
- `geometry.mv.cat_pussinboots` (RP/models/entity/cat_pussinboots.geo.json, 23 cubos; huesos: backLegL, backLegR, body, frontLegL, frontLegR, head, tail1, tail2): `cat/cat_pussinboots`, `cat/cat_pussinboots_tame`
- `geometry.mv.cat_nyan` (RP/models/entity/cat_nyan.geo.json, 14 cubos; huesos: backLegL, backLegR, body, frontLegL, frontLegR, head, tail1, tail2): `cat/cat_nyan`, `cat/cat_nyan_tame`
- `geometry.mv.cat_tom` (RP/models/entity/cat_tom.geo.json, 17 cubos; huesos: backLegL, backLegR, body, frontLegL, frontLegR, head, tail1, tail2): `cat/cat_tom`, `cat/cat_tom_tame`

### BP

- Archivo: `BP/entities/cat.json`
- `mv:variant` [0, 4]: valor:peso 1:9 2:1 3:9 4:9 (en minecraft:entity_spawned)

### Skins que no están en la base

- `cat/cat_garfield` (antes `mv:variant`=1): variante de modelo completo `geometry.mv.cat_garfield`
- `cat/cat_pussinboots` (antes `mv:variant`=2): variante de modelo completo `geometry.mv.cat_pussinboots`
- `cat/cat_nyan` (antes `mv:variant`=3): variante de modelo completo `geometry.mv.cat_nyan`
- `cat/cat_tom` (antes `mv:variant`=4): variante de modelo completo `geometry.mv.cat_tom`

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
