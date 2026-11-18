# Estado del proyecto

Última actualización: 2026-11-18 (versión del pack 5.0.0, objetivo Minecraft 1.26.60).
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
| chicken | adulto templado | **re-rigueado** `mv.chicken` | duck, goose | 0-11 | pendiente: modelo vanilla + capas (cresta, cola, papada, pico) |
| creeper | siempre | **re-rigueado** `mv.creeper` | creeper esqueleto, TnT, cactus, piedra, conchas | 0-34 / 0-4 | pendiente: modelo vanilla + capas (costillas, calavera) |
| dolphin | adulto | vanilla | – | – (sin BP) | ok |
| drowned | adulto | **cuerpo propio** `mv.drowned` (160×63) | drowned_trident | 0-5 / 0-1 | pendiente (decisión aplazada por el usuario) |
| ender_dragon | siempre | vanilla | – | 0-7 | ok |
| enderman | siempre | vanilla | – | 0-26 | pendiente: dientes/lengua al enfadarse (ver tareas) |
| evocation_illager | siempre | vanilla | sombreros y disfraces (chef, wizard, …) | 0-32 / 0-8 | ok |
| fox | adulto y zorro rojo | vanilla | platypus, platypus_perry | 0-2 | ok; 1 ornitorrinco, 2 Perry |
| frog | rana templada | vanilla | frog_crown | 0-20 / 0-2 | ok; skins frías/cálidas sin usar (pendiente) |
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
| spider | siempre | vanilla | spider_fangs, spider_giant_legs | 0-26 / 0-1 (gigante) | por verificar: "mini patas" y araña gigante |
| stray | – | vanilla | – | – | retextura pura (`stray.png` + `stray_overlay.png`), sin entidad |
| turtle | adulto | vanilla | – | 0-6 | ok |
| villager_v2 | adulto | vanilla | villager_overlay | – (sin BP) | ok; codos de la skin algo desplazados |
| vindicator | siempre | vanilla | armaduras | 0-22 / 0-4 | ok |
| wandering_trader | siempre | vanilla | mochila | 0-9 | ok |
| warden | siempre | vanilla | – | 0-6 | ok |
| witch | siempre | vanilla (sombrero oculto) | witch_extras (sombrero, escoba, pociones) | 0-9 | ok (probado) |
| wither | siempre | **modelo propio** `mv.wither_boss` | armadura, calavera | – | excepción aceptada: conserva modelo y animación |
| wither_skeleton | siempre | vanilla | capa, mochila, cabezas de piglin | 0-9 / 0-2 | ok |
| zombie | adulto | vanilla | caídos (zombie2-5), mandíbula rota, minero, espadas, flechas, pierna | 0-334 / 0-615 | ok; codos de la skin algo desplazados |
| zombie_villager_v2 | adulto | vanilla | – | – (sin BP) | ok |

Retexturas puras (solo texturas en rutas vanilla, sin entidad): caballos/burro/mula/caballo
esqueleto/zombi (`horse2/`), panda, slime, stray, wither.

Mobs vanilla puros (se quitó todo): lobo, vaca, champiñaca, calamar, calamar brillante, allay, cabra,
ocelote, husk.

## Tareas pendientes

1. **Pollo** (commit propio): modelo vanilla + capa con cresta, cola, papada y segundo pico. Su cuerpo
   re-rigueado está en otro sistema de coordenadas (comprobar pivotes/giro de `setup`). El usuario
   dice que ahora se ve bien: no romperlo.
2. **Creeper** (commit propio): modelo vanilla + capa con costillas/calavera. Igual: ahora se ve bien.
3. **Enderman**: dientes y lengua al enfadarse. Propuesta pendiente de aprobación: pintarlos en la
   zona `hat` (UV 0,16) de cada skin usando `RP/textures/entity/enderman/enderman_jaw.png`, sin
   geometría (la cara de enfado vanilla sube `head` 5 px y baja `hat` 5 px). La alternativa con capa
   necesita la jerarquía `body` → `head` → `hat` y ajuste con capturas.
4. **Araña**: confirmar con captura qué son las "mini patas al final" (probablemente `spider_fangs`)
   y si la araña gigante se ve bien (15 % de arañas nuevas con BP).
5. **Ahogado**: cuerpo distinto (piernas de 2 px, cabeza 7×7, textura 160×63). Opciones planteadas:
   cuerpo vanilla + algas/aletas como capa; lo mismo y el usuario repinta las 5 skins a 64×64; o
   dejarlo así. El usuario lo aplazó.
6. **Rana**: las skins frías y cálidas (`cold_frog*`, `warm_frog*`) no se usan; el usuario quiere
   recuperarlas más adelante como subvariantes de esas variantes vanilla.
7. **Variantes vanilla en general**: ahora las skins solo salen en la primera variante vanilla; la
   idea futura es tener subvariantes por cada variante vanilla (clima, tipo de gato…).
8. **Compatibilidad con Actions & Stuff**: dos packs no pueden redefinir la misma entidad de cliente.
   Hará falta un parche de compatibilidad o heredar las animaciones de A&S en nuestras entidades.
9. **Sorteo sin BP**: hoy es aleatorio por cliente y cambia al recargar; el usuario quiere estudiar una
   semilla derivada de la posición (no es persistente, pero sería más estable).
10. Revisar si las geometrías de variante completa (zombis caídos, capibara, caracol…) se mantienen
    según la regla de "no sustituir el modelo".
11. **Hallazgos de las herramientas (2026-11-18)**, sin corregir:
    - **Delfín**: `controller.render.mv.dolphin` usa `array.xskins[0]`: siempre sale la primera skin;
      `mv_default2`…`mv_default7` nunca se dibujan (`simulate.py`). No tiene BP.
    - **`pack_icon.png`** de RP y BP miden 274×274; deben ser cuadrados y potencia de 2 (256×256).
    - **Capas con pivote/padre distintos del modelo base** (regla 2): `validate.py` lista ~39. Las
      relevantes: araña (`spider_fangs` y `spider_giant_legs` cuelgan de la raíz en vez de `body0`; en
      reposo se ven bien con `render.py`, pero no seguirían una animación de `body0`, p. ej. de A&S), hoglin (`hoglin_piglinhead*` con pivotes de
      `head`/`body` desplazados), rana (`frog_crown`: `root`/`body` con pivote distinto), sniffer
      (`sniffer_torchflower` desplazado 1,75 en Z), evocador y vindicador (`body` con pivote 12 en vez
      de 24 y padre `waist`), y casi todas las capas del zombi (cuelgan de `spine`, que no existe en
      vanilla). Las de padre `root` cuando vanilla no tiene padre son inofensivas mientras nada anime `root`.
    - Inofensivo: `mv_default2` del pollo (rama de bebé inalcanzable), `mv_empty` del esqueleto wither,
      `mv_ghost` del guardián y `mv_exploding` del dragón no se usan.

## Historial de decisiones

- Persistencia con propiedades `mv:*` en lugar de `minecraft:variant` (choca con vanilla).
- Bebés siempre vanilla (tienen modelos propios nuevos que no encajan con las skins).
- Carpetas `BP/` y `RP/`, versión 5.0.0, `min_engine_version` 1.26.60.
- Sin animaciones propias ni modelos re-rigueados; añadidos como capas (por compatibilidad con A&S).
- Borrados: Rey Esqueleto Wither, modelos WIP sin usar (blastling, watchling, endersent, necrosent,
  hector_salamanca, evoker_costume, piglin_merchant), skins de vaca/champiñaca, BP de la vaca.
- El zombie_pillager.json del BP era el zombie villager v1 vanilla con un sorteo sin uso: borrado.
