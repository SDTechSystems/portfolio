---
name: cerrar-sesion
description: Actualiza la sección Estado y el Registro de decisiones de docs/spec.md con lo hecho en la sesión, como pide AGENTS.md. Úsalo al terminar un trabajo y antes del commit final.
disable-model-invocation: true
---

# Cerrar la sesión: actualizar `docs/spec.md`

`AGENTS.md` exige actualizar **§5 Estado** y **§8 Registro de decisiones** al terminar.

## 1. Qué cambió

- `git status`, `git diff` y `git log --oneline origin/main..HEAD` para ver los cambios de la rama.
- Repasa en la conversación qué se **verificó de verdad** (comandos corridos, anchos probados, resultados). No anotes como hecho lo que no se probó.

## 2. §5 Estado

- Cambia **Última actualización** a la fecha de hoy (AAAA-MM-DD), un resumen de 2–4 palabras y la rama actual.
- Agrega una línea por logro, con el formato de las existentes:
  - `- [x]` hecho y verificado, con la evidencia en datos (ej. "24/24 portadas", "164 KB", "320, 390 y 1440 px").
  - `- [~]` hecho pero sin confirmar, diciendo qué falta y por qué.
- Si una línea antigua quedó obsoleta, corrígela en vez de duplicarla.
- Si cambian las cifras del catálogo (cantidad de juegos, Switch 1 / Switch 2), actualízalas.

## 3. §6 Tareas y §7 Decisiones abiertas

- Marca `[x]` / `[~]` las tareas T* que avanzaron.
- Si el dueño resolvió una decisión D*, márcala **Resuelta** con la respuesta.

## 4. §8 Registro de decisiones

- Una fila por decisión **no obvia** de la sesión: `| AAAA-MM-DD | Decisión | Motivo |`.
- El motivo explica el porqué (lo que se descartó y por qué), no repite el qué.
- Si una decisión reemplaza a otra, tacha la vieja con `~~…~~ → nueva`, como en la fila de la pestaña de consola.

## 5. Estilo

Español, tuteo, frases cortas, sin emojis. No reescribas secciones que no cambiaron. Muestra al usuario el diff de `docs/spec.md` antes del commit.
