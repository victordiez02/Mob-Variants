# Herramientas (`tools/`)

Scripts Python ≥ 3.12. Solo `render.py`, `inventory.py` (cobertura), `texuv.py` y `geotool.py limbmerge` necesitan **Pillow**
(`pip install pillow`); el resto no tiene dependencias. Leen el repo y la plantilla `vanilla/`, y se
pueden ejecutar desde cualquier carpeta. `-I` aísla Python de módulos externos; no lo uses con los
scripts que necesitan Pillow si está instalado en el usuario.

## Uso diario

```bash
python -I tools/check.py [mob ...]      # todo lo estático: validate + bpcheck + simulate (resumen)
python tools/render.py <mob>            # imágenes de las variantes -> tools/out/<mob>.png
python -I tools/contentlog.py --since 20:10   # errores del Content Log del juego, agrupados
python -I tools/addskin.py <mob> <png>        # skin nueva en entidad, render controller y BP
```

Todos devuelven código 1 si hay errores.

| Script | Para qué |
|---|---|
| `check.py [mob ...]` | Lanza `validate`, `bpcheck` y `simulate` (este último solo para los mobs indicados, o todos) y muestra errores y avisos. |
| `validate.py [--all]` | RP: referencias rotas (texturas, geometrías, animaciones, render controllers, `Texture./Geometry./Material.` sin definir) y las **trampas de CLAUDE.md**: `format_version` menor que la vanilla, lista `animation_controllers`, materiales que no son vanilla, `q.property('mv:…')` sin `q.has_property`, variables `v.mv_*`/`v.xvar` usadas sin asignar, IDs vanilla redefinidos o fuera del namespace `mv`, **huesos de capas con pivote o padre distintos del modelo base** (regla 2) y `pack_icon` que no es potencia de 2. `--all` lista además los archivos sin usar (las texturas en rutas vanilla cuentan como retexturas). |
| `bpcheck.py` | BP: grupos y eventos que no existen, propiedades `mv:*` sin declarar, fuera de rango o sin `client_sync`, lógica en `minecraft:add_attributes` y **regla 5**: componentes, grupos, eventos y propiedades vanilla idénticos al archivo vanilla actual (solo se permiten añadidos `mv:` y eventos del motor como `minecraft:entity_spawned`). Las desviaciones documentadas están en `ALLOWED_DIFFS`. |
| `simulate.py [mob ...] [--detail]` | Ejecuta los scripts de la entidad y evalúa los render controllers (intérprete de Molang propio) para los 100 valores del sorteo sin BP y para cada resultado del `randomize` de `minecraft:entity_spawned` con BP. Por capa, cuántas combinaciones (geometría, texturas) distintas salen (1 = no varía). Avisa de **claves `mv_*` que nunca se dibujan** (probando también enfadado, ensillado, domesticado, profesiones, clima…), de capas que **con BP siguen dependiendo del sorteo local** y de errores de Molang. `--detail` da la probabilidad de cada resultado con los pesos reales del BP. Con muchas propiedades (zombi) usa los 1500 resultados más probables más el más probable de cada valor (`mvsim.capped`); render.py igual. |
| `render.py <mob> [opciones]` | Renderizador por software: dibuja cada combinación distinta (de más a menos probable) con todas sus capas, `part_visibility` y la pose estática de las animaciones de la entidad. Opciones: `--nobp`, `--bp mv:variant=3`, `--q is_angry=1`, `--q climate=warm`, `--view front\|back\|side\|top\|all`, `--max N`, `--size PX`, `--nopose`, `--out`. Ver detalles en la cabecera del script. |
| `contentlog.py [--since HH:MM] [--all] [--list] [--file F]` | Lee el Content Log más reciente de `%APPDATA%\Minecraft Bedrock\logs`, solo errores y avisos, agrupando los repetidos. |
| `geotool.py fit \| faces \| limbmerge \| relayer \| rebone` | Pasar skins de modelos re-rigueados al modelo vanilla: `fit` (qué % del UV del modelo propio cae dentro de cada modelo vanilla), `faces <geo addon> <geo vanilla> [hueso=huesoVanilla …]` (cara a cara), `limbmerge <geo addon> <geo vanilla> <texturas…>` (recoloca extremidades partidas; **modifica las texturas**), `relayer` (copia a una capa el pivote, padre y rotación vanilla) y `rebone <geo variante> <geo base> [viejo=nuevo …] [--drop=a,b] [--write]` (variantes de modelo completo: renombra los huesos a los vanilla para que los muevan las animaciones vanilla, pasa el resto a `mv_`, quita los de `--drop` con sus hijos y conserva los pivotes propios). Como módulo, `build_overlay()` genera capas a partir de huesos de un modelo antiguo (ver `refactor(witch)`, `refactor(spider)`, `refactor(pig)` en git). |
| `addskin.py <mob> <png> [--array A] [--key K] [--weight W] [--dry-run]` | Añade una skin en todos los sitios: copia el PNG, clave `mv_defaultN` en la entidad, entrada en el array del render controller y, si el array se lee como `[v.mv_variant - 1]`, el `N` del sorteo local (`v.xvar = math.random_integer(1, N)`) y el `range` y todos los `randomize` del BP. Avisa si el mob tiene un segundo array (abeja enfadada, ghast, cerdo con silla). Conserva el formato de los archivos (diffs mínimos). |
| `inventory.py [mob ...] [--quiet]` | Ficha de cada mob en `docs/mobs/<mob>.md` (solo la sección entre `<!-- inventory:start -->` y `<!-- inventory:end -->`; el resto se escribe a mano) y tabla de `docs/mobs/README.md`: entidad vanilla, puerta, skins en orden de `mv:variant` con su peso en el BP, eventos con sorteo y **cobertura** de cada skin (piezas que la textura vanilla pinta y la skin deja por debajo del 60 %: saldrían invisibles; ignora capas exteriores con `inflate`). Imprime las skins con problemas. Necesita Pillow. |
| `package.py` | Comprueba que los manifests concuerdan (versiones, dependencia BP → RP) y genera `dist/MobVariants_RP_<v>.mcpack`, `…_BP_<v>.mcpack` y `MobVariants_<v>.mcaddon`. |
| `bdstest.py [mob ...] [--bds DIR] [--count N] [--y 64] [--keep]` | Prueba el BP en el motor real con Bedrock Dedicated Server (`MV_BDS` = carpeta del servidor): mundo plano nuevo con RP, BP y el BP de pruebas `tools/bds/mv_test_bp` (Script API), hace aparecer cada mob N veces y compara el % de cada `mv:*` con el esperado del `randomize`, además de listar los errores del servidor. `--y`: altura de aparición (`--y 10` para ramas bajo tierra, como los zombis mineros). Solo toca la carpeta del servidor (copia de seguridad de `server.properties`). |
| `bbscene.py <mob> [--bp …] [--q …]` | Prepara una variante para Blockbench (MCP blockbench): escribe `tools/out/bb/<mob>.scene.json` con base, capas, texturas, partes ocultas y animaciones, e imprime la línea `execute_script` que la carga con `tools/bb/load_scene.js`. En Blockbench quedan `mvPose(anim, t)` (animación + pose base a la vez) y `mvExportLayer(geo)`. Ver skill mv-blockbench. |
| `bbcheck.py <mob> [opciones de bbscene] [--anim A] [--views …] [--frames N]` / `bbcheck.py --measure [mob …] [--max-px 0.5] [--verbose]` | Con Blockbench abierto (puente 127.0.0.1:8787, no lo arranca): hoja de capturas de una variante animada en una sola imagen, y medición numérica de cuánto se separa cada capa del hueso vanilla de su nombre en todas las animaciones de adulto (`--measure`, todos los mobs ~4 min, solo imprime las que se separan). bbscene acepta `--all-layers` y `--roll xvar=N`. |
| `bbapply.py <geometry.mv.x> [--dry-run]` | Mete en el `.geo.json` del pack los huesos de una capa editada en Blockbench (`mvExportLayer`), con el formato del repo (ida y vuelta sin cambios = 0 líneas de diff). |
| `texuv.py template \| retarget \| recolor \| lint` | Texturas (Pillow): plantilla UV con caras y huesos; traslado de una skin al UV de otro modelo cara a cara (une extremidades partidas, informa de caras sin origen y de huesos que irían a una capa); variantes de color (HSV o colores de otra skin); píxeles fuera del UV y semitransparencias. Salida en `tools/out/tex/`. Ver skill mv-texture. |
| `hooks/pre-commit` | validate + bpcheck (+ ruff si cambian scripts) antes de cada commit. Se activa una vez con `git config core.hooksPath tools/hooks`. |
| `getvanilla.py [--force \| --version]` | Descarga la plantilla `vanilla/` (bedrock-samples) de la versión fijada en `VERSION`. |
| `mvlib.py`, `molang.py`, `mvsim.py` | Módulos: JSON con comentarios, índices de packs, geometrías (herencia 1.8, UV de caras), `save()` con formato compacto; intérprete de Molang (perezoso en `?:`, `&&`, `||`, como el juego); simulación de una entidad en un estado dado. |

