# Estado del proyecto

Última actualización: 2026-11-19 (versión del pack 5.0.0, objetivo Minecraft 1.26.60).
Actualiza este archivo al terminar cada tarea.

## Estado por mob

"Puerta" = cuándo se aplican las skins (`v.mv_active`); fuera de ella el mob es vanilla.
"Modelo base" = `mv_default`. Las geometrías `geometry.mv.*` son capas o variantes propias.

| Mob | Puerta | Modelo base | Geometrías propias | BP (`mv:variant` / `mv:mark_variant`) | Estado |
|---|---|---|---|---|---|
| bee | adulto | vanilla | bee_nectar | 0-7 | ok |
| blaze | siempre | vanilla | – | 0-8 | ok |
| cat | adulto y gato blanco (`q.variant == 0`) | vanilla | gatos especiales (Garfield, Nyan, Puss, Tom) | 0-4 | ok; 0 = gato blanco normal |
| cave_spider | siempre | vanilla | – | 0-7 | ok |
| chicken | adulto templado | vanilla `chicken.v1.12` | chicken_extras (cola, papada, cresta, pico inferior), duck, goose | 0-11 | ok; pato y oca: modelo completo con huesos vanilla |
| creeper | siempre | vanilla `creeper.v1.8` | creeper_extras (costillas, torso, calavera), TnT, cactus, piedra, conchas; creeper esqueleto (modelo completo) | 0-34 / 0-4 | ok; creeper esqueleto con huesos vanilla |
| dolphin | adulto | vanilla | – | 0-7 | ok (7 skins, antes salía solo la primera) |
| drowned | adulto | **cuerpo propio** `mv.drowned` (160×63) | drowned_trident | 0-5 / 0-1 | pendiente (decisión aplazada por el usuario) |
| ender_dragon | siempre | vanilla | – | 0-7 | ok |
| enderman | siempre | vanilla | – | 0-26 | pendiente: dientes/lengua al enfadarse (ver tareas) |
| evocation_illager | siempre | vanilla | sombreros y disfraces (chef, wizard, …) | 0-32 / 0-8 | ok |
| fox | adulto y zorro rojo | vanilla | platypus, platypus_perry | 0-2 | ok; 1 ornitorrinco, 2 Perry |
| frog | siempre (cada clima con sus skins) | vanilla | frog_crown | 0-20 / 0-2 | ok; 1-10 skins del clima, 11-20 especiales |
| ghast | siempre | vanilla | – | 0-13 | ok |
| guardian | siempre | vanilla | – | 0-9 | ok |
| hoglin | adulto | vanilla | cabezas de piglin, calavera wither | 0-11 / 0-3 | ok |
| iron_golem | siempre | vanilla | irongolem_rose | 0-16 / 0-1 | ok |
| pig | adulto templado | vanilla **antiguo** `geometry.pig` + `setup.v1.0` | pig_extras (orejas, cola), capibara, snail, pig_chest, pig_flower | 0-8 / 0-3 | ok (probado) |
| piglin | adulto | vanilla | – | – / 0-13 | ok |
| piglin_brute | siempre | vanilla | piglin_mask | 0-13 | ok |
| pillager | siempre | vanilla | pillager_helmet | 0-23 / 0-4 | ok |
| ravager | siempre | vanilla | – | 0-9 | ok |
| sheep | adulto | vanilla | sheep_horns | 0-2 | ok |
| skeleton | siempre | vanilla | skeleton.armor, skeleton.armor2 (ropa) | 0-15 / 0-1 | ok |
| sniffer | adulto | vanilla | flores (crecen con temporizadores del BP) | 0-9 / 0-7 | ok |
| spider | siempre | vanilla (patas ocultas si es gigante) | spider_fangs, spider_giant_legs (muslo + articulación) | 0-26 / 0-1 (gigante) | ok; la gigante tenía las patas hundidas en el suelo |
| stray | – | vanilla | – | – | retextura pura (`stray.png` + `stray_overlay.png`), sin entidad |
| turtle | adulto | vanilla | – | 0-6 | ok |
| villager_v2 | adulto | vanilla | villager_professions (una capa por profesión) | – (sin BP) | ok |
| vindicator | siempre | vanilla | armaduras | 0-21 / 0-4 | ok; `part_visibility` vanilla (brazos) |
| wandering_trader | siempre | vanilla | mochila | 0-9 | ok |
| warden | siempre | vanilla | – | 0-6 | ok |
| witch | siempre | vanilla (sombrero oculto) | witch_extras (sombrero, escoba, pociones) | 0-9 | ok (probado) |
| wither | siempre | **modelo propio** `mv.wither_boss` | armadura, calavera | – | excepción aceptada: conserva modelo y animación |
| wither_skeleton | siempre | vanilla | capa, mochila, cabezas de piglin | 0-9 / 0-2 | ok |
| zombie | adulto | vanilla | que se arrastra (zombie2-5, animación propia), mandíbula rota, minero, espadas, flechas, pierna | `variant` 0-34, `pose` 0-6, `miner`, `sword` 0-3, `sword_type` 0-5, `arrow`/`arrow2` 0-5 | ok (bdstest a y=64 y y=10) |
| zombie_villager_v2 | adulto | vanilla | – | – (sin BP) | ok |

