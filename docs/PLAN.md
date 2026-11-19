# Plan de trabajo (lista viva)

Marca `[x]` al terminar cada punto y anota el commit. Lo que necesite al usuario va en "Preguntas".
Detalle de cada mob: STATUS.md.

## Fase 0: avisos del editor y arreglos rápidos
- [x] Avisos de la extensión de Minecraft: `.mcignore` + `.mcattributes`; validate comprueba `v.mv_*` (067afd4)
- [x] creeper `mv_TnT` → `mv_tnt`, `bone69` del wither (27b672d)
- [x] `pack_icon.png` de RP y BP a 256×256 (5ba88c3)
- [x] Delfín: usa las 7 skins y BP nuevo con `mv:variant` (98ab7ba, bdstest OK)
- [x] Wither: `wither_armor_blue.png` 64×32 es así en vanilla; simulate ya no avisa de texturas vanilla (011b38e)
- [x] `zombie-villager7.png`: los píxeles fuera del UV no se dibujan; la skin se ve bien. render.py arreglado
      (neverRender y bind_pose_rotation: el aldeano zombi salía vacío) (011b38e)
- [ ] Vindicador: `vindicator9` = `vindicator12` (pregunta 1)

## Fase 1: capas con pivote y padre vanilla (regla 2)
- [x] 33 capas con `geotool relayer` + pig_chest a mano (b289a91). bbcheck --measure: 66 capas, 0 px.
- [x] bbcheck daba ~1 px falso en el sniffer (relative_to no se copiaba) (13ab531)

## Fase 2: modelos re-rigueados
- [ ] araña gigante y "mini patas" (render con `mv:mark_variant=1`)
- [ ] pollo → vanilla + capa (cresta, cola, papada, pico)
- [ ] creeper → vanilla + capa (costillas, calavera, TnT)
- [ ] ahogado (pregunta 2)
- [ ] enderman: dientes/lengua al enfadarse (pregunta 3)

## Fase 3: geometrías de variante completa (pregunta 4)
- [ ] capibara, caracol, pato, oca, ornitorrinco, gatos especiales, zombis caídos 2-5

## Fase 4: funciones nuevas
- [ ] subvariantes por variante vanilla (ranas frías/cálidas…)
- [ ] sorteo sin BP basado en la posición

## Fase 5: compatibilidad con Actions & Stuff

## Fase 6: release 5.0.0 (bdstest de todo, package, tag)

## Limpiezas menores pendientes
- [ ] claves sin uso: `mv_default2` del pollo, `mv_ghost` del guardián, `mv_empty` del esqueleto wither
- [ ] actualizar STATUS.md (tarea 11) con lo resuelto en las fases 0 y 1

## Preguntas para el usuario
1. Vindicador: `vindicator9.png` y `vindicator12.png` son idénticas. ¿Borro una o la recoloreo?
2. Ahogado (aplazado).
3. Enderman: dientes/lengua pintados en la zona `hat` de la skin (sin geometría), ¿sí?
4. Geometrías de variante completa: ¿excepción como el wither o pasarlas a modelo vanilla + capa?
