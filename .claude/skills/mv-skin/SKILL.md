---
name: mv-skin
description: Añadir o cambiar skins, cosméticos (capas) o mobs en Mob Variants - addskin.py, capas con huesos vanilla, render controllers y BP. Úsala cuando el usuario pase una textura nueva, pida un sombrero/accesorio, una variante nueva o un mob nuevo.
allowed-tools: Bash(python -I tools/addskin.py:*), Bash(python -I tools/check.py:*), Bash(python tools/render.py:*), Bash(python -I tools/simulate.py:*), Bash(python -I tools/geotool.py:*), Read(tools/out/*)
---

# Skins, capas y mobs

Antes: lee la ficha del mob (`docs/mobs/<mob>.md`). Reglas en CLAUDE.md (modelo vanilla, capas, `mv_*`,
regla 7: los extras vuelven de uno en uno con la skill **mv-mob**).

## Skin nueva (patrón estándar)

`python -I tools/addskin.py <mob> <png> --dry-run`, revisa y repite sin `--dry-run`.
Hace las 5 cosas: copia el PNG a `RP/textures/entity/<mob>/`, clave `mv_defaultN` en la entidad,
`Texture.mv_defaultN` al final del array del render controller y, si el array se lee como
`[v.mv_variant - 1]`, sube el `N` del sorteo local de la entidad, amplía el `range` de `mv:variant` y
añade `{weight, set_property}` a cada randomize del BP.
Opciones: `--array array.yskins` (otro array, p. ej. ensillado), `--key`, `--weight N`.
Si dice que el patrón no es estándar o que no encuentra el randomize, edítalo a mano.
Después: skill mv-verify con `--bp mv:variant=<N que imprime>`.

La textura debe tener la proporción del UV de la geometría (64×64 o 64×32 según el modelo vanilla
actual vs. antiguo): `simulate.py` lo avisa.

## Cosmético como capa (sombrero, flor, colmillos…)

1. Geometría `geometry.mv.<mob>_<cosa>` en `RP/models/entity/`, formato ≥ 1.12. Huesos raíz con
   **nombre, pivote y padre del hueso vanilla** (cópialos de `vanilla/resource_pack/models/entity/`);
   piezas propias como hijos `mv_*`. Para generarla desde un modelo antiguo: `build_overlay()` de
   `tools/geotool.py`.
2. Claves `mv_<cosa>` en `geometry`/`textures` de la entidad; render controller
   `controller.render.mv.<mob>_<cosa>` con `Geometry.mv_empty` (`geometry.mv.zombie_empty`) cuando
   no toca; condición en la entidad (`v.mv_active && …`).
3. Si debe guardarse con BP: `mv:mark_variant` (o el valor que ya use el mob) en el randomize.
4. Ocultar una pieza vanilla: `part_visibility` en el render controller.
5. mv-verify: validate no debe dar avisos de esa capa; renderiza con `--view all`.

## Mob nuevo

Pasos en docs/ARCHITECTURE.md ("Cómo añadir un mob nuevo"). Copia la entidad vanilla actual
(`format_version` igual), materiales solo vanilla, `v.mv_active` si tiene bebé o variantes vanilla.

## Skins de un modelo re-rigueado

`python -I tools/geotool.py fit` (qué % encaja en cada modelo vanilla) y
`faces <geo addon> <geo vanilla> [hueso=huesoVanilla]`. Extremidades partidas:
`python tools/geotool.py limbmerge …` (modifica PNGs: commit antes).
