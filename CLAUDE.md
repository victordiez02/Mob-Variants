# CLAUDE.md — Mob Variants

Add-on de Minecraft Bedrock que da skins y cosméticos aleatorios a los mobs vanilla.
Objetivo actual: **1.26.60**, y en el futuro ser compatible con *Actions & Stuff* (A&S).

Lee también:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): cómo funciona el sistema de variantes (léelo antes de tocar un mob).
- [docs/STATUS.md](docs/STATUS.md): estado de cada mob, tareas pendientes y decisiones ya tomadas.
- [docs/TOOLS.md](docs/TOOLS.md): scripts de validación y simulación de `tools/`.

## Estructura

| Ruta | Qué es |
|---|---|
| `RP/` | Resource pack. **Debe funcionar solo** (las skins se sortean en el cliente). |
| `BP/` | Behavior pack opcional. Solo guarda la variante elegida en propiedades de entidad. Depende del RP. |
| `vanilla/` | Packs vanilla de referencia ([Mojang/bedrock-samples](https://github.com/Mojang/bedrock-samples), release estable). **Gitignored**; ver "Plantilla vanilla". |
| `tools/` | Scripts Python de validación y simulación (ver docs/TOOLS.md). |
| `docs/` | Documentación y `Probabilities.pdf` (fuera de los packs para que no se empaquete). |

El desarrollador trabaja en este repo; Minecraft lee `BP/` y `RP/` mediante **junctions** en
`%APPDATA%\Minecraft Bedrock\Users\Shared\games\com.mojang\development_{behavior,resource}_packs\`.
No hay que copiar nada: guardar y volver a entrar al mundo basta.

## Reglas del proyecto (decididas con el usuario; no las cambies sin preguntar)

1. **Modelo y animaciones vanilla.** No se sustituye el modelo base de ningún mob ni se añaden
   animaciones propias. Los modelos re-rigueados heredados de otros packs (codos/rodillas partidos,
   párpados) se están eliminando. Excepción temporal: el **wither** conserva su modelo y su animación
   `animation.mv.wither_boss.move`.
2. **Lo nuevo va en capas.** Sombreros, flores, colmillos, etc. son geometrías aparte cuyos huesos
   **se llaman como los huesos vanilla** (`head`, `body`, `leg0`, …) con su mismo pivote y jerarquía
   de padres, para que sigan cualquier animación (vanilla o A&S). Las piezas propias van como hijos
   con prefijo `mv_`. Para esconder una pieza vanilla, `part_visibility` en el render controller.
3. **Skins solo en la variante vanilla por defecto y en adultos** (vaca templada, gato blanco, zorro
   rojo, rana templada…). Bebés y otras variantes vanilla se ven 100 % vanilla. Se controla con
   `v.mv_active` (ver ARCHITECTURE).
4. **Namespace `mv`** para todo lo propio: `geometry.mv.*`, `controller.render.mv.*`,
   `animation.mv.*`, propiedades `mv:*`, grupos/eventos de BP `mv:*`, claves de entidad `mv_*`.
   Nunca redefinas un ID vanilla: afecta a otros mobs (pasó con el guardián anciano y el zoglin).
5. **El BP se construye sobre el archivo vanilla actual**, añadiendo solo propiedades y nodos
   `set_property` a los eventos vanilla. Nunca copies un archivo vanilla antiguo.
6. **Retexturas puras** (sin entidad) cuando la skin encaja en el UV vanilla y no hay aleatoriedad:
   texturas en la ruta vanilla (stray, caballos, panda, slime, wither).

## Flujo de trabajo

1. Antes de tocar un mob, mira su fila en docs/STATUS.md.
2. Después de cualquier cambio ejecuta (detalles en docs/TOOLS.md):
   ```bash
   python -I tools/check.py <mob>     # validate + bpcheck + simulate: debe acabar en "RESULT: OK"
   python tools/render.py <mob>       # mira tú mismo el PNG (tools/out/<mob>.png) antes de pedir pruebas
   ```
   Los huecos de bedrock-samples (8 animaciones vanilla que existen en el juego) salen como EXPECTED,
   no como errores. Los avisos de capas de validate son la deuda de la regla 2 (ver STATUS.md).
3. **Pruebas en el juego: las hace el usuario**, solo para lo que no cubren las herramientas
   (animaciones en movimiento, materiales, comportamiento del BP). Pide capturas; el Content Log lo
   lees tú: `python -I tools/contentlog.py --since HH:MM` (el juego añade al mismo archivo hasta que se
   reinicia). Recuerda al usuario probar con mobs **recién aparecidos** (los antiguos no tienen la
   propiedad del BP guardada).
4. Commits en español, estilo conventional (`fix:`, `refactor(<mob>):`, `chore:`), uno por mob cuando
   el cambio requiera cuidado. Termina con la línea `Co-Authored-By` que indique el sistema.

## Trampas conocidas (todas han roto el pack alguna vez)

- **`format_version` de las entidades de cliente = la de su archivo vanilla.** Las de 1.26.0 reparten
  Molang en varias líneas (`(cond) ? {` … `};`); con 1.10.0 la entidad no carga y el mob sale vanilla.
- **No uses `animation_controllers`** (lista antigua): el juego la rechaza en entidades de packs y se
  pierde la pose base (enderman con la cabeza separada). Mete los controladores en `animations` y
  lánzalos desde `scripts.animate`.
- **Materiales inexistentes invalidan la entidad entera** (`[Json][error] Material "x" ... not defined`).
  Usa materiales vanilla (`entity_alphatest`, `enderman`, `stray_clothes`, …). No hay materiales propios.
- **`minecraft:add_attributes` no es un evento del motor**: nada que pongas ahí se ejecuta.
  Los sorteos van en `minecraft:entity_spawned` (y `entity_transformed` si procede).
- Índices de arrays en render controllers: `max(0, x) % tamaño` (dan la vuelta, no se recortan).
- `q.property('x')` sobre una propiedad que no existe da error: protégelo con `q.has_property('x')`.
- Claves que usa el motor por nombre y no deben llevar prefijo: `beam`, `beam_material`,
  `death_material` (dragón, guardián). Copia las claves vanilla que ningún render controller usa.
- Huesos de capas: copia **pivote y padre** del hueso vanilla. Si la pose vanilla mueve `body` (enderman
  sube 11 px), una capa sin ese padre queda descolocada.
- Windows: carpetas con `[ ]` rompen `glob` y `New-Item -Target` (comodines); VS Code bloquea archivos
  un instante al escribir (los `save()` de tools reintentan).

## Plantilla vanilla

`vanilla/` no está en git. Para regenerarla: `python -I tools/getvanilla.py` (descarga
`bedrock-samples-<versión>-full.zip` de [Mojang/bedrock-samples](https://github.com/Mojang/bedrock-samples/releases)).
La versión está en la constante `VERSION` de ese script (v1.26.60.5); para pasar a otra versión de
Minecraft, cámbiala y ejecuta `--force`. La CI usa el mismo script y cachea por versión.

## CI

`.github/workflows/checks.yml` se ejecuta en cada push a `main` y en cada PR: ruff + pyright sobre
`tools/`, y `validate`, `bpcheck`, `simulate` y `render` (de todos los mobs) sobre los packs. Los
renders quedan como artefacto `renders` del run (14 días): sirven para revisar visualmente un cambio.
