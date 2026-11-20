# Compatibilidad con Actions & Stuff (A&S)

Estado: **prueba con el zombi** (rama `ans-compat`). Analizado con A&S 1.1.68.

## Cómo es A&S

- Solo resource pack (sin BP): el BP de Mob Variants no choca con nada.
- Redefine 117 entidades de cliente, entre ellas **todas las de Mob Variants**, con modelos, animaciones y
  render controllers propios y ofuscados (`geometry.oreville_ans.*`, `v.cdrzno`…). Los nombres pueden
  cambiar en cada versión de A&S (sospecha: solo hemos visto una).
- Modelos re-rigueados: huesos propios (el cerdo tiene `root` y patas `d680…`); el zombi conserva casi
  todos los nombres vanilla. **Las capas con huesos de nombre vanilla (regla 2) no siguen sus animaciones**
  en la mayoría de mobs.
- Tres subpacks con entidades distintas: SP0 (texturas vanilla, UV vanilla en casi todos los mobs),
  SP1 y SP2 (texturas propias en muchos mobs, a veces de otro tamaño).
- Las entidades de cliente no se fusionan entre packs: para cada mob gana la del pack de más arriba.
  Molang no puede saber si otro pack está activo.

## Cómo se hace compatible

`tools/ans_patch.py` genera **en local** un tercer pack, `dist/MV_ANS_RP` (ignorado por git: nada de A&S
entra en el repo), a partir del A&S que tenga el usuario y del subpack que use:

- Entidad de A&S + nuestras claves `mv_*`, el sorteo (`initialize`) y la puerta (`pre_animation`).
- Su render controller del cuerpo con `!v.mv_active` y una copia nuestra, `controller.render.mv.ans.<mob>`,
  donde solo cambia `Texture.default` por `array.mv_skins[...]`, con `v.mv_active`.
- Piezas que A&S dibuja y el vanilla no (cubos extra): esas zonas de la skin toman los píxeles de la textura
  vanilla (copias en `textures/mv_ans/<mob>/`). En el zombi son las hombreras y los pies, que usan la zona
  del sombrero; el modelo de A&S no tiene sombrero, así que las skins con sombrero lo pierden.
- Solo se admiten mobs cuyo `Texture.default` de A&S sea la textura vanilla y cuyo render controller propio
  use solo `array.mv_skins`; el resto se salta con el motivo.

Orden de packs: **MV x A&S** arriba, **A&S** en medio y **Mob Variants RP** abajo (si MV estuviera encima de
A&S, sus entidades taparían las de A&S de los mobs aún no fusionados). BP de Mob Variants como siempre.
Con cada versión nueva de A&S: volver a ejecutar la herramienta.

```
python tools/ans_patch.py zombie --subpack SP0 --install
```

## Pendiente

- Prueba en el juego del zombi (skins, animaciones de A&S, bebés de A&S, hombreras sin restos del sombrero).
- Si funciona: resto de mobs de SP0, y ver SP1/SP2 (texturas propias de A&S: haría falta adaptar skins).
- Sombreros y demás capas: sobre los huesos de A&S, mob a mob.
- Distribuir el pack generado necesitaría permiso de Oreville (contiene sus entidades).