Retexturas puras (solo texturas en rutas vanilla, sin entidad): caballos/burro/mula/caballo
esqueleto/zombi (`horse2/`), panda, slime, stray, wither.

Mobs vanilla puros (se quitó todo): lobo, vaca, champiñaca, calamar, calamar brillante, allay, cabra,
ocelote, husk.

## Tareas pendientes

Lista viva y detallada en [PLAN.md](PLAN.md). Resumen de lo que queda:

1. **Ahogado**: cuerpo distinto (piernas de 2 px, cabeza 7×7, textura 160×63). Decisión del usuario.
2. **Enderman**: dientes y lengua al enfadarse. Propuesta: pintarlos en la zona `hat` (UV 0,16) de
   cada skin con `enderman_jaw.png`, sin geometría. Pendiente de aprobación.
3. **Oveja**: el usuario ve que le falta el hocico; RP, geometría y textura coinciden con vanilla.
   Pendiente de captura.
4. **Compatibilidad con Actions & Stuff**: dos packs no pueden redefinir la misma entidad de cliente.
5. **Sorteo sin BP por posición**: estudiado, no compensa (ver PLAN.md).

## Hallazgos resueltos (2026-11-19)

- Avisos del editor: `.mcignore`, `.mcattributes`, `cspell.json`, `.gitattributes` (docs/TOOLS.md).
- 33 capas con pivote/padre/rotación vanilla (`geotool relayer`); `bbcheck --measure`: 0 px en todas.
- Delfín con sus 7 skins y BP; ranas frías/cálidas con sus skins; araña gigante con las patas en el
  suelo; pollo y creeper con modelo vanilla + capa; `pack_icon` 256×256; claves sin uso eliminadas.
- Herramientas: render.py (neverRender, bind_pose_rotation, pivote de cubo por defecto en el centro),
  bbscene/load_scene (pivote de cubo, relative_to), molang.py (`true`/`false`), validate (variables
  `v.mv_*` sin asignar, rotación de capas), simulate (texturas vanilla).

## Historial de decisiones

- Persistencia con propiedades `mv:*` en lugar de `minecraft:variant` (choca con vanilla).
- Bebés siempre vanilla (tienen modelos propios nuevos que no encajan con las skins).
- Carpetas `BP/` y `RP/`, versión 5.0.0, `min_engine_version` 1.26.60.
- Sin animaciones propias ni modelos re-rigueados; añadidos como capas (por compatibilidad con A&S).
- Borrados: Rey Esqueleto Wither, modelos WIP sin usar (blastling, watchling, endersent, necrosent,
  hector_salamanca, evoker_costume, piglin_merchant), skins de vaca/champiñaca, BP de la vaca.
- El zombie_pillager.json del BP era el zombie villager v1 vanilla con un sorteo sin uso: borrado.
- Subvariantes por variante vanilla: empezado con la rana (cada clima usa sus skins).
- Párpados de pollo y creeper eliminados: necesitaban animación propia (regla 1).
- 0 animaciones propias salvo wither y zombi que se arrastra. Variantes de modelo completo con huesos
  renombrados a los vanilla (`geotool rebone`), sin párpados. Entidades reconstruidas desde la vanilla
  (la lista `animation_controllers` duplicaba animaciones).
- Zombi: una propiedad BP por rasgo (la codificación en dos números salía mal: solo espadas de madera).
- Aldeano: una capa por profesión (`villager_professions.geo.json`), piernas con `inflate` 0.1.
- Borrados los duplicados `vindicator12.png` y `chicken2.png` (pollito).
