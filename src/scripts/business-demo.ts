import {
  sampleProducts,
  sampleCustomers,
  sampleAccounts,
  type DemoProduct,
  type DemoAccount,
} from "../data/business-demo";
import {
  $,
  $$,
  es,
  l,
  node,
  button,
  money,
  notice,
  initDialogs,
  initScreens,
} from "./demo-core";
const erp = document.body.dataset.demo === "openmultipos";
const products = sampleProducts(es ? "es" : "en").filter(
  (p) => erp || p.brand === "a",
);
const customers = sampleCustomers(es ? "es" : "en");
const accounts: DemoAccount[] = erp ? [] : sampleAccounts(es ? "es" : "en");
let paymentAccount: DemoAccount | undefined;
const owedBy = (a: DemoAccount) =>
  a.purchases.reduce((sum, p) => sum + p.amount - p.paid, 0);
let brand = "a";
const cart = new Map<string, number>();
type Sale = {
  id: string;
  brand: string;
  total: number;
  items: string[];
  method: string;
  customer: string;
  amountByBrand?: Record<string, number>;
};
const sales: Sale[] = [
  {
    id: "DEMO-001",
    brand: "a",
    total: 25500,
    items: [l("3 × Café frío", "3 × Cold brew")],
    method: "cash",
    customer: customers[0].name,
  },
  {
    id: "DEMO-002",
    brand: "a",
    total: 17000,
    items: [l("2 × Café frío", "2 × Cold brew")],
    method: "card",
    customer: customers[1].name,
  },
  {
    id: "DEMO-003",
    brand: "b",
    total: 65000,
    items: [l("1 × Lámpara de escritorio", "1 × Desk lamp")],
    method: "cash",
    customer: customers[2].name,
  },
];
const localSales = () =>
  sales
    .filter((s) => s.brand === brand || s.brand === "mixed")
    .map((s) =>
      s.brand === "mixed" ? { ...s, total: s.amountByBrand![brand] } : s,
    );
