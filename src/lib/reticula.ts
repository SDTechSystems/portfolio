// Ancho del mosaico "¿No ves tu juego?" para cerrar la retícula sin huecos.
// Simula cómo coloca el navegador los mosaicos (grid-auto-flow: dense: cada uno va en el primer
// hueco donde quepa) y prueba los anchos posibles para el cierre: gana el que deja menos celdas vacías.
// Hace falta porque los juegos con varias versiones miden dos mosaicos y pueden dejar un hueco.

/** Una pieza del tablero (ancho en columnas, alto en filas) o el lugar del cierre de una sección. */
export type Pieza = { ancho: number; alto?: number } | 'cierre';

type Celdas = boolean[][];

function cabe(c: Celdas, fila: number, col: number, ancho: number, alto: number) {
  for (let y = fila; y < fila + alto; y++) for (let x = col; x < col + ancho; x++) if (c[y]?.[x]) return false;
  return true;
}

function poner(c: Celdas, columnas: number, ancho: number, alto: number) {
  for (let fila = 0; ; fila++)
    for (let col = 0; col + ancho <= columnas; col++)
      if (cabe(c, fila, col, ancho, alto)) {
        for (let y = fila; y < fila + alto; y++) {
          c[y] ??= Array(columnas).fill(false);
          for (let x = col; x < col + ancho; x++) c[y][x] = true;
        }
        return;
      }
}

const vacias = (c: Celdas) => c.reduce((n, fila) => n + fila.filter((x) => !x).length, 0);

/** Devuelve el ancho de cada cierre, en el orden en que aparecen. `minimo`: ancho de un mosaico. */
export function cierres(piezas: Pieza[], columnas: number, minimo: number): number[] {
  const c: Celdas = [];
  const anchos: number[] = [];
  for (const p of piezas) {
    if (p !== 'cierre') { poner(c, columnas, p.ancho, p.alto ?? 1); continue; }
    let mejor = columnas, menos = Infinity;
    // Candidatos: cerrar la última fila primero (empate = se queda ahí), luego tapar un hueco anterior.
    const ultima = c.at(-1)?.filter((x) => !x).length ?? 0;
    const candidatos = [ultima, ...c.map((fila) => fila.filter((x) => !x).length), columnas];
    for (const ancho of candidatos) {
      if (ancho < minimo || ancho > columnas) continue;
      const prueba = c.map((fila) => [...fila]);
      poner(prueba, columnas, ancho, 1);
      if (vacias(prueba) < menos) { menos = vacias(prueba); mejor = ancho; }
    }
    poner(c, columnas, mejor, 1);
    anchos.push(mejor);
  }
  return anchos;
}

/** Columnas que ocupa cada pieza del tablero (celular: 6 columnas; escritorio: 10).
 *  La usan index.astro al compilar y el buscador al recalcular el cierre. */
export const anchoPieza = (tipo: 'fila' | 'grande' | 'medio' | 'normal', movil: boolean) =>
  tipo === 'fila' || tipo === 'grande' ? (movil ? 6 : 10) : tipo === 'medio' ? (movil ? 3 : 5) : (movil ? 3 : 2);
