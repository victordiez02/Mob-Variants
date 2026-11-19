# Plan de trabajo (lista viva)

Marca `[x]` al terminar cada punto y anota el commit. Lo que necesite al usuario va en "Preguntas".
Detalle de cada mob: STATUS.md.

## Fase 0: avisos del editor y arreglos rápidos
- [x] Extensión de Minecraft: `.mcignore` + `.mcattributes`; validate comprueba `v.mv_*` (067afd4, fc8002e)
- [x] Ortografía: `cspell.json` (inglés + español + vocabulario) (fc8002e). Finales de línea: `.gitattributes` (37e1f45)
- [x] creeper `mv_TnT` → `mv_tnt`, `bone69` del wither (27b672d)
- [x] `pack_icon.png` de RP y BP a 256×256 (5ba88c3)
- [x] Delfín: usa las 7 skins y BP nuevo con `mv:variant` (98ab7ba, bdstest OK)
- [x] Wither: `wither_armor_blue.png` 64×32 es así en vanilla; simulate ya no avisa de texturas vanilla (011b38e)
- [x] `zombie-villager7.png`: los píxeles fuera del UV no se dibujan; la skin se ve bien (011b38e)
- [x] Claves sin uso del guardián y del esqueleto wither (fa1ea21); rama de bebé del pollo (con el pollo)
- [ ] Vindicador: `vindicator9` = `vindicator12` (pregunta 1)

## Fase 1: capas con pivote y padre vanilla (regla 2)
- [x] 33 capas con `geotool relayer` + pig_chest a mano (b289a91). bbcheck --measure: 66 capas, 0 px.
- [x] bbcheck daba ~1 px falso en el sniffer (relative_to no se copiaba) (13ab531)

## Fase 2: modelos re-rigueados
- [x] Araña gigante: patas hundidas en el suelo ("mini patas al final"); ahora muslo + articulación como
      el modelo original, pies en y=0 (44f0dc8, bdstest OK)
- [x] Pollo → vanilla + capa chicken_extras (ac5424d)
- [x] Creeper → vanilla + capa creeper_extras; sombreros y TnT reenganchados (c72e5e2)
- [ ] Ahogado (pregunta 2)
- [ ] Enderman: dientes/lengua al enfadarse (pregunta 3)

## Fase 3: geometrías de variante completa (pregunta 4)
- [ ] capibara, caracol, pato, oca, ornitorrinco, gatos especiales, zombis caídos 2-5, creeper esqueleto

## Fase 4: funciones nuevas
- [x] Ranas frías y cálidas con sus skins (2781464)
- [ ] Más subvariantes por variante vanilla (gatos, zorro ártico, pollo/cerdo/vaca de otros climas…):
      solo si hay skins para ellas
- [x] Sorteo sin BP por posición: estudiado, **no compensa**. `initialize` se ejecuta cuando cada
      cliente carga la entidad, y para entonces el mob ya se ha movido: dos jugadores (o el mismo tras
      recargar) leerían posiciones distintas. Solo coincidiría con mobs quietos. La solución real es el BP.

## Fase 5: compatibilidad con Actions & Stuff (pregunta 5)

## Fase 6: release 5.0.0
- [ ] Prueba en el juego de lo cambiado (pregunta 6)
- [ ] bdstest de todos los mobs, package, tag v5.0.0

## Preguntas para el usuario
1. Vindicador: `vindicator9.png` y `vindicator12.png` son idénticas. ¿Borro una o la recoloreo?
   Pollo: `chicken2.png` es un pollito (skin de bebé) y los bebés son vanilla: ¿lo borro?
2. Ahogado (aplazado).
3. Enderman: dientes/lengua pintados en la zona `hat` de la skin (sin geometría), ¿sí?
4. Geometrías de variante completa: ¿excepción como el wither o pasarlas a modelo vanilla + capa?
5. Actions & Stuff: hace falta su pack (versión actual) para ver qué entidades redefine.
6. Probar en el juego (Content Log incluido).
