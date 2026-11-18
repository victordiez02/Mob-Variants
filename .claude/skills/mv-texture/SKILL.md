---
name: mv-texture
description: Hacer, adaptar y revisar texturas (skins y cosméticos) de Mob Variants - plantillas UV, pasar una skin de un modelo antiguo/re-rigueado al UV vanilla, recolorear variantes, detectar píxeles perdidos, y pintar/retocar sobre el modelo en Blockbench. Úsala cuando haya que crear o modificar un PNG, migrar skins de modelo, o el usuario quiera pintar él.
allowed-tools: Bash(python tools/texuv.py:*), Bash(python tools/render.py:*), Bash(python -I tools/bbscene.py:*), mcp__blockbench__get_texture, mcp__blockbench__list_textures, mcp__blockbench__screenshot, mcp__blockbench__execute_script, mcp__blockbench__make_palette, Read(tools/out/*)
---

# Texturas

Primero lo determinista (Python, sin Blockbench, sin gastar tokens en mirar); Blockbench solo para pintar
a ojo sobre el modelo. Los PNG nuevos van a `tools/out/tex/` hasta que el usuario los apruebe; después
se copian a `RP/textures/entity/<mob>/` (o se usa `addskin.py`, skill mv-skin). Commit antes de
modificar un PNG del repo.

## Scripts (`python tools/texuv.py …`, necesitan Pillow: sin `-I`)

| Orden | Para qué |
|---|---|
| `template <geometry> [textura]` | PNG con cada cara contorneada (rojo north, azul south, amarillo east, verde west, blanco up, morado down) y el nombre del hueso. Para el usuario si pinta a mano, o para saber qué píxeles usa una cara. |
| `retarget <geo origen> <geo destino> <textura> [hueso=hueso[+hueso2]…]` | Crea la textura para otro modelo copiando cara a cara lo que se ve en el mismo hueso. `leg0=leg0+knee` une extremidades partidas. Informa de caras reescaladas, caras sin origen (pintar a mano) y **huesos del origen sin sitio** en el destino (candidatos a capa). Así se migran gallina, creeper, ahogado y similares (STATUS). |
| `recolor <textura> [--hue G] [--sat F] [--val F] [--like otra]` | Variante de color: desplazamiento HSV y/o colores de otra skin (`--like`, p. ej. la vanilla fría o cálida). |
| `lint [mob…] [--min 20]` | Píxeles opacos fuera de toda cara (trabajo que no se ve) y semitransparentes (con materiales alpha-test se ven del todo o nada). Falsos positivos: texturas de otro mob reutilizadas para un cosmético (`iron_golem2` en la flor) y mobs con materiales con transparencia (dragón). |

Texturas: como en las entidades (`textures/entity/pig/pig`) o ruta a archivo. Geometrías: IDs
(`geometry.pig`, `geometry.mv.chicken`; los IDs están en la entidad y en las etiquetas de render.py).

Comprobar el resultado sin tocar el pack: renderizar la geometría con el PNG nuevo. Mientras no exista
una opción para ello en render.py, copia temporalmente el PNG a su ruta del pack, ejecuta
`render.py <mob> --bp …` y restaura con git; o cárgalo en Blockbench (abajo).

## Pintar sobre el modelo (Blockbench, skill mv-blockbench para arrancar y cargar)

1. `python -I tools/bbscene.py <mob> --bp …` y `execute_script` con la línea que imprime.
2. Cubo por **uuid** (Blockbench nombra los cubos como su hueso y la cabeza puede tener varios):
   `execute_script` `return Cube.all.filter(c=>c.name=='head').map(c=>[c.uuid,c.size()])`.
3. `paint_faces` con `{cube: uuid, face: 'north', ops: [{type:'rect', x, y, width, height, color}]}`
   (coordenadas relativas a la cara; otros tipos de op: los de `paint_texture`). Detalles de cara
   (ojos, boca, dientes) también con `paint_face`.
4. `mvPose(null, 0)` antes de cada `screenshot` (la captura vuelve al modo edición y pierde la pose).
5. Mientras no se guarde, todo está en memoria: para descartar, vuelve a cargar la escena. Para
   guardar en el PNG del repo: `execute_script` `Texture.all.find(t=>t.name=='pig.png').save()`.
   Antes, commit; después, `git diff --stat` y skill mv-verify.
6. Colores que casen con el mob: `make_palette` sobre la textura vanilla o la skin base.

## Cosmético nuevo con textura propia

Geometría de capa (skill mv-skin) + textura propia: en Blockbench `create_texture` (tamaño potencia de
2) y `pack_uv` **solo** sobre los cubos de esa capa nueva (nunca en geometrías con skins del pack: les
cambia el UV). `set_cube_uv` para colocar una pieza en una zona libre de una textura existente.
Formas: `add_plane` (flores/hojas en cruz como las vanilla), `voxelize_matrix` (piezas pixel art:
espadas, flechas, emblemas), `mirror_element` (simétricos). `detail_cubes` solo como base, su estilo
no es vanilla. Después `mvExportLayer` + `bbapply.py` (skill mv-blockbench) y guardar la textura.

## No

`resize_texture` para "arreglar" una skin con otro UV (usa `retarget`); texturas emisivas o
`create_vfx_texture` (no hay materiales propios); referencias de Internet (denegadas).
