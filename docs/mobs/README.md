# Mobs

Una ficha por mob. Cada ficha tiene:

- **Estado actual**: generado por `python tools/inventory.py` (entidad, puerta, skins con su peso en el BP y
  aviso de las que no pintan alguna pieza del modelo vanilla). No se edita a mano: vuelve a ejecutar la herramienta.
- **Notas**: fallos vistos en el juego y decisiones.
- **Antes (`legacy-v5`)**: lo que tenía el add-on antes de la base solo de skins (capas, variantes de modelo
  completo, animaciones propias, BP), con las rutas para recuperarlo (`git show legacy-v5:<ruta>`).
- **Plan**: lo pendiente de ese mob. Para trabajar un mob: skill `mv-mob`.

Retexturas puras (sin entidad, textura en la ruta vanilla): caballos, burro, mula y caballos esqueleto y zombi
(`horse2/`), panda, slime, stray y oveja (`sheep.tga`).

<!-- inventory:start -->

| Mob | Skins | BP | Skins a revisar |
|---|---|---|---|
| [bee](bee.md) | 7 | sí |  |
| [blaze](blaze.md) | 8 | sí | 1 |
| [chicken](chicken.md) | 4 | sí |  |
| [creeper](creeper.md) | 18 | sí |  |
| [dolphin](dolphin.md) | 7 | sí | 3 |
| [ender_dragon](ender_dragon.md) | 7 | sí | 1 |
| [enderman](enderman.md) | 26 | sí | 2 |
| [evocation_illager](evocation_illager.md) | 31 | sí |  |
| [frog](frog.md) | 40 | sí |  |
| [ghast](ghast.md) | 13 | sí | 1 |
| [guardian](guardian.md) | 9 | sí |  |
| [hoglin](hoglin.md) | 11 | sí |  |
| [iron_golem](iron_golem.md) | 15 | sí |  |
| [pig](pig.md) | 5 | sí |  |
| [piglin](piglin.md) | 13 | sí | 5 |
| [piglin_brute](piglin_brute.md) | 13 | sí | 5 |
| [pillager](pillager.md) | 23 | sí |  |
| [ravager](ravager.md) | 9 | sí |  |
| [skeleton](skeleton.md) | 15 | sí |  |
| [sniffer](sniffer.md) | 9 | sí | 1 |
| [spider](spider.md) | 25 | sí | 1 |
| [turtle](turtle.md) | 6 | sí |  |
| [vindicator](vindicator.md) | 21 | sí | 3 |
| [wandering_trader](wandering_trader.md) | 9 | sí |  |
| [warden](warden.md) | 6 | sí |  |
| [witch](witch.md) | 9 | sí | 9 |
| [wither_skeleton](wither_skeleton.md) | 9 | sí |  |
| [zombie](zombie.md) | 33 | sí |  |
| [zombie_villager_v2](zombie_villager_v2.md) | 9 | sí |  |

Sin entidad en el pack (vanilla puro de momento; ver su md): [cat](cat.md), [cave_spider](cave_spider.md), [drowned](drowned.md), [fox](fox.md), [sheep](sheep.md), [villager_v2](villager_v2.md), [wither](wither.md), [wither_skull](wither_skull.md), [wither_skull_dangerous](wither_skull_dangerous.md).

<!-- inventory:end -->
