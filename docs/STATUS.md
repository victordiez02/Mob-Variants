# Estado del proyecto

Última actualización: 2026-11-19 (versión del pack 5.0.0, objetivo Minecraft 1.26.60, rama `skins-base`).

## Resumen

- **Base solo de skins** (commit `feat!: base solo de skins`): 29 mobs con skins aleatorias sobre su entidad
  vanilla, con RP solo o RP + BP (`mv:variant`). Comprobado con `check.py` (validate, bpcheck, simulate) y con
  `bdstest.py` (BDS real: todos los mobs reciben su `mv:variant` dentro del rango, sin errores del servidor).
  **Falta la prueba en el juego.**
- Estado detallado de cada mob: [docs/mobs/](mobs/README.md) (tabla con número de skins y skins a revisar).
- Todo lo anterior (capas, variantes de modelo completo, animaciones propias, mecánicas del BP) está en la
  etiqueta `legacy-v5` y descrito en la sección "Antes" de cada ficha.

Mobs vanilla de momento (sin skins del cuerpo que encajen): gato, zorro, oveja (solo retextura), ahogado,
aldeano, wither, araña de cueva. Retexturas puras: caballos, burro, mula, caballo esqueleto/zombi, panda,
slime, stray, oveja.

## Aplazado por el usuario (recordárselo)

- **Ahogado**: cuerpo distinto (piernas de 2 px, cabeza 7×7, textura 160×63). Ver docs/mobs/drowned.md.
- **Enderman**: dientes y lengua al enfadarse. Ver docs/mobs/enderman.md.

## Historial de decisiones

- 2026-11-19: tras muchos fallos en el juego con capas y modelos heredados, el usuario decide rehacer el
  add-on **mob por mob desde la base vanilla**: primero solo skins, luego cada extra de uno en uno, probado
  en el juego (regla 7). Fichas por mob generadas con `tools/inventory.py`; trabajo por mob con la skill
  `mv-mob` (pensada para lanzar una conversación o agente por mob).
- Persistencia con propiedades `mv:*` en lugar de `minecraft:variant` (choca con vanilla). `mv:variant = 0`
  significa "sin skin guardada" (mob anterior al BP) y se ve vanilla.
- Bebés siempre vanilla (tienen modelos propios nuevos que no encajan con las skins).
- Carpetas `BP/` y `RP/`, versión 5.0.0, `min_engine_version` 1.26.60.
- Sin animaciones propias ni modelos re-rigueados (compatibilidad con A&S). Únicas excepciones admitidas
  cuando vuelvan: zombi que se arrastra y wither (animación propia de su geometría).
- Variantes de modelo completo: segunda geometría dibujada en lugar del cuerpo, con huesos de nombre vanilla
  (decidido frente a un attachable encima: las proporciones son distintas).
- Borrados antes de `legacy-v5`: Rey Esqueleto Wither, modelos WIP sin usar, skins de vaca/champiñaca,
  duplicados `vindicator12` y `chicken2` (pollito).
- Sorteo sin BP por posición: estudiado, **no compensa** (`initialize` se ejecuta cuando cada cliente carga la
  entidad; dos jugadores leerían posiciones distintas).