## Límites conocidos

- **Molang**: no se ejecutan los bloques multilínea `{ … }` de las entidades 1.26 (solo contienen lógica
  vanilla). `math.random` devuelve el punto medio. Las queries valen 0 salvo que se fijen.
- **render.py**: los materiales se dibujan como alpha-test (sin transparencias parciales, brillo ni
  `uv_anim`); la pose es la del instante 0 con todo quieto. Los huesos `"reset": true` de geometrías
  1.8 antiguas (enderman) no tienen semántica documentada: su pose sale aproximada y el script lo avisa
  (prueba `--nopose`). Las partes que dibuja el motor fuera de los render controllers (objetos en la
  mano, armaduras, sillas de vanilla…) no salen.
- **simulate/render con BP** ignoran los `filters` de los eventos (bioma, bebé…): las probabilidades
  son las del `randomize` sin condiciones.

## Avisos del editor (extensión Blockception)

`.mcignore` excluye `vanilla/`, `dist/` y `tools/out/` (eran ~2600 avisos de los archivos de Mojang).
`.mcattributes` desactiva los códigos que son falsos positivos aquí, cada uno con su motivo:
la extensión no entiende los bloques Molang multilínea de las entidades 1.26 y pierde todas sus
variables; nuestros packs no contienen los objetos, bloques, sonidos ni loot tables del juego; y los
avisos del BP son idénticos en el archivo vanilla. Lo que esos códigos comprobarían lo hacen
`validate.py` (variables `v.mv_*`/`xvar` asignadas, claves `Texture./Geometry.`, animaciones) y
`bpcheck.py`. Tras cambiar estos archivos: *Developer: Reload Window*.

