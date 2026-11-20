// Cart, filters and search shared by the sample online stores (/muestras/). Everything stays in
// memory: nothing is stored or sent. The checkout shows the WhatsApp message the store would receive.
type Line = { key: string; id: string; name: string; variant: string; price: number; img: string; qty: number };
type Options = { greeting: string; freeShipping?: number; shipping?: number; gift?: number; lineLabel?: (l: Line) => string };
const cop = (n: number) => '$' + n.toLocaleString('es-CO');
const esc = (s: string) => s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

export function createStore(o: Options) {
  const lines: Line[] = [];
  const drawer = document.querySelector<HTMLDialogElement>('[data-cart-drawer]')!;
  const list = drawer.querySelector<HTMLElement>('[data-cart-lines]')!;
  const live = document.querySelector<HTMLElement>('[data-cart-live]');
  const gift = drawer.querySelector<HTMLInputElement>('[data-gift]');
  const product = (id: string) => document.querySelector<HTMLElement>(`[data-product="${id}"]`)!;
  const totals = () => {
    const subtotal = lines.reduce((s, l) => s + l.price * l.qty, 0);
    const ship = !subtotal || (o.freeShipping && subtotal >= o.freeShipping) ? 0 : (o.shipping ?? 0);
    const wrap = gift?.checked && subtotal ? (o.gift ?? 0) : 0;
    return { subtotal, ship, wrap, total: subtotal + ship + wrap, count: lines.reduce((s, l) => s + l.qty, 0) };
  };
  const render = () => {
    const t = totals();
    document.querySelectorAll('[data-cart-count]').forEach(el => { el.textContent = String(t.count); el.toggleAttribute('data-empty', !t.count); });
    list.innerHTML = lines.length ? lines.map(l => `
      <li class="cart-line">
        ${l.img ? `<img src="${esc(l.img)}" alt="" width="72" height="72">` : '<span class="cart-thumb" aria-hidden="true"></span>'}
        <div class="cart-line-info"><b>${esc(l.name)}</b>${l.variant ? `<small>${esc(l.variant)}</small>` : ''}<span>${cop(l.price)}</span></div>
        <div class="cart-qty" role="group" aria-label="Cantidad de ${esc(l.name)}">
          <button type="button" data-qty="-1" data-key="${esc(l.key)}" aria-label="Quitar uno">−</button><output>${l.qty}</output><button type="button" data-qty="1" data-key="${esc(l.key)}" aria-label="Agregar uno">+</button>
        </div>
      </li>`).join('') : '<li class="cart-empty">Tu carrito está vacío. Agrega algo lindo.</li>';
    const set = (sel: string, v: string) => drawer.querySelectorAll(sel).forEach(el => { el.textContent = v; });
    set('[data-cart-subtotal]', cop(t.subtotal));
    set('[data-cart-ship]', t.ship ? cop(t.ship) : 'Gratis');
    set('[data-cart-total]', cop(t.total));
    const bar = drawer.querySelector<HTMLElement>('[data-ship-bar]');
    if (bar && o.freeShipping) {
      bar.style.setProperty('--p', String(Math.min(1, t.subtotal / o.freeShipping)));
      set('[data-ship-note]', t.subtotal >= o.freeShipping ? '¡Tu envío es gratis! 🎉' : `Te faltan ${cop(o.freeShipping - t.subtotal)} para el envío gratis`);
    }
    drawer.querySelector<HTMLButtonElement>('[data-checkout]')!.disabled = !lines.length;
  };
  const add = (id: string, variant = '', price?: number) => {
    const el = product(id);
    const key = `${id}|${variant}`;
    const found = lines.find(l => l.key === key);
    if (found) found.qty++;
    else lines.push({ key, id, variant, name: el.dataset.name!, price: price ?? Number(el.dataset.price), img: el.querySelector('img')?.currentSrc || el.querySelector('img')?.src || '', qty: 1 });
    render();
    if (live) live.textContent = `${el.dataset.name} agregado al carrito`;
    document.querySelectorAll<HTMLElement>('[data-cart-open]').forEach(b => { b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); });
  };
  list.addEventListener('click', e => {
    const b = (e.target as Element).closest<HTMLButtonElement>('[data-qty]');
    if (!b) return;
    const l = lines.find(x => x.key === b.dataset.key)!;
    l.qty += Number(b.dataset.qty);
    if (l.qty <= 0) lines.splice(lines.indexOf(l), 1);
    render();
    drawer.querySelector<HTMLButtonElement>(`[data-key="${CSS.escape(b.dataset.key!)}"][data-qty="${b.dataset.qty}"]`)?.focus();
  });
  gift?.addEventListener('change', render);
  document.querySelectorAll('[data-cart-open]').forEach(b => b.addEventListener('click', () => drawer.showModal()));
  drawer.querySelectorAll('[data-cart-close]').forEach(b => b.addEventListener('click', () => drawer.close()));
  drawer.addEventListener('click', e => { if (e.target === drawer) drawer.close(); });
  document.addEventListener('click', e => {
    const b = (e.target as Element).closest<HTMLElement>('[data-add]');
    if (b) add(b.dataset.add!);
  });
  drawer.querySelector('[data-checkout]')!.addEventListener('click', () => {
    const t = totals();
    const label = o.lineLabel ?? ((l: Line) => `${l.qty} × ${l.name}${l.variant ? ` (${l.variant})` : ''} — ${cop(l.price * l.qty)}`);
    const text = [o.greeting, '', ...lines.map(label), '', `Subtotal: ${cop(t.subtotal)}`, ...(o.shipping !== undefined ? [`Envío: ${t.ship ? cop(t.ship) : 'gratis'}`] : []), ...(t.wrap ? [`Empaque de regalo: ${cop(t.wrap)}`] : []), `Total: ${cop(t.total)}`, '', 'Nombre:', 'Dirección de entrega:'].join('\n');
    drawer.close();
    (window as any).sdOrder(text);
  });
  render();
  return { add };
}

