import type { Locale } from "./catalog";
export const sampleProducts = (locale: Locale) => {
  const en = locale === "en";
  return [
    {
      id: "p1",
      brand: "a",
      name: en ? "Cold brew" : "Café frío",
      category: "drinks",
      icon: "☕",
      price: 8500,
      stock: 32,
      stored: 8,
      sku: "DEMO-101",
    },
    {
      id: "p2",
      brand: "a",
      name: en ? "Tropical juice" : "Jugo tropical",
      category: "drinks",
      icon: "🍊",
      price: 6500,
      stock: 24,
      stored: 6,
      sku: "DEMO-102",
    },
    {
      id: "p3",
      brand: "a",
      name: en ? "Sparkling water" : "Agua con gas",
      category: "drinks",
      icon: "◉",
      price: 4000,
      stock: 48,
      stored: 24,
      sku: "DEMO-103",
    },
    {
      id: "p4",
      brand: "a",
      name: en ? "Chocolate cookie" : "Galleta de chocolate",
      category: "food",
      icon: "🍪",
      price: 4500,
      stock: 18,
      stored: 0,
      sku: "DEMO-104",
    },
    {
      id: "p5",
      brand: "a",
      name: en ? "Croissant" : "Croissant",
      category: "food",
      icon: "🥐",
      price: 6000,
      stock: 12,
      stored: 0,
      sku: "DEMO-105",
    },
    {
      id: "p6",
      brand: "a",
      name: en ? "Iced tea" : "Té helado",
      category: "drinks",
      icon: "🍵",
      price: 5500,
      stock: 4,
      stored: 0,
      sku: "DEMO-106",
    },
    {
      id: "p7",
      brand: "b",
      name: en ? "Desk lamp" : "Lámpara de escritorio",
      category: "tech",
      icon: "◒",
      price: 65000,
      stock: 8,
      stored: 0,
      sku: "DEMO-201",
    },
    {
      id: "p8",
      brand: "b",
      name: en ? "Wireless mouse" : "Mouse inalámbrico",
      category: "tech",
      icon: "◩",
      price: 42000,
      stock: 14,
      stored: 0,
      sku: "DEMO-202",
    },
    {
      id: "p9",
      brand: "b",
      name: en ? "USB-C cable" : "Cable USB-C",
      category: "tech",
      icon: "⌁",
      price: 18000,
      stock: 3,
      stored: 0,
      sku: "DEMO-203",
    },
    {
      id: "p10",
      brand: "b",
      name: en ? "Notebook" : "Libreta",
      category: "office",
      icon: "▤",
      price: 12000,
      stock: 25,
      stored: 0,
      sku: "DEMO-204",
    },
  ];
};
export type DemoProduct = ReturnType<typeof sampleProducts>[number];
export const sampleCustomers = (locale: Locale) => [
  {
    id: "c1",
    name: locale === "es" ? "Cliente de ejemplo A" : "Sample customer A",
    orders: 5,
    total: 128000,
  },
  {
    id: "c2",
    name: locale === "es" ? "Cliente de ejemplo B" : "Sample customer B",
    orders: 3,
    total: 76000,
  },
  {
    id: "c3",
    name: locale === "es" ? "Cliente de ejemplo C" : "Sample customer C",
    orders: 2,
    total: 45000,
  },
];

export type DemoPurchase = { id: string; date: string; items: string; amount: number; paid: number };
export type DemoAccount = { id: string; name: string; credit: number; purchases: DemoPurchase[]; payments: { date: string; amount: number }[] };
export const sampleAccounts = (locale: Locale): DemoAccount[] => {
  const en = locale === "en";
  return [
    {
      id: "c1",
      name: en ? "Sample customer A" : "Cliente de ejemplo A",
      credit: 0,
      purchases: [
        { id: "DEMO-F01", date: en ? "Mon" : "Lun", items: en ? "2 × Cold brew" : "2 × Café frío", amount: 17000, paid: 5000 },
        { id: "DEMO-F04", date: en ? "Wed" : "Mié", items: en ? "1 × Croissant, 1 × Tropical juice" : "1 × Croissant, 1 × Jugo tropical", amount: 12500, paid: 0 },
      ],
      payments: [{ date: en ? "Tue" : "Mar", amount: 5000 }],
    },
    {
      id: "c2",
      name: en ? "Sample customer B" : "Cliente de ejemplo B",
      credit: 3000,
      purchases: [],
      payments: [{ date: en ? "Thu" : "Jue", amount: 14000 }],
    },
    {
      id: "c3",
      name: en ? "Sample customer C" : "Cliente de ejemplo C",
      credit: 0,
      purchases: [
        { id: "DEMO-F06", date: en ? "Fri" : "Vie", items: en ? "2 × Chocolate cookie" : "2 × Galleta de chocolate", amount: 9000, paid: 0 },
      ],
      payments: [],
    },
  ];
};
