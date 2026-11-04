---
name: nuevo-producto
description: Agrega un juego, DLC o update al catálogo (productos.json) con su portada, y comprueba que el build pasa. Úsalo cuando el usuario pida agregar, cambiar o quitar un título o su precio.
argument-hint: "<título> <consola> <precio COP> [ruta de la portada]"
disable-model-invocation: true
---

# Agregar un producto al catálogo

Petición: $ARGUMENTS

Archivo: `src/assets/Catalogo_Nintendo_Switch_Colombia/productos.json` (lista `productos`).
Portadas: `src/assets/Catalogo_Nintendo_Switch_Colombia/imagenes/`.
Las reglas que se validan están en `src/lib/catalogo.ts`; si este archivo y el código no coinciden, manda el código.

## 1. Reúne los datos (pregunta solo lo que falte)

| Campo | Regla |
|---|---|
| `id` | minúsculas y guiones, único (ej. `mario-kart-world`). Si el juego tiene versión para las dos consolas, son **dos entradas** con ids distintos (ej. sufijo `-switch-2`; paquete de mejora: `-mejora`) y el mismo `grupo`. |
| `grupo` | solo si hay varias versiones del juego: mismo texto (minúsculas y guiones) en todas, ej. `"zelda-totk"`. Se dibujan en un solo mosaico; la portada sale de la versión de Switch 2 (si su logo está arriba, `imagen.recorte: "arriba"`). |
| `titulo` | nombre oficial. |
| `plataforma` | exactamente `"Nintendo Switch"` o `"Nintendo Switch 2"`. |
| `tipo_producto` | `"juego_digital"`, `"juego_con_accesorios"` (muestra "Necesita Ring-Con"), `"dlc"`, `"update"` o `"paquete_mejora"` (con `"plataforma": "Nintendo Switch 2"` y `grupo`). |
| `precio_referencia_eshop_colombia_cop` | entero en pesos **sin puntos** (`239900`, no `239.900`), o `null` → se muestra "Consultar". |
| `precio_venta_cop` | opcional; si existe, es el precio que se muestra (decisión D5 del spec). |
| `edicion`, `estado_precio`, `puesto_ranking` | copia el formato de las entradas vecinas (`"base"`, `"referencia"`, siguiente número). |
| `imagen` | `{ "ruta": "imagenes/<id>.webp", "alt": "Arte oficial de <título>", "ancho", "alto" }`. Opcional: sin portada queda el fondo gris (F5). |

No inventes precios: si el usuario no da uno, pregunta o usa `null`.

## 2. Portada

- Nómbrala `<id>.webp` (también valen `.jpg`, `.jpeg`, `.png`) y déjala en `imagenes/`.
- Proporción 16:9 (como las demás, 1920×1080; mínimo 960×540, pero en computador se verá borrosa). Comprueba el tamaño real del archivo y pon `ancho`/`alto` correctos.
- Astro la optimiza al compilar: no la reduzcas a mano.

## 3. Orden y visibilidad

- La entrada se dibuja en el orden del archivo: colócala donde el usuario quiera (por defecto, al final de los juegos).
- Para que sea destacado, su id va en `src/data/tienda.ts → destacados` (siempre exactamente 3).
- DLC y updates solo se ven si `tienda.ts → mostrarDlcUpdates` es `true` (tarea T4b del spec).
- No toques el diseño (`docs/diseno.md` §7: agregar un juego es solo datos + portada).

## 4. Verifica

1. `npm run build`: debe terminar sin "Revisa el catálogo:". El hook `revisar-catalogo.sh` ya lo corre al editar `productos.json` o `tienda.ts`; si te devuelve errores, corrígelos.
2. Si cambió el número de mosaicos, revisa a 390 px y 1440 px que la última fila no deje huecos (`docs/diseno.md` §8).
3. Resume al usuario: título, consola, precio mostrado (formato `$ 239.900`) y si tiene portada.
4. Actualiza `docs/spec.md` → **Estado** (cantidad de títulos) antes del commit, o recuérdale al usuario correr `/cerrar-sesion`.