Ortografía (Code Spell Checker + diccionario español): `cspell.json` activa inglés y español, ignora
`vanilla/`, `dist/` y `tools/out/`, y lista el vocabulario del proyecto (nombres de mobs, de huesos,
identificadores). Si sale una palabra nueva correcta, añádela a `words`.

## Validador oficial de Mojang (opcional)

[Minecraft Creator Tools](https://github.com/Mojang/minecraft-creator-tools) (`mct`) valida
manifiestos, iconos, esquemas JSON y tamaños. No hace falta instalarlo:

```bash
npx -y @minecraft/creator-tools@0.20.0 validate all -i <copia con RP/ y BP/> --single -o <carpeta de salida> --json --warn-only
```

Ejecútalo sobre una **copia** de `RP/` y `BP/` (escribe informes y lee todo lo que hay en la carpeta).
Avisos que son ruido en este proyecto: `uv_anim ... required` (esquema de render controllers),
`JSONF` sobre archivos vanilla del BP, `STRICT` (redefinimos entidades `minecraft:` a propósito) y
`UNLINK` de texturas/sonidos en rutas vanilla. Lo útil: `CPACKICON`, `CHKMANIF` y errores de manifiesto.

## Notas

- `save()` escribe JSON con listas cortas en una línea y acepta un `header` de comentarios `//`.
- Los modelos/entidades antiguos de vanilla para comparar se pueden descargar de
  `https://raw.githubusercontent.com/Mojang/bedrock-samples/<tag>/resource_pack/...` (tags estables:
  `v1.19.30` … `v1.26.60.5`).
- Pylance/pyright usan `pyrightconfig.json` (raíz) y ruff `tools/ruff.toml`; ambos deben quedar a 0:
  `npx -y pyright@1.1.400 -p pyrightconfig.json` y `python -m ruff check tools`.
