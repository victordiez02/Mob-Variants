# cave_spider

Mob vanilla de momento: sus 7 skins (escorpiones) se pintaron para otro modelo y sobre la araña vanilla salen rotas.

<!-- inventory:start -->
<!-- inventory:end -->

## Notas (fallos vistos en el juego y decisiones)

- (ninguna todavía)

## Antes (`legacy-v5`)

Lo que tenía el add-on antes de la base solo de skins. Recuperar un archivo: `git show legacy-v5:<ruta>` o `git checkout legacy-v5 -- <ruta>`.

- Entidad: `RP/entity/cave_spider.entity.json` (vanilla `cave_spider.entity.json`)
- Render controller `controller.render.mv.cave_spider` (RP/render_controllers/cave_spider.render_controllers.json)

### BP

- Archivo: `BP/entities/cave_spider.json`
- `mv:variant` [0, 7]: valor:peso 1:1 2:1 3:1 4:1 5:1 6:1 7:1 (en minecraft:entity_spawned)

### Skins que no están en la base

- `spider/scorpion` (antes `mv:variant`=1): escorpión pintado para otro modelo: cabeza 18-38 %, cuerpo y patas incompletos (uno casi invisible)
- `spider/scorpion2` (antes `mv:variant`=2): escorpión pintado para otro modelo: cabeza 18-38 %, cuerpo y patas incompletos (uno casi invisible)
- `spider/scorpion3` (antes `mv:variant`=3): escorpión pintado para otro modelo: cabeza 18-38 %, cuerpo y patas incompletos (uno casi invisible)
- `spider/scorpion4` (antes `mv:variant`=4): escorpión pintado para otro modelo: cabeza 18-38 %, cuerpo y patas incompletos (uno casi invisible)
- `spider/scorpion5` (antes `mv:variant`=5): escorpión pintado para otro modelo: cabeza 18-38 %, cuerpo y patas incompletos (uno casi invisible)
- `spider/scorpion6` (antes `mv:variant`=6): escorpión pintado para otro modelo: cabeza 18-38 %, cuerpo y patas incompletos (uno casi invisible)
- `spider/scorpion7` (antes `mv:variant`=7): escorpión pintado para otro modelo: cabeza 18-38 %, cuerpo y patas incompletos (uno casi invisible)

## Plan

- [ ] Probar la base en el juego (mobs recién aparecidos).
- [ ] Decidir con el usuario qué extras de "Antes" vuelven, de uno en uno (skill `mv-mob`).
