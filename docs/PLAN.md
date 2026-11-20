# Plan de trabajo (lista viva)

Marca `[x]` al terminar cada punto y anota el commit. El detalle por mob está en su ficha
([docs/mobs/](mobs/README.md)); aquí solo lo general. Lo que necesite al usuario va en "Preguntas".

## Fase A: base solo de skins (rama `skins-base`)
- [x] Etiqueta `legacy-v5` con el add-on completo anterior
- [x] Inventario por mob: `tools/inventory.py` + fichas `docs/mobs/*.md` con lo que había en `legacy-v5`
- [x] Base: entidad vanilla + `controller.render.mv.<mob>` (copia del vanilla, solo cambia la textura) + BP con
      `mv:variant`; skins pintadas para otros modelos fuera. check OK, bdstest OK (29 mobs)
- [x] `addskin.py` adaptado (sorteo local con N, varios `randomize`); skill `mv-mob`
- [ ] **Prueba en el juego de la base** (pregunta 1)
- [ ] Revisar las skins marcadas en "Revisar" de las fichas (narices, orejas, aletas, sombrero de la bruja…)
- [ ] Fusionar `skins-base` en `main` cuando la base esté probada

## Fase B: extras de uno en uno (skill `mv-mob`, una conversación/agente por mob)
Orden propuesto (de menos a más riesgo); el usuario elige qué vuelve:
1. Capas simples que no dependen de la pose: corona de la rana, rosa del gólem, flores del sniffer, sombreros.
2. Capas sobre extremidades: armaduras del vindicador (¿brazos cruzados?), colmillos y patas de la araña.
3. Variantes de modelo completo: pato y oca, capibara y caracol, ornitorrinco, gatos, creeper esqueleto.
4. Zombi: mandíbula rota, minero, espadas y flechas, zombi que se arrastra (con su animación).
5. Aldeano (accesorios por profesión con brazos cruzados), wither (modelo y animación propios).
Antes de las capas de mobs con objetos en la mano: comprobar con la base si el hacha del vindicador y la
espada del esqueleto wither se ven (ver sus fichas).

## Fase C: compatibilidad con Actions & Stuff (rama `ans-compat`, docs/ANS.md)
- [x] Análisis de A&S 1.1.68 y `tools/ans_patch.py` (pack local fusionado)
- [ ] Prueba en el juego del zombi (SP0)
- [ ] Resto de mobs de SP0; SP1/SP2

## Fase D: release
- [ ] bdstest de todos los mobs, package, tag

## Preguntas para el usuario
1. Probar la base en el juego con mobs **recién aparecidos** (Content Log incluido).
2. Actions & Stuff: probar el zombi con el pack generado (docs/ANS.md).
3. Ahogado y enderman: aplazados (recordar).
