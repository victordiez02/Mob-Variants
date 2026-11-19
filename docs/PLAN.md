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
- [x] Vindicador: `vindicator12` (= `vindicator9`) y pollito `chicken2` borrados (fd9f12e)

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

## Fase 3: geometrías de variante completa
- [x] Huesos renombrados a los vanilla (`geotool rebone`), sin párpados: capibara, pato, oca,
      ornitorrinco, gatos especiales, creeper esqueleto (1251f9b). Zombie2-5 conservan sus huesos y su
      animación de arrastrarse (be1cf62)
- [x] Entidades reconstruidas desde la vanilla: 0 animaciones propias salvo wither y zombi (1251f9b)
- [x] Vindicador/evocador: `part_visibility` vanilla (dos pares de brazos); zombi con una propiedad por
      rasgo (be1cf62); aldeano con una capa por profesión (c080ca9)
- [ ] Oveja sin hocico (pregunta 4)

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
1. (resuelta: duplicados borrados)
2. Ahogado (aplazado).
3. Enderman: dientes/lengua pintados en la zona `hat` de la skin (sin geometría), ¿sí?
4. Oveja: captura del hocico que falta, junto a una oveja vanilla.
5. Actions & Stuff: hace falta su pack (versión actual) para ver qué entidades redefine.
6. Probar en el juego (Content Log incluido).
