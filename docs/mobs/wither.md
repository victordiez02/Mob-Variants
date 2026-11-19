# wither

Mob vanilla de momento: tenía modelo y animación propios y su textura no encaja en el modelo vanilla.

<!-- inventory:start -->
<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- La geometría propia redefinía los IDs vanilla `geometry.witherBoss` y `geometry.wither_skull` (regla 4).
- `wither.png` y `wither_invulnerable.png` (ruta vanilla) solo pintan el 64-69 % del torso vanilla: quitadas.
- El usuario quiere conservar su animación propia cuando vuelva.

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/wither.entity.json` (vanilla `wither.entity.json`)
- Render controller `controller.render.wither_boss` (vanilla)
- Render controller `controller.render.wither_boss_armor_white` (vanilla)
- Render controller `controller.render.wither_boss_armor_blue` (vanilla)

### Animaciones propias

- `move`: `animation.mv.wither_boss.move`

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
