---
name: mv-blockbench
description: Usar Blockbench (MCP blockbench) en Mob Variants - ver una variante con sus capas y animaciones vanilla en movimiento, comprobar que los cosméticos siguen a los huesos, ajustar o crear capas (huesos con nombre/pivote vanilla) y pintar texturas. Úsala cuando render.py no basta (animaciones, edición visual) o el usuario pida revisar algo en Blockbench.
allowed-tools: Bash(python -I tools/bbscene.py:*), Bash(python -I tools/bbapply.py:*), Bash(curl -s -m 3 http://127.0.0.1:8787/ping), mcp__blockbench__get_status, mcp__blockbench__execute_script, mcp__blockbench__screenshot, mcp__blockbench__screenshot_views, mcp__blockbench__list_outliner, mcp__blockbench__get_element, mcp__blockbench__list_animations, mcp__blockbench__list_textures, mcp__blockbench__get_texture, mcp__blockbench__check_model, mcp__blockbench__get_orientation, mcp__blockbench__which_side, mcp__blockbench__set_camera_angle, Read(tools/out/*)
---

# Blockbench en este proyecto

Para qué SÍ: (1) ver una variante como en el juego **con animaciones vanilla en movimiento** (lo que
`render.py` no hace) y comprobar que las capas siguen al cuerpo (regla 2, compatibilidad A&S);
(2) ajustar pivotes/padres o crear piezas de una **capa** `geometry.mv.*`; (3) pintar/corregir texturas.
Para qué NO: modelar mobs nuevos, crear animaciones o rigs (regla 1: modelo y animaciones vanilla),
`find_references`/paletas/`detail_cubes`/generadores (engranajes, pelo, alas…), `pack_uv` (rompe el UV
vanilla de las skins), `install_plugin`/`uninstall_plugin` (denegados), exportar a glTF.

## 0. ¿Está levantado? (no lo arranques tú: está prohibido)

`curl -s -m 3 http://127.0.0.1:8787/ping` debe dar `{"ok":true,…}` y deben existir las herramientas
`mcp__blockbench__*`. Si no, para y pide al usuario exactamente:
1. "Abre **Blockbench** (escritorio). Debe salir el aviso *MCP server started on port 8787*; si no,
   menú **Tools ▸ Start MCP Server**."
2. Si el ping va pero no tienes las herramientas: "Ejecuta `/mcp` en Claude Code y reconecta
   **blockbench** (o reinicia la sesión)."

## 1. Cargar una variante (base + capas + texturas + animaciones)

1. `python -I tools/bbscene.py <mob> [--bp mv:variant=N] [--bp mv:mark_variant=M] [--q is_angry=1]`
   (mismas opciones que render.py). Imprime la línea `execute_script` a usar.
2. `mcp__blockbench__execute_script` con ese código. Devuelve capas cargadas, `shared_bones` (huesos de
   capa que reciben la animación del hueso vanilla del mismo nombre) y `always_playing`.
   Blockbench renombra huesos repetidos (`head` → `head2`): es normal, el cargador lo tiene en cuenta.
3. Pose + animación: `execute_script` `return mvPose('animation.quadruped.walk', 0.3)` y luego
   `screenshot` (`view`: front, back, left, right, front_right, top) o `screenshot_views`.
   **No uses `preview_animation`**: reproduce solo una animación y pierde la pose (`setup`).
   Nombres de animaciones: `list_animations` o el informe del paso 2. `mvPose(null, 0)` = reposo.
4. Qué mirar: piezas `mv_*` que se separan del cuerpo al moverse (padre o pivote distinto del vanilla),
   cosas flotando, caras con la textura equivocada. `check_model` lista z-fighting/flotantes (en
   modelos vanilla algunos avisos son normales).

Es un proyecto temporal: **nunca** `save_project`/`export_project` sobre archivos del repo.

## 2. Corregir o crear una capa

1. Carga la variante (paso 1). Inspecciona con `list_outliner` / `get_element`.
2. Edita con `edit_element` (pivote, padre, rotación) o añade piezas con `add_group`/`add_cube`
   **dentro** de los grupos de esa capa, como hijos `mv_*` (lados: el modelo mira a -Z; usa
   `get_orientation`/`which_side`, no la imagen). Los huesos raíz de la capa deben copiar nombre,
   pivote y padre del hueso vanilla (validate lo comprueba).
3. `execute_script` `return mvExportLayer('geometry.mv.<capa>')` → escribe
   `tools/out/bb/<capa>.export.json`.
4. `python -I tools/bbapply.py geometry.mv.<capa> --dry-run`, revisa, repite sin `--dry-run`
   (solo geometrías `geometry.mv.*` en formato 1.12; mantiene el estilo del repo).
5. Skill mv-verify (`check.py <mob>`, `render.py`) y vuelve a cargar para verlo animado.

## 3. Texturas

Las texturas cargadas **son los PNG del repo**: `paint_texture`/`paint_faces` + guardar la textura
(`execute_script` `Texture.all.find(t=>t.name=='x.png').save()`) los modifica. Haz commit antes y
revisa con `get_texture`. No cambies el tamaño de una skin sin mirar el `texture_width/height` de su
geometría (simulate avisa si no encaja). Para la boca del enderman o repintar el ahogado (STATUS),
pinta sobre las zonas UV de la textura vanilla (`paint_faces` usa coordenadas de cada cara).

## 4. Revisión del usuario

`request_review` muestra vistas en el panel de Blockbench y espera su veredicto: úsalo para lo que
quieras que confirme él en vez de entrar al juego.
