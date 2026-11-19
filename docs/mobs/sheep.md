# sheep

Sin entidad: solo la retextura `textures/entity/sheep/sheep.tga` en la ruta vanilla. Los cuernos eran una capa.

<!-- inventory:start -->
<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- En el juego: el usuario veía que **le faltaba el hocico**. RP, geometría y textura coincidían con vanilla y la retextura encaja en el UV; causa sin encontrar.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/sheep.entity.json` (vanilla `sheep.entity.json`)
- Render controller `controller.render.sheep.v2` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.sheep` si `v.mv_active` (RP/render_controllers/sheep.render_controllers.json)
- Render controller `controller.render.mv.sheep_horns` si `v.mv_active` (RP/render_controllers/sheep.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.sheep_horns` → `geometry.mv.sheep_horns` (RP/models/entity/sheep_horns.geo.json, 6 cubos; cuelga de: head): `sheep/sheep_horns`

### BP

- Archivo: `BP/entities/sheep.json`
- `mv:variant` [0, 2]: valor:peso 1:7 2:3 (en minecraft:entity_spawned)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
