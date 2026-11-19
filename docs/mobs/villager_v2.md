# villager_v2

Mob vanilla de momento: no tenía skins del cuerpo, solo capas de accesorios por profesión.

<!-- inventory:start -->
<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- En el juego: algunos aldeanos con dobles brazos (la capa de cada profesión traía brazos sueltos sobre los cruzados vanilla); el pescador parecía tener dos piernas (piernas idénticas superpuestas) y el librero tenía el accesorio roto (antes de separar una capa por profesión).

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/villager_v2.entity.json` (vanilla `villager_v2.entity.json`)
- Render controller `controller.render.villager_v3_base` si `!v.mv_active` (vanilla)
- Render controller `controller.render.villager_v3_masked` si `!v.mv_active` (vanilla)
- Render controller `controller.render.villager_v3_level` si `!v.mv_active` (vanilla)
- Render controller `controller.render.mv.villager_v2_base` si `v.mv_active` (RP/render_controllers/villager_v2.render_controllers.json)
- Render controller `controller.render.mv.villager_v2_masked` si `v.mv_active` (RP/render_controllers/villager_v2.render_controllers.json)
- Render controller `controller.render.mv.villager_v2_level` si `v.mv_active` (RP/render_controllers/villager_v2.render_controllers.json)
- Render controller `controller.render.mv.villager_v2_overlay` si `v.mv_active` (RP/render_controllers/villager_v2_overlay.render_controllers.json)

### Capas (accesorios)

- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_farmer` (RP/models/entity/villager_professions.geo.json, 52 cubos; cuelga de: arms, body, head, leg0, leg1): `empty`, `villager2/professions/farmer_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_fisherman` (RP/models/entity/villager_professions.geo.json, 35 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/fisherman_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_shepherd` (RP/models/entity/villager_professions.geo.json, 27 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/shepherd_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_fletcher` (RP/models/entity/villager_professions.geo.json, 57 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/fletcher_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_librarian` (RP/models/entity/villager_professions.geo.json, 11 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/librarian_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_cartographer` (RP/models/entity/villager_professions.geo.json, 12 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/cartographer_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_cleric` (RP/models/entity/villager_professions.geo.json, 73 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/cleric_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_armorer` (RP/models/entity/villager_professions.geo.json, 13 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/armorer_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_weapon_smith` (RP/models/entity/villager_professions.geo.json, 53 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/weaponsmith_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_tool_smith` (RP/models/entity/villager_professions.geo.json, 44 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/toolsmith_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_butcher` (RP/models/entity/villager_professions.geo.json, 8 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/butcher_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_leatherworker` (RP/models/entity/villager_professions.geo.json, 48 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/leatherworker_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_stonemason` (RP/models/entity/villager_professions.geo.json, 43 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/stonemason_overlay`
- `controller.render.mv.villager_v2_overlay` → `geometry.mv.villager_nitwit` (RP/models/entity/villager_professions.geo.json, 9 cubos; cuelga de: arms, body, head, leg0, leg1): `villager2/professions/nitwit_overlay`

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