function subtotal() {
  return [...cart].reduce(
    (sum, [id, q]) => sum + products.find((p) => p.id === id)!.price * q,
    0,
  );
}
function discount() {
  return Math.round(
    Math.max(
      0,
      Math.min(50, Number($<HTMLInputElement>("#sale-discount").value) || 0),
    ),
  );
}
function total() {
  return Math.round((subtotal() * (100 - discount())) / 100);
}
function eligible(p: DemoProduct) {
  return p.brand === brand;
}
function add(p: DemoProduct) {
  const qty = cart.get(p.id) || 0;
  if (qty >= p.stock)
    return notice(
      l(
        "Ya agregaste las existencias disponibles en el ejemplo.",
        "You have added all available sample stock.",
      ),
    );
  cart.set(p.id, qty + 1);
  renderCart();
  notice(l("Añadido a la cesta: ", "Added to basket: ") + p.name);
}
function renderCatalog() {
  const search =
    $<HTMLInputElement>("#product-search").value.toLocaleLowerCase();
  const category = $<HTMLSelectElement>("#product-category").value;
  const selected = products.filter(
    (p) =>
      eligible(p) &&
      (category === "all" || p.category === category) &&
      `${p.name} ${p.sku}`.toLocaleLowerCase().includes(search),
  );
  const grid = $("#product-grid");
  grid.replaceChildren();
  selected.forEach((p) => {
    const b = button("", () => add(p), "product-tile");
    b.setAttribute("aria-label", l("Añadir ", "Add ") + p.name);
    const art = node("span", p.icon, "product-art");
    const info = node("span", "", "product-info");
    info.append(node("strong", p.name), node("small", p.sku, "muted"));
    const bottom = node("span", "", "product-bottom");
    bottom.append(node("b", money(p.price)), node("span", "+", "product-plus"));
    b.append(art, info, bottom);
    if (p.stock === 0) b.disabled = true;
    grid.append(b);
  });
  $("#product-empty").hidden = selected.length > 0;
}
function renderCart() {
  const lines = $("#cart-lines");
  lines.replaceChildren();
  if (!cart.size) {
    const empty = node("div", "", "cart-empty");
    empty.append(
      node("span", "＋"),
      node(
        "p",
        l("Tu próxima venta empieza aquí", "Your next sale starts here"),
      ),
      node(
        "small",
        l(
          "Selecciona un producto del catálogo.",
          "Choose a product from the catalog.",
        ),
      ),
    );
    lines.append(empty);
  }
  cart.forEach((qty, id) => {
    const p = products.find((p) => p.id === id)!;
    const line = node("div", "", "cart-line");
    line.dataset.product = id;
    const info = node("div");
    info.append(
      node("strong", p.name),
      node(
        "small",
        money(p.price) +
          (erp ? " · " + (p.brand === "a" ? "Aurora" : "Nexo") : ""),
      ),
    );
    const controls = node("div", "", "quantity-controls");
    const minus = button(
      "−",
      () => {
        qty > 1 ? cart.set(id, qty - 1) : cart.delete(id);
        renderCart();
        (
          $<HTMLElement>(`[data-product="${id}"] button`) ||
          $<HTMLElement>(".cart-line button") ||
          $("#clear-cart")
        ).focus();
      },
      "quantity-button",
    );
    minus.setAttribute(
      "aria-label",
      l("Quitar una unidad de ", "Remove one ") + p.name,
    );
    const plus = button(
      "+",
      () => {
        add(p);
        $<HTMLElement>(`[data-product="${id}"] button:last-child`).focus();
      },
      "quantity-button",
    );
    plus.setAttribute(
      "aria-label",
      l("Añadir una unidad de ", "Add one ") + p.name,
    );
    controls.append(minus, node("span", String(qty)), plus);
    line.append(info, controls);
    lines.append(line);
  });
  $("#cart-count").textContent = String(
    [...cart.values()].reduce((a, b) => a + b, 0),
  );
  $("#cart-subtotal").textContent = money(subtotal());
  $("#cart-discount").textContent = "− " + money(subtotal() - total());
  $("#cart-total").textContent = money(total());
  $<HTMLButtonElement>("#start-checkout").disabled = !cart.size;
}
function saleList(target: string) {
  const container = $(target);
  container.replaceChildren();
  localSales()
    .slice()
    .reverse()
    .slice(0, 8)
    .forEach((s) => {
      const row = node("div", "", "sale-row");
      const info = node("div");
      info.append(node("strong", s.id), node("small", s.customer));
      const end = node("div");
      end.append(
        node("strong", money(s.total)),
        node(
          "small",
          l("Completada · Ejemplo", "Completed · Sample"),
          "positive",
        ),
      );
      row.append(info, end);
      container.append(row);
    });
}
function renderInventory() {
  const search =
    $<HTMLInputElement>("#inventory-search").value.toLocaleLowerCase();
  const rows = $("#inventory-rows");
  rows.replaceChildren();
  const matching = products.filter(
    (p) =>
      eligible(p) && `${p.name} ${p.sku}`.toLocaleLowerCase().includes(search),
  );
  matching.forEach((p) => {
    const tr = node("tr");
    const name = node("td");
    name.append(
      node("span", p.icon, "table-product-icon"),
      node("strong", p.name),
    );
    const qty = node("td");
    qty.append(
      node("span", String(p.stock), p.stock <= 5 ? "pill warning" : "pill"),
    );
    const action = node("td");
    action.append(
      button(
        l("Ver ficha", "View details"),
        () => showProduct(p),
        "text-button",
      ),
    );
    tr.append(name, node("td", p.sku), node("td", money(p.price)), qty);
    if (!erp) tr.append(node("td", String(p.stored)));
    tr.append(action);
    rows.append(tr);
  });
  $("#inventory-empty").hidden = matching.length > 0;
}
function showProduct(p: DemoProduct) {
  $("#product-title").textContent = p.name;
  const box = $("#product-details");
  box.replaceChildren();
  const art = node("div", p.icon, "detail-product-art");
  box.append(
    art,
    node("p", "SKU · " + p.sku),
    node("p", l("Precio de ejemplo · ", "Sample price · ") + money(p.price)),
    node("p", l("Existencias de ejemplo · ", "Sample stock · ") + p.stock),
    ...(erp
      ? []
      : [
          node(
            "p",
            l("En el local · ", "In the shop · ") +
              (p.stock - p.stored) +
              l(" · En bodega · ", " · In storeroom · ") +
              p.stored,
            "stock-split",
          ),
          (() => {
            const row = node("div", "", "move-buttons");
            const move = (toStore: boolean) => {
              if (toStore ? p.stock - p.stored <= 0 : p.stored <= 0)
                return notice(
                  l("No hay unidades para mover.", "No units to move."),
                );
              p.stored += toStore ? 1 : -1;
              renderInventory();
              $(".stock-split").textContent =
                l("En el local · ", "In the shop · ") +
                (p.stock - p.stored) +
                l(" · En bodega · ", " · In storeroom · ") +
                p.stored;
              notice(
                toStore
                  ? l("1 unidad pasó a la bodega.", "1 unit moved to the storeroom.")
                  : l("1 unidad pasó al local.", "1 unit moved to the shop."),
              );
            };
            row.append(
              button(l("← 1 al local", "← 1 to shop"), () => move(false)),
              button(l("1 a bodega →", "1 to storeroom →"), () => move(true)),
            );
            return row;
          })(),
        ]),
    node(
      "p",
      l(
        "Producto ficticio para explorar el catálogo.",
        "Fictional product for exploring the catalog.",
      ),
      "muted",
    ),
  );
  $("#product-to-cart").onclick = () => {
    add(p);
    $<HTMLDialogElement>("#product-dialog").close();
    show("sales");
  };
  $<HTMLDialogElement>("#product-dialog").showModal();
}
function renderReports() {
  const weekly = $<HTMLSelectElement>("#report-period").value === "week";
  const list = localSales();
  const count = list.length + (weekly ? 24 : 0);
  const today = list.reduce((s, x) => s + x.total, 0);
  const history =
    brand === "a"
      ? [126000, 204000, 153000, 267000, 186000, 300000]
      : [180000, 215000, 182000, 280000, 198000, 340000];
  const revenue = today + (weekly ? history.reduce((a, b) => a + b, 0) : 0);
  $("#report-revenue").textContent = money(revenue);
  $("#report-count").textContent = String(count);
  $("#report-average").textContent = money(
    Math.round(revenue / Math.max(count, 1)),
  );
  saleList("#report-sales");
  const values = [...history, today];
  const days = es
    ? ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    : ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const max = Math.max(...values, 1);
  $$<HTMLElement>("#sales-chart>div").forEach((bar, i) => {
    const visual = $<HTMLElement>("span", bar);
    visual.style.setProperty(
      "--bar-height",
      Math.max(5, Math.round((values[i] / max) * 100)) + "%",
    );
    $("b", bar).textContent = new Intl.NumberFormat(es ? "es-CO" : "en-US", {
      notation: "compact",
      maximumFractionDigits: 1,
    }).format(values[i]);
  });
  $("#sales-chart").setAttribute(
    "aria-label",
    l("Ingresos ficticios: ", "Fictional revenue: ") +
      values.map((v, i) => days[i] + " " + money(v)).join("; "),
  );
}
function renderDebts() {
  if (erp) return;
  const owing = accounts.filter((a) => owedBy(a) > 0);
  const totalOwed = accounts.reduce((s, a) => s + owedBy(a), 0);
  const pending = accounts.reduce(
    (s, a) => s + a.purchases.filter((p) => p.amount > p.paid).length,
    0,
  );
  const countText =
    owing.length === 1
      ? l("1 cliente con saldo pendiente", "1 customer with a balance")
      : owing.length +
        l(" clientes con saldo pendiente", " customers with a balance");
  $("[data-metric=owed]").textContent = money(totalOwed);
  $("[data-metric=owed-count]").textContent = countText;
  $("#debts-total").textContent = money(totalOwed);
  $("#debts-count").textContent = countText;
  $("#debts-purchases").textContent = String(pending);
  $("#debts-credit").textContent = money(
    accounts.reduce((s, a) => s + a.credit, 0),
  );
  const box = $("#debt-accounts");
  box.replaceChildren();
  accounts.forEach((a) => {
    const card = node("article", "", "surface debt-card");
    const head = node("div", "", "debt-head");
    const who = node("div");
    who.append(node("h2", a.name));
    const owed = owedBy(a);
    who.append(
      node(
        "small",
        owed
          ? l("Debe ", "Owes ") + money(owed)
          : l("Al día", "Up to date"),
        owed ? "warning-text" : "positive",
      ),
    );
    head.append(who);
    if (a.credit)
      head.append(
        node("span", l("Saldo a favor ", "Store credit ") + money(a.credit), "pill"),
      );
    card.append(head);
    const list = node("ul", "", "debt-list");
    const open = a.purchases.filter((p) => p.amount > p.paid);
    if (!open.length)
      list.append(node("li", l("Sin compras pendientes.", "No unpaid purchases."), "muted"));
    open.forEach((p) => {
      const li = node("li");
      const info = node("span");
      info.append(
        node("strong", p.date + " · " + p.items),
        node(
          "small",
          p.id + (p.paid ? l(" · Abonado ", " · Paid ") + money(p.paid) : ""),
          "muted",
        ),
      );
      li.append(info, node("span", money(p.amount - p.paid)));
      list.append(li);
    });
    card.append(list);
    if (a.payments.length)
      card.append(
        node(
          "p",
          l("Últimos abonos: ", "Recent payments: ") +
            a.payments
              .slice(-3)
              .map((p) => p.date + " " + money(p.amount))
              .join(" · "),
          "muted debt-history",
        ),
      );
    const actions = node("div", "", "debt-actions");
    const pay = button(l("Registrar abono", "Record payment"), () => {
      paymentAccount = a;
      $("#payment-context").textContent =
        a.name + " · " + l("Debe ", "Owes ") + money(owedBy(a));
      const input = $<HTMLInputElement>("#payment-amount");
      input.value = String(Math.min(Math.max(owedBy(a), 500), 500000));
      $<HTMLDialogElement>("#payment-dialog").showModal();
    }, "primary");
    pay.setAttribute("aria-label", l("Registrar abono de ", "Record payment for ") + a.name);
    const statement = button(l("Estado de cuenta", "Statement"), () => showStatement(a));
    statement.setAttribute("aria-label", l("Estado de cuenta de ", "Statement for ") + a.name);
    actions.append(pay, statement);
    card.append(actions);
    box.append(card);
  });
}
function showStatement(a: DemoAccount) {
  $("#statement-customer").textContent = a.name;
  const lines = $("#statement-lines");
  lines.replaceChildren();
  a.purchases
    .filter((p) => p.amount > p.paid)
    .forEach((p) => {
      const row = node("p", "", "receipt-line");
      row.append(node("span", p.date + " · " + p.items), node("span", money(p.amount - p.paid)));
      lines.append(row);
    });
  if (a.credit) {
    const row = node("p", "", "receipt-line");
    row.append(node("span", l("Saldo a favor", "Store credit")), node("span", "− " + money(a.credit)));
    lines.append(row);
  }
  if (!lines.childElementCount)
    lines.append(node("p", l("Sin saldo pendiente.", "No balance due.")));
  $("#statement-total").textContent = money(owedBy(a));
  $<HTMLDialogElement>("#statement-dialog").showModal();
}
function render() {
  renderCatalog();
  renderCart();
  renderInventory();
  renderReports();
  const list = localSales();
  $("[data-metric=revenue]").textContent = money(
    list.reduce((s, x) => s + x.total, 0),
  );
  $("[data-metric=transactions]").textContent =
    list.length + l(" ventas de ejemplo", " sample sales");
  $("[data-metric=products]").textContent = String(
    products.filter(eligible).length,
  );
  $("[data-metric=low]").textContent = String(
    products.filter((p) => eligible(p) && p.stock <= 5).length,
  );
  saleList("#recent-sales");
  renderDebts();
}
initDialogs();
const show = initScreens();
$("#product-search").addEventListener("input", renderCatalog);
$("#product-category").addEventListener("change", renderCatalog);
$("#inventory-search").addEventListener("input", renderInventory);
$("#report-period").addEventListener("change", renderReports);
$("#sale-discount").addEventListener("input", renderCart);
$("#sale-discount").addEventListener("change", () => {
  $<HTMLInputElement>("#sale-discount").value = String(discount());
  renderCart();
});
$("#clear-cart").addEventListener("click", () => {
  cart.clear();
  $<HTMLInputElement>("#sale-discount").value = "0";
  renderCart();
  notice(l("Cesta vacía.", "Basket cleared."));
});
$("#business-picker")?.addEventListener("change", (e) => {
  brand = (e.target as HTMLSelectElement).value;
  $<HTMLSelectElement>("#product-category").value = "all";
  render();
  notice(
    l(
      "Negocio de ejemplo actualizado. La cesta conserva sus productos.",
      "Sample business updated. The basket keeps its items.",
    ),
  );
});
$$("[data-customer]").forEach((b) =>
  b.addEventListener("click", () => {
    $<HTMLSelectElement>("#sale-customer").value = b.dataset.customer!;
    show("sales");
    notice(l("Cliente de ejemplo seleccionado.", "Sample customer selected."));
  }),
);
$("#start-checkout").addEventListener("click", () => {
  if (!cart.size) return;
  $("#checkout-amount").textContent = money(total());
  $<HTMLDialogElement>("#checkout-dialog").showModal();
});
$<HTMLButtonElement>("#checkout-form button[type=submit]").disabled = false;
$("#checkout-form").addEventListener("submit", (e) => {
  e.preventDefault();
  if (!cart.size) return;
  const field = $<HTMLInputElement>("#sale-discount");
  if (!field.checkValidity()) {
    show("sales");
    $<HTMLDialogElement>("#checkout-dialog").close();
    field.reportValidity();
    return;
  }
  const method = $<HTMLInputElement>("[name=payment]:checked").value;
  const customerId = $<HTMLSelectElement>("#sale-customer").value;
  if (method === "credit" && customerId === "walk-in") {
    $("#credit-note").textContent = l(
      "Para vender a crédito, elige un cliente en la cesta.",
      "To sell on credit, choose a customer in the basket.",
    );
    return;
  }
  if (!erp) $("#credit-note").textContent = "";
  const amount = total();
  const itemLines: string[] = [];
  const receipt = $("#receipt-lines");
  receipt.replaceChildren();
  const brands = new Set<string>();
  const amountByBrand: Record<string, number> = {};
  cart.forEach((q, id) => {
    const p = products.find((p) => p.id === id)!;
    p.stock -= q;
    brands.add(p.brand);
    amountByBrand[p.brand] = (amountByBrand[p.brand] || 0) + p.price * q;
    itemLines.push(`${q} × ${p.name}`);
    const row = node("p", "", "receipt-line");
    row.append(
      node(
        "span",
        `${q} × ${p.name}` +
          (erp ? " · " + (p.brand === "a" ? "Aurora" : "Nexo") : ""),
      ),
      node("span", money(p.price * q)),
    );
    receipt.append(row);
  });
  let remaining = amount;
  [...brands].forEach((key, i) => {
    const allocated =
      i === brands.size - 1
        ? remaining
        : Math.round((amountByBrand[key] * (100 - discount())) / 100);
    amountByBrand[key] = allocated;
    remaining -= allocated;
    if (erp) {
      const row = node("p", "", "receipt-line");
      row.append(
        node("strong", key === "a" ? "Aurora" : "Nexo"),
        node("strong", money(allocated)),
      );
      receipt.append(row);
    }
  });
  if (discount())
    receipt.append(
      node("p", l("Descuento: ", "Discount: ") + discount() + "%"),
    );
  const customer =
    customers.find((c) => c.id === $<HTMLSelectElement>("#sale-customer").value)
      ?.name || l("Venta de mostrador", "Walk-in customer");
  sales.push({
    id: `DEMO-${String(sales.length + 1).padStart(3, "0")}`,
    brand: brands.size > 1 ? "mixed" : [...brands][0],
    total: amount,
    items: itemLines,
    method: $<HTMLInputElement>("[name=payment]:checked").value,
    customer,
    amountByBrand,
  });
  if (method === "credit") {
    const account = accounts.find((a) => a.id === customerId)!;
    let due = amount;
    const used = Math.min(account.credit, due);
    account.credit -= used;
    account.purchases.push({
      id: sales[sales.length - 1].id,
      date: l("Hoy", "Today"),
      items: itemLines.join(", "),
      amount: due,
      paid: used,
    });
    receipt.append(
      node(
        "p",
        l("A crédito · queda por cobrar a ", "On credit · added to the account of ") +
          account.name,
      ),
    );
  }
  $("#receipt-total").textContent = money(amount);
  cart.clear();
  field.value = "0";
  render();
  $<HTMLDialogElement>("#checkout-dialog").close();
  $<HTMLDialogElement>("#receipt-dialog").showModal();
});
$("#receipt-dialog").addEventListener("close", () =>
  $<HTMLElement>(".product-tile")?.focus(),
);
$("#receipt-dialog [data-close-receipt]").addEventListener("click", () =>
  $<HTMLDialogElement>("#receipt-dialog").close(),
);
if (!erp) {
  $<HTMLButtonElement>("#payment-form button[type=submit]").disabled = false;
  $("#payment-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const input = $<HTMLInputElement>("#payment-amount");
    if (!paymentAccount || !input.checkValidity()) return input.reportValidity();
    let left = Math.round(Number(input.value));
    paymentAccount.payments.push({ date: l("Hoy", "Today"), amount: left });
    for (const p of paymentAccount.purchases) {
      const part = Math.min(left, p.amount - p.paid);
      p.paid += part;
      left -= part;
    }
    paymentAccount.credit += left;
    renderDebts();
    $<HTMLDialogElement>("#payment-dialog").close();
    notice(
      left
        ? l("Abono registrado. Sobraron ", "Payment recorded. ") +
            money(left) +
            l(" como saldo a favor.", " became store credit.")
        : l("Abono registrado en la cuenta.", "Payment recorded on the account."),
    );
  });
  $("#statement-share").addEventListener("click", () =>
    notice(
      l(
        "En la aplicación se abre el chat de WhatsApp del cliente con el estado de cuenta. En esta demo no se envía nada.",
        "In the app this opens the customer’s WhatsApp chat with the statement. Nothing is sent in this demo.",
      ),
    ),
  );
  $("#backup-now").addEventListener("click", () => {
    $("#backup-status").textContent = l(
      "Conectada · última copia hace un momento (simulada)",
      "Connected · last copy just now (simulated)",
    );
    notice(l("Copia simulada. No se envió ningún dato.", "Simulated backup. No data was sent."));
  });
  $$<HTMLInputElement>("[name=payment]").forEach((r) =>
    r.addEventListener("change", () => ($("#credit-note").textContent = "")),
  );
}
$$<HTMLButtonElement>("[data-accent]").forEach((b) =>
  b.addEventListener("click", () => {
    document.body.style.setProperty("--action", b.dataset.accent!);
    $$("[data-accent]").forEach((x) =>
      x.setAttribute("aria-pressed", String(x === b)),
    );
    notice(
      l("Acento actualizado para esta demo.", "Accent updated for this demo."),
    );
  }),
);
render();
