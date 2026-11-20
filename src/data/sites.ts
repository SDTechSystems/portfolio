import type { Locale } from './catalog';
// Sample websites shown in /paginas/. Landings and stores are fictional businesses built on the
// sample brands of /marcas/ (same logo, palette and typefaces); their pages live in src/pages/muestras/.
export type SiteKind = 'landing' | 'store' | 'custom';
type T = Record<Locale, string>;
export type SampleSite = {
  slug: string; brand?: string; name: string; kind: SiteKind; style: T; sector: T; title: T; summary: T;
  features: Record<Locale, string[]>; colors: string[];
  // Link relative to the site root ({lang} is replaced with the visitor's language).
  href: string; cover: string;
};
export const siteKinds: { id: SiteKind; label: T; one: T }[] = [
  { id: 'landing', label: { es: 'Landing pages', en: 'Landing pages' }, one: { es: 'Landing page', en: 'Landing page' } },
  { id: 'store', label: { es: 'Tiendas online', en: 'Online stores' }, one: { es: 'Tienda online', en: 'Online store' } },
  { id: 'custom', label: { es: 'Sitios a medida', en: 'Custom websites' }, one: { es: 'Página a medida', en: 'Custom website' } },
];
const sample = (slug: string) => ({ href: `muestras/${slug}/`, cover: `muestras/${slug}/portada.webp` });
export const sites: SampleSite[] = [
  {
    slug: 'brasa-brava', brand: 'brasa-brava', name: 'Brasa Brava', kind: 'landing', ...sample('brasa-brava'),
    style: { es: 'Llamativa', en: 'Bold' }, sector: { es: 'Hamburguesería', en: 'Burger joint' },
    title: { es: 'Hambre de pedir desde el primer vistazo.', en: 'Hungry to order at first sight.' },
    summary: { es: 'Landing de restaurante con letras gigantes, combos con precio, horario en vivo y pedido directo por WhatsApp.', en: 'Restaurant landing with huge type, priced combos, live opening hours and direct WhatsApp ordering.' },
    features: { es: ['Menú de combos con precios', 'Pedido por WhatsApp con el combo elegido', 'Aviso de abierto o cerrado según la hora', 'Sedes con horarios y cómo llegar'], en: ['Combo menu with prices', 'WhatsApp order with the chosen combo', 'Open or closed notice based on the time', 'Locations with hours and directions'] },
    colors: ['#E1341E', '#FFC12E', '#1B1615', '#FFF3E2'],
  },
  {
    slug: 'sereno', brand: 'sereno', name: 'Sereno', kind: 'landing', ...sample('sereno'),
    style: { es: 'Minimalista', en: 'Minimal' }, sector: { es: 'Cuidado de la piel', en: 'Skincare' },
    title: { es: 'Mucho aire, poco ruido, un solo producto.', en: 'Plenty of air, little noise, one product.' },
    summary: { es: 'Landing de lanzamiento para un sérum: ritual en tres pasos, ingredientes claros, preguntas frecuentes y lista de espera.', en: 'Launch landing for a serum: a three-step ritual, clear ingredients, FAQ and a waiting list.' },
    features: { es: ['Ritual en tres pasos', 'Ingredientes explicados sin tecnicismos', 'Preguntas frecuentes desplegables', 'Lista de espera con confirmación'], en: ['Three-step ritual', 'Ingredients explained in plain words', 'Expandable FAQ', 'Waiting list with confirmation'] },
    colors: ['#F4F0EA', '#DCCFBE', '#8C9A84', '#2E2E2C'],
  },
  {
    slug: 'aurelia', brand: 'aurelia', name: 'Aurelia Hotel & Spa', kind: 'landing', ...sample('aurelia'),
    style: { es: 'Lujo', en: 'Luxury' }, sector: { es: 'Hotel boutique y spa', en: 'Boutique hotel and spa' },
    title: { es: 'Reservas con la calma de un hotel cinco estrellas.', en: 'Bookings with five-star calm.' },
    summary: { es: 'Landing elegante para hotel: suites, spa, gastronomía, experiencias y un cotizador de estadía que arma la solicitud de reserva.', en: 'Elegant hotel landing: suites, spa, dining, experiences and a stay estimator that prepares the booking request.' },
    features: { es: ['Suites con tarifas por noche', 'Cotizador de estadía por fechas y huéspedes', 'Experiencias y spa', 'Solicitud de reserva por WhatsApp'], en: ['Suites with nightly rates', 'Stay estimator by dates and guests', 'Experiences and spa', 'Booking request via WhatsApp'] },
    colors: ['#0F3B32', '#C9A45C', '#F3EDE1', '#8FA89A'],
  },
  {
    slug: 'orbita', brand: 'orbita', name: 'Órbita Software', kind: 'landing', ...sample('orbita'),
    style: { es: 'Tecnológica', en: 'Tech' }, sector: { es: 'Estudio de software', en: 'Software studio' },
    title: { es: 'Una landing que vende como un producto digital.', en: 'A landing that sells like a digital product.' },
    summary: { es: 'Landing de empresa tecnológica en modo oscuro: servicios, proceso, métricas animadas, planes con selector mensual o anual y contacto.', en: 'Dark-mode tech company landing: services, process, animated metrics, plans with a monthly or yearly switch and contact.' },
    features: { es: ['Métricas que cuentan al aparecer', 'Planes con precio mensual o anual', 'Proceso de trabajo por etapas', 'Formulario de contacto de ejemplo'], en: ['Metrics that count up on view', 'Plans with monthly or yearly pricing', 'Step-by-step process', 'Sample contact form'] },
    colors: ['#6C4CFF', '#29D3F5', '#0B0F2A', '#EEF1FF'],
  },
  {
    slug: 'arco', brand: 'arco', name: 'Arco Odontología', kind: 'landing', ...sample('arco'),
    style: { es: 'Sobria', en: 'Professional' }, sector: { es: 'Clínica odontológica', en: 'Dental clinic' },
    title: { es: 'Confianza clínica y citas en tres toques.', en: 'Clinical trust and appointments in three taps.' },
    summary: { es: 'Landing para consultorio: tratamientos, equipo de especialistas, testimonios, convenios y agendamiento de cita guiado.', en: 'Clinic landing: treatments, specialist team, testimonials, partners and a guided appointment request.' },
    features: { es: ['Agendamiento por tratamiento, día y hora', 'Equipo de especialistas', 'Testimonios y convenios', 'Botón de urgencias visible'], en: ['Appointment by treatment, day and time', 'Specialist team', 'Testimonials and partners', 'Visible emergency button'] },
    colors: ['#1C5DB0', '#35C2C9', '#F4F9FC', '#2B3443'],
  },
  {
    slug: 'la-navaja', brand: 'la-navaja', name: 'La Navaja Barbería', kind: 'landing', ...sample('la-navaja'),
    style: { es: 'Retro', en: 'Retro' }, sector: { es: 'Barbería clásica', en: 'Classic barbershop' },
    title: { es: 'El oficio de siempre con reservas de hoy.', en: 'Old-school craft with modern booking.' },
    summary: { es: 'Landing con estética de barbería antigua: lista de precios tipo pizarra, barberos, galería de cortes y reserva de turno.', en: 'Vintage barbershop landing: chalkboard price list, barbers, haircut gallery and slot booking.' },
    features: { es: ['Lista de precios estilo pizarra', 'Elección de barbero y turno', 'Galería de cortes', 'Horarios y ubicación'], en: ['Chalkboard-style price list', 'Choose your barber and slot', 'Haircut gallery', 'Hours and location'] },
    colors: ['#7A1F2B', '#F1E6D2', '#1E2A3A', '#B8914B'],
  },
  {
    slug: 'michi-firulais', brand: 'michi-firulais', name: 'Michi & Firulais', kind: 'store', ...sample('michi-firulais'),
    style: { es: 'Divertida', en: 'Playful' }, sector: { es: 'Tienda de mascotas', en: 'Pet shop' },
    title: { es: 'Una tienda alegre que se compra sola.', en: 'A cheerful store that sells itself.' },
    summary: { es: 'Tienda online con categorías por mascota, búsqueda, carrito, envío gratis desde un monto y pedido final por WhatsApp.', en: 'Online store with categories per pet, search, cart, free shipping over an amount and a final WhatsApp order.' },
    features: { es: ['Filtros por mascota y categoría', 'Búsqueda instantánea', 'Carrito con barra de envío gratis', 'Pedido listo para enviar por WhatsApp'], en: ['Filters by pet and category', 'Instant search', 'Cart with a free-shipping bar', 'Order ready to send via WhatsApp'] },
    colors: ['#FF8A3D', '#18A5A7', '#1F2D4A', '#FFF6E9'],
  },
  {
    slug: 'ebano', brand: 'ebano', name: 'Ébano Joyería', kind: 'store', ...sample('ebano'),
    style: { es: 'Elegante', en: 'Elegant' }, sector: { es: 'Joyería de autor', en: 'Designer jewelry' },
    title: { es: 'Una vitrina silenciosa para piezas que permanecen.', en: 'A quiet showcase for pieces that endure.' },
    summary: { es: 'Tienda online de lujo: colecciones, ficha de producto con talla y metal, carrito lateral, empaque de regalo y pedido asistido.', en: 'Luxury online store: collections, product sheet with size and metal, side cart, gift wrapping and assisted ordering.' },
    features: { es: ['Ficha de producto con talla y metal', 'Colecciones y orden por precio', 'Carrito lateral con empaque de regalo', 'Pedido asistido por un asesor'], en: ['Product sheet with size and metal', 'Collections and price sorting', 'Side cart with gift wrapping', 'Advisor-assisted ordering'] },
    colors: ['#121212', '#C9A96E', '#F4EEE4', '#BDB7AE'],
  },
  {
    slug: 'invitacion', name: 'Invitación de boda', kind: 'custom', href: '{lang}/demos/invitacion/', cover: 'screenshots/wedding-interactive-be7539825df8.png',
    style: { es: 'Romántica', en: 'Romantic' }, sector: { es: 'Evento · Proyecto entregado', en: 'Event · Delivered project' },
    title: { es: 'Una invitación que cuenta una historia.', en: 'An invitation that tells a story.' },
    summary: { es: 'Web de boda a medida, entregada y aprobada por el cliente: historia, galería, cuenta regresiva, mapas y confirmación de asistencia.', en: 'Custom wedding website, delivered and approved by the client: story, gallery, countdown, maps and RSVP.' },
    features: { es: ['Historia y galería con ampliación', 'Cuenta regresiva y mapas', 'Confirmación de asistencia por familia'], en: ['Story and gallery with zoom', 'Countdown and maps', 'RSVP per family'] },
    colors: ['#713c49', '#c7d1b9', '#fffdf8', '#2b2a28'],
  },
];
export const siteHref = (base: string, s: SampleSite, locale: Locale) => `${base}${s.href.replace('{lang}', locale)}`;
export const kindLabel = (kind: SiteKind, locale: Locale) => siteKinds.find(k => k.id === kind)!.one[locale];
