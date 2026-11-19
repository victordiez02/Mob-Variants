# fox

Mob vanilla de momento: sus únicas variantes eran el ornitorrinco y Perry (modelo completo).

<!-- inventory:start -->
<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/fox.entity.json` (vanilla `fox.entity.json`)
- Render controller `controller.render.fox.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.fox` si `v.mv_active` (RP/render_controllers/fox.render_controllers.json)

### Variantes de modelo completo

Geometría propia dibujada en lugar del cuerpo vanilla (huesos con nombre vanilla para que la animen las animaciones vanilla; ver `geotool rebone`).

- `geometry.mv.platypus_perry` (RP/models/entity/fox_platypus_perry.geo.json, 15 cubos; huesos: body, head, leg0, leg1, leg2, leg3, root, tail): `fox/perry`
- `geometry.mv.platypus` (RP/models/entity/fox_platypus.geo.json, 13 cubos; huesos: body, head, leg0, leg1, leg2, leg3, root, tail): `fox/perry`

### BP

- Archivo: `BP/entities/fox.json`
- `mv:variant` [0, 2]: valor:peso 1:15 2:5 (en minecraft:entity_spawned)

### Skins que no están en la base

- `fox/perry` (antes `mv:variant`=1): variante de modelo completo `geometry.mv.platypus`
- `fox/perry` (antes `mv:variant`=2): variante de modelo completo `geometry.mv.platypus_perry`

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
