---
name: mv-release
description: Commits, versiones y publicación de Mob Variants - commits atómicos, subir versión de los manifests, empaquetar .mcpack/.mcaddon, tag y release de GitHub, y actualizar a una versión nueva de Minecraft (plantilla vanilla). Úsala al hacer commit/push, al preparar una versión o cuando salga un Minecraft nuevo.
allowed-tools: Bash(python -I tools/package.py:*), Bash(python -I tools/getvanilla.py:*), Bash(python -I tools/check.py:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*)
---

# Commits

- Atómicos: un cambio lógico por commit (un mob, una herramienta, docs). Mensaje en español,
  conventional (`fix(<mob>):`, `feat(tools):`, `refactor(<mob>):`, `docs:`, `ci:`, `chore:`).
- **Sin** línea `Co-Authored-By`.
- El hook `tools/hooks/pre-commit` pasa validate + bpcheck (+ ruff si tocas tools). Si no está
  activo: `git config core.hooksPath tools/hooks`. No uses `--no-verify` salvo que el usuario lo pida.
- Push a `main` cuando el usuario lo pida o lo haya pedido en la sesión; luego comprueba la CI (mv-verify).

# Versión del pack

1. Sube `header.version`, `modules[].version` y la dependencia del BP al RP en `RP/manifest.json`
   y `BP/manifest.json` (los cuatro iguales). El nombre del pack lleva la versión (`v5.0`).
2. `python -I tools/package.py`: valida los manifests y genera `dist/*.mcpack` y `dist/*.mcaddon`.
3. Commit `chore: versión X.Y.Z`, push y tag `vX.Y.Z` (`git tag vX.Y.Z && git push origin vX.Y.Z`,
   pide confirmación: es público). `.github/workflows/release.yml` comprueba que el tag coincide con el
   manifest y publica la release con los paquetes.

# Minecraft nuevo

1. Cambia `VERSION` en `tools/getvanilla.py` al tag estable nuevo de Mojang/bedrock-samples y
   `python -I tools/getvanilla.py --force`.
2. `python -I tools/check.py`: `format_version` menor que la vanilla = error; bpcheck lista
   componentes/grupos/eventos que ya no coinciden con la vanilla nueva (regla 5: reconstruye el
   archivo desde el vanilla nuevo añadiendo solo propiedades y `set_property` `mv:`).
3. `min_engine_version` de los manifests y de las entidades (validate lo lista en INFO).
4. Actualiza CLAUDE.md (versión objetivo) y STATUS.md.