// Chips (data-filter-group + data-value), search box and sort select over [data-product] cards.
export function createFilters() {
  const cards = [...document.querySelectorAll<HTMLElement>('[data-product]')];
  const grid = cards[0]?.parentElement;
  const search = document.querySelector<HTMLInputElement>('[data-search]');
  const sort = document.querySelector<HTMLSelectElement>('[data-sort]');
  const empty = document.querySelector<HTMLElement>('[data-empty-state]');
  const count = document.querySelector<HTMLElement>('[data-result-count]');
  const active: Record<string, string> = {};
  const norm = (s: string) => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
  const apply = () => {
    const q = norm(search?.value.trim() ?? '');
    let shown = 0;
    cards.forEach(c => {
      const tags = (c.dataset.tags ?? '').split(' ');
      const ok = Object.values(active).every(v => v === 'all' || tags.includes(v)) && (!q || norm(c.dataset.name! + ' ' + (c.dataset.keywords ?? '')).includes(q));
      c.hidden = !ok; if (ok) shown++;
    });
    if (sort && grid) {
      const order = [...cards].sort((a, b) => sort.value === 'asc' ? +a.dataset.price! - +b.dataset.price! : sort.value === 'desc' ? +b.dataset.price! - +a.dataset.price! : +a.dataset.pos! - +b.dataset.pos!);
      order.forEach(c => grid.appendChild(c));
    }
    if (empty) empty.hidden = shown !== 0;
    if (count) count.textContent = `${shown} ${shown === 1 ? 'producto' : 'productos'}`;
  };
  document.querySelectorAll<HTMLButtonElement>('[data-filter-group]').forEach(b => {
    const g = b.dataset.filterGroup!;
    if (b.getAttribute('aria-pressed') === 'true') active[g] = b.dataset.value!;
    b.addEventListener('click', () => {
      document.querySelectorAll<HTMLButtonElement>(`[data-filter-group="${g}"]`).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      active[g] = b.dataset.value!; apply();
    });
  });
  search?.addEventListener('input', apply);
  sort?.addEventListener('change', apply);
  cards.forEach((c, i) => { c.dataset.pos = String(i); });
  apply();
}
