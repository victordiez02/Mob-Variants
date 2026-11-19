---
name: mv-mob
description: Trabajar UN mob de Mob Variants sobre la base solo de skins - revisar sus skins, arreglar las que no pintan el modelo vanilla y recuperar de uno en uno los extras de legacy-v5 (capas, variantes de modelo completo, mecánicas del BP). Úsala cuando el usuario pida trabajar un mob concreto o se lance una conversación/agente para un mob.
allowed-tools: Bash(python tools/inventory.py:*), Bash(python -I tools/check.py:*), Bash(python tools/render.py:*), Bash(python -I tools/simulate.py:*), Bash(python -I tools/addskin.py:*), Bash(python -I tools/geotool.py:*), Bash(python tools/texuv.py:*), Bash(git show legacy-v5:*), Bash(git diff:*), Bash(git status:*), Bash(git log:*), Read(tools/out/*), Read(docs/mobs/*)
---

# Trabajar un mob

Una conversación (o agente) = **un mob**. La base es solo de skins (CLAUDE.md, regla 7); todo lo demás
está en la etiqueta `legacy-v5` y vuelve **de uno en uno**, cuando el usuario lo pida y tras probarlo él.

## 1. Contexto (no lo redescubras)

1. Lee `docs/mobs/<mob>.md` entera: estado actual, notas (fallos vistos en el juego), "Antes" y plan.
2. Lee docs/ARCHITECTURE.md si vas a tocar la entidad, el render controller o el BP.
3. `python tools/inventory.py <mob>` para tener la ficha al día (no edites a mano la sección generada).

## 2. Qué archivos puedes tocar

Solo los del mob: `RP/entity/<mob>.entity.json`, `RP/render_controllers/<mob>.render_controllers.json`,
`BP/entities/<archivo>.json`, `RP/textures/entity/<carpeta del mob>/`, las geometrías/animaciones que
recuperes para él (`RP/models/entity/…`, `RP/animations/…`) y `docs/mobs/<mob>.md`.
- Hay carpetas de texturas compartidas (`illager/` evocador + devastador, `piglin/` piglin + bruto,
  `skeleton/` esqueleto + wither esqueleto + stray): no borres ni renombres lo que use otro mob
  (búscalo con Grep en `RP/entity/`).
- Lo general (tools/, CLAUDE.md, ARCHITECTURE, STATUS, PLAN, skills) **no** se toca desde una conversación de
  mob: si hace falta, propónselo al usuario y anótalo en la ficha.
- Otras conversaciones pueden estar trabajando otros mobs a la vez: no hagas `git add -A` ni toques archivos
  ajenos; añade a git solo tus rutas.

## 3. Revisar las skins de la base

- Columna "Revisar" de la ficha: piezas que la skin deja casi sin pintar (saldrían invisibles).
  `python tools/render.py <mob> --bp mv:variant=N --view all` y mira el PNG. Si es a propósito (máscara sin
  nariz), añádela a la línea `` - Revisadas (a propósito): `<textura>`, … `` de las notas (inventory deja de
  contarla); si está rota: arréglala (skill `mv-texture`: `texuv.py retarget`, rellenar
  desde otra parte de la misma skin solo en píxeles transparentes) o sácala de la base.
- Sacar una skin: quita su clave y su entrada del array, renumera (las siguientes bajan uno), baja el `N`
  de `math.random_integer(1, N)`, el `range` y cada `randomize` del BP. Después `check.py` y `inventory.py`.
- Skins nuevas: skill `mv-skin` (`addskin.py`).

## 4. Recuperar un extra de legacy-v5 (solo si el usuario lo pide)

1. Elige **uno** de la sección "Antes" de la ficha y díselo al usuario antes de empezar.
2. Trae los archivos: `git show legacy-v5:<ruta> > <ruta>` (geometría, textura, animación). No traigas la
   entidad ni el render controller antiguos enteros: añade a los actuales solo lo necesario.
3. Rehazlo con las reglas actuales (CLAUDE.md): capa = huesos con nombre, pivote y padre vanilla
   (`geotool relayer`) y piezas `mv_*`; variante de modelo completo = huesos renombrados a los vanilla
   (`geotool rebone`); render controller propio con la `part_visibility` vanilla; propiedad del BP nueva
   `mv:<rasgo>` con su `randomize` (nunca dependas de otra propiedad sorteada en el mismo evento).
4. Comprueba lo que el inventario o la ficha avisen para ese extra (brazos cruzados, objetos en la mano,
   poses: zombi tumbado, aldeano con brazos cruzados…).
5. Skill `mv-verify` (check, inventory, render) y, si hay BP, `bdstest.py <mob>`.

## 5. Cerrar

1. Actualiza las notas y el plan de la ficha (qué se hizo, qué falta, qué debe probar el usuario).
2. Commit atómico solo con tus rutas: `fix(<mob>): …` / `feat(<mob>): …` (skill `mv-release` para el estilo).
3. Pide al usuario la prueba en el juego con mobs **recién aparecidos** y concreta qué mirar. Lo que vea va
   a las notas de la ficha. Si algo falla en el juego y no lo explican las herramientas, apúntalo como
   sospecha con la prueba que la apoya, no como hecho.
