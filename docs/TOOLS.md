# Herramientas (`tools/`)

Scripts Python 3 sin dependencias salvo **Pillow** (`pip install pillow`) para los que tocan imágenes.
Leen el repo y la plantilla `vanilla/`; ejecútalos desde cualquier carpeta. `-I` aísla Python de
módulos externos (no lo uses con los que necesitan Pillow si está instalado en el usuario).

| Script | Uso | Para qué |
|---|---|---|
| `validate.py` | `python -I tools/validate.py` | Referencias del RP: texturas, geometrías, animaciones y render controllers que no existen; claves `Texture./Geometry./Material.` usadas sin definir; archivos sin usar. |
| `bpcheck.py` | `python -I tools/bpcheck.py` | BP: grupos y eventos referenciados que no existen, propiedades `mv:*` sin declarar o fuera de rango. |
| `simulate.py` | `python -I tools/simulate.py [mob ...]` | Evalúa los render controllers con un intérprete de Molang (`molang.py`) para los 100 valores del sorteo y para cada valor del BP; lista cuántas skins/modelos distintos salen por capa. Si un mob da 1, sus variantes no funcionan. |
| `fit.py` | `python tools/fit.py` | Para cada entidad con modelo propio, qué porcentaje de las caras de su UV cae dentro del UV de cada modelo vanilla (¿encajan las skins en el modelo vanilla?). |
| `facecheck.py` | `python -I tools/facecheck.py <geo addon> <geo vanilla> [hueso=huesoVanilla ...]` | Lo mismo, cara a cara, indicando qué caras quedan fuera. |
| `limbmerge.py` | `python tools/limbmerge.py <geo addon> <geo vanilla> <textura sin extensión> ...` | Recoloca en el layout vanilla los píxeles de extremidades partidas (pierna + rodilla con UV de caja). Modifica las texturas: haz commit antes. |
| `overlay.py` | (módulo) `build(src_bones, plan, ident, desc)` | Genera una geometría de capa a partir de huesos de un modelo antiguo, colgándolos de huesos con nombre vanilla. Ver ejemplos en el historial (`refactor(witch)`, `refactor(spider)`, `refactor(pig)`). |
| `mvlib.py`, `geo.py` | (módulos) | Carga de JSON con comentarios, índices de geometrías, resolución de herencia 1.8, `save()` con formato compacto y reintentos ante bloqueos de archivo. |

Notas:
- `save()` escribe JSON con listas cortas en una línea y acepta un `header` de comentarios `//`.
- Los modelos/entidades antiguos de vanilla para comparar se pueden descargar de
  `https://raw.githubusercontent.com/Mojang/bedrock-samples/<tag>/resource_pack/...` (tags estables:
  `v1.19.30` … `v1.26.60.5`). Se usó para distinguir qué cambió el addon respecto a vanilla.
