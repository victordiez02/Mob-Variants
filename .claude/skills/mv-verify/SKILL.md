---
name: mv-verify
description: Verificar cambios de Mob Variants (RP, BP o tools/) sin entrar al juego - check.py, render.py, contentlog.py, bdstest.py y CI. Úsala después de cualquier cambio en un mob, antes de commit, cuando el usuario reporte un fallo visual o del Content Log, o para revisar la CI.
allowed-tools: Bash(python tools/inventory.py:*), Bash(python -I tools/check.py:*), Bash(python -I tools/validate.py:*), Bash(python -I tools/bpcheck.py:*), Bash(python -I tools/simulate.py:*), Bash(python tools/render.py:*), Bash(python -I tools/contentlog.py:*), Bash(python -m ruff check tools:*), Read(tools/out/*)
---

# Verificar un cambio

Ejecuta en este orden y para en el primer fallo. Todo sale con código 1 si hay errores.

1. `python -I tools/check.py <mob>`: validate + bpcheck + simulate. Debe acabar en `RESULT: OK`.
   - `EXPECTED (vanilla gaps) N` es normal (cosas del juego que faltan en bedrock-samples).
   - Avisos `layer … pivot/parent ≠`: la capa no copia el pivote o el padre del hueso vanilla (regla 2).
   - `format_version 1.10.0 (vanilla 1.8.0)` (INFO): entidad 1.8.0 convertida a propósito (lista
     `animation_controllers`); es normal.
   - `textures never drawn`: la clave `mv_*` no sale en ningún estado (render controller mal o clave sobrante).
   - `BP result depends on local roll`: con BP cada jugador vería algo distinto en esa capa.
   - `texture size does not match the geometry UV`: la proporción del PNG no es la de `texture_width/height`.
2. `python tools/inventory.py <mob>`: actualiza la ficha y dice qué skins dejan piezas vanilla sin pintar
   (saldrían invisibles en el juego). Una skin nueva no debe salir aquí salvo que sea a propósito.
3. `python tools/render.py <mob>` y lee `tools/out/<mob>.png` con Read (sin `-I`: necesita Pillow).
   - Una combinación concreta: `--bp mv:variant=3 --bp mv:mark_variant=1`. Sin BP: `--nobp`.
   - Estados: `--q is_angry=1`, `--q is_saddled=1`, `--q v.ischarging=1`, `--q climate=warm`, `--q is_baby=1`.
   - Vistas: `--view all` (front, back, side, top). Tamaño: `--size 384`. Menos teselas: `--max 6`.
   - Fíjate en: capas descolocadas respecto al cuerpo, caras con la textura de otra zona (UV), partes
     vanilla que deberían ocultarse (`part_visibility`), skins iguales repetidas.
   - Límites: sin movimiento, materiales como alpha-test, pose aproximada con huesos `reset` (enderman).
4. Si cambiaste `tools/`: `python -m ruff check tools` y `npx -y pyright@1.1.400 -p pyrightconfig.json`
   (ejecútalo desde la carpeta scratchpad; los dos a 0).

## Lo que necesita el juego

Solo animaciones en movimiento, materiales/brillo y la confirmación final. Pide al usuario que pruebe
con mobs **recién aparecidos** y dime la hora; luego lee tú el log:
`python -I tools/contentlog.py --since HH:MM` (`--all` incluye [inform]; `--list` lista los logs).

## Comportamiento real del BP (Bedrock Dedicated Server)

`python -I tools/bdstest.py [mob ...] --count 200` (~30 s todos los mobs). Servidor en
`C:/Users/victo/Documents/minecraft_server` (variable `MV_BDS` en `.claude/settings.local.json`; si no
está, pásalo con `--bds`). Úsalo después de tocar cualquier `BP/entities/*.json`.
- Compara el % de cada `mv:*` al aparecer con el esperado del `randomize` y lista errores del servidor
  (carga de packs, JSON, scripts). Debe acabar en `RESULT: OK`.
- Los mobs aparecen a y=64 (superficie): ramas con `filters` de altura/bioma/bebé distintas no se
  prueban y pueden salir como `CHECK`; mira el `filters` del evento antes de tocar nada.
- Solo toca la carpeta del servidor (mundo `mv_test`, packs de desarrollo, `server.properties` con
  copia de seguridad restaurada al final). No lo arranques para otra cosa ni cambies su versión.
- Visual con animaciones en movimiento y separación de capas medida (`bbcheck.py`): skill **mv-blockbench**.
  Tras tocar una capa: `python -I tools/bbcheck.py --measure <mob>` (necesita Blockbench abierto).

## CI

`.github/workflows/checks.yml` (push a main y PR): ruff, pyright, validate, bpcheck, simulate, render
de todos los mobs (artefacto `renders`) y package. Estado: API pública
`https://api.github.com/repos/victordiez02/Mob-Variants/actions/runs?per_page=1` (no hay `gh`).
