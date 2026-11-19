# drowned

Mob vanilla de momento: sus skins se pintaron para un cuerpo propio (160×63). **Aplazado por el usuario**.

<!-- inventory:start -->
<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- Aplazado por el usuario (recordárselo). Cuerpo distinto: piernas de 2 px, cabeza 7×7, textura 160×63.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/drowned.entity.json` (vanilla `drowned.entity.json`)
- Render controller `controller.render.zombie.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.drowned` si `v.mv_active` (RP/render_controllers/drowned.render_controllers.json)
- Render controller `controller.render.mv.drowned_trident` si `v.mv_active` (RP/render_controllers/drowned.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.drowned` → `geometry.mv.drowned` (RP/models/entity/drowned.geo.json, 24 cubos; cuelga de: body, hat, head, jacket, leftArm, leftItem, leftLeg, leftPants, rightArm, rightItem, rightLeg, rightPants, root, waist): `zombie/drowned`, `zombie/drowned2`, `zombie/drowned3`, `zombie/drowned4`, `zombie/drowned5`
- `controller.render.mv.drowned_trident` → `geometry.mv.drowned_trident` (RP/models/entity/drowned_trident.geo.json, 4 cubos; cuelga de: UpperBody, body, jacket, pole, spine): `trident`

### BP

- Archivo: `BP/entities/drowned.json`
- `mv:variant` [0, 5]: valor:peso 1:1 2:1 3:1 4:1 5:1 (en minecraft:entity_spawned)
- `mv:mark_variant` [0, 1]: valor:peso 1:2 0:8 (en minecraft:entity_spawned)

### Skins que no están en la base

- `zombie/drowned` (antes `mv:variant`=1): variante de modelo completo `geometry.mv.drowned`
- `zombie/drowned2` (antes `mv:variant`=2): variante de modelo completo `geometry.mv.drowned`
- `zombie/drowned3` (antes `mv:variant`=3): variante de modelo completo `geometry.mv.drowned`
- `zombie/drowned4` (antes `mv:variant`=4): variante de modelo completo `geometry.mv.drowned`
- `zombie/drowned5` (antes `mv:variant`=5): variante de modelo completo `geometry.mv.drowned`

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
