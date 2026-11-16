// Client intake forms. Each page sends its answers to the linked Google Form
// (and from there to its response spreadsheet). `entry` is the Google Forms
// field ID and option texts must match the Google Form exactly, or Google
// ignores the answer. To change a question, edit the Google Form first and
// then copy the new text here.
export type Question = {
  entry: number;
  label: string;
  help?: string;
  kind: 'text' | 'long' | 'radio' | 'checkbox';
  options?: string[];
  other?: boolean;
  required?: boolean;
  max?: number;
  input?: 'tel' | 'url' | 'text';
  autocomplete?: string;
  placeholder?: string;
};
export type FormSection = { title: string; help?: string; questions: Question[] };
export type IntakeForm = {
  slug: string; formId: string; sheet: string;
  name: string; nav: string; eyebrow: string; title: string; titleAccent: string; lead: string; minutes: number;
  card: string; whatsappLabel: string; sections: FormSection[];
};

const contact = (ids: [number, number, number, number]): FormSection => ({
  title: 'Tus datos de contacto',
  help: 'Solo los usamos para responderte sobre esta solicitud.',
  questions: [
    { entry: ids[0], label: '¿Cómo te llamas?', kind: 'text', required: true, autocomplete: 'name', placeholder: 'Tu nombre' },
    { entry: ids[1], label: '¿Cómo se llama tu negocio?', kind: 'text', required: true, autocomplete: 'organization', placeholder: 'Nombre del negocio' },
    { entry: ids[2], label: '¿A qué WhatsApp te escribimos?', help: 'Número con indicativo, por ejemplo 57 300 000 0000.', kind: 'text', required: true, input: 'tel', autocomplete: 'tel', placeholder: '57 300 000 0000' },
    { entry: ids[3], label: '¿En qué ciudad estás?', kind: 'text', autocomplete: 'address-level2', placeholder: 'Ciudad' },
  ],
});

const closing = (date: number, budget: number | null, extra: number, budgetHelp = ''): FormSection => ({
  title: 'Cierre',
  questions: [
    { entry: date, label: '¿Para qué fecha lo necesitas?', kind: 'text', placeholder: 'Por ejemplo: finales de diciembre' },
    ...(budget ? [{ entry: budget, label: 'Presupuesto aproximado (opcional)', help: budgetHelp, kind: 'text' as const, placeholder: 'Por ejemplo: entre 1 y 2 millones' }] : []),
    { entry: extra, label: '¿Algo más que debamos saber?', kind: 'long' },
  ],
});

export const forms: IntakeForm[] = [
  {
    slug: 'diseno-de-marca',
    formId: '1FAIpQLSdu3qX5PhCLSIaZk92n8kqqYXD-owWUne7xrNvqDRUmt6jlHw',
    sheet: '1wGUikwweh-Mf9GvF49HY5fpSp-BL84yjdq4GxkUOHvk',
    name: 'Diseño de marca', nav: 'Diseño de marca',
    eyebrow: 'FORMULARIO DE BRIEF / IDENTIDAD VISUAL',
    title: 'Tu marca empieza', titleAccent: 'con tu historia',
    lead: 'Con tus respuestas creamos las 2 propuestas de logo de tu marca. Responde con tus palabras; si alguna pregunta no aplica, escribe “no aplica”. Las imágenes de referencia o tu logo actual puedes enviarlos por WhatsApp.',
    minutes: 8,
    card: 'Logo, paleta, tipografías, piezas para redes e imagen corporativa. Cuéntanos de tu negocio y preparamos 2 propuestas.',
    whatsappLabel: 'Diseño de marca (brief de identidad visual)',
    sections: [
      contact([1894455767, 869340618, 1152472857, 26859726]),
      { title: 'Datos básicos', questions: [
        { entry: 404708001, label: 'Nombre exacto de la marca', help: 'Tal como debe aparecer en el logo, con tildes y mayúsculas.', kind: 'text', required: true },
        { entry: 439802491, label: 'Eslogan o frase', help: 'Escríbelo tal cual, o “no tengo”.', kind: 'text' },
        { entry: 1241882018, label: '¿Qué vendes u ofreces?', help: 'Tus productos o servicios principales.', kind: 'long', required: true },
        { entry: 1088656602, label: '¿Dónde vendes?', help: 'Local, domicilios, redes sociales, ferias, tienda en línea… y en qué ciudad.', kind: 'text' },
        { entry: 1655013243, label: '¿Desde cuándo existe el negocio?', help: 'O “apenas voy a empezar”.', kind: 'text' },
      ] },
      { title: 'Tu cliente', questions: [
        { entry: 2013434430, label: '¿Quién te compra?', help: 'Edad aproximada, tipo de persona y qué busca.', kind: 'long', required: true },
        { entry: 762744005, label: '¿Por qué te eligen a ti y no a otro?', help: 'Lo que te hace diferente.', kind: 'long' },
        { entry: 709909975, label: 'Competencia', help: 'Nombra 2 o 3 negocios parecidos al tuyo y qué te gusta o no de su imagen.', kind: 'long' },
      ] },
      { title: 'Personalidad de la marca', questions: [
        { entry: 545890191, label: 'Elige hasta 3 palabras que describan cómo quieres que se sienta tu marca', kind: 'checkbox', required: true, max: 3, other: true,
          options: ['Cercana', 'Elegante', 'Divertida', 'Natural', 'Moderna', 'Artesanal', 'Tradicional', 'Juvenil', 'Premium', 'Tranquila', 'Energética'] },
        { entry: 680021241, label: '¿Qué NO quieres que transmita?', kind: 'long' },
        { entry: 1452805813, label: 'Colores', help: '¿Cuáles te gustan o quieres usar? ¿Cuáles no quieres?', kind: 'long' },
        { entry: 732759799, label: 'Tipo de logo', kind: 'radio', options: ['Un dibujo o símbolo junto al nombre', 'Solo el nombre con una letra especial', 'No sé, propónganme'] },
        { entry: 454845003, label: 'Referencias', help: 'Cuéntanos qué logos o marcas te gustan (de cualquier tipo de negocio) y qué te gusta de cada una. Puedes pegar enlaces; las imágenes envíalas por WhatsApp.', kind: 'long' },
      ] },
      { title: 'Dónde usarás tu marca', questions: [
        { entry: 1693859056, label: '¿Dónde vas a usar el logo?', help: 'Marca todos los que apliquen.', kind: 'checkbox', other: true,
          options: ['Instagram', 'Facebook', 'WhatsApp', 'Etiquetas o stickers', 'Empaques o bolsas', 'Letrero o fachada', 'Uniformes', 'Sellos'] },
        { entry: 1200702426, label: '¿Vas a imprimir algo pronto?', help: 'Qué y de qué tamaño aproximado.', kind: 'text' },
        { entry: 1391600276, label: '¿Ya tienes un logo?', help: 'Si es así, cuéntanos qué quieres conservar o cambiar, y envíalo por WhatsApp.', kind: 'long' },
      ] },
      { title: 'Datos para tus piezas', help: 'Escribe solo los que quieras que aparezcan en banners y publicaciones; los que dejes vacíos no aparecerán.', questions: [
        { entry: 359707561, label: 'Instagram', kind: 'text', placeholder: '@tunegocio' },
        { entry: 1271262557, label: 'Facebook', kind: 'text' },
        { entry: 892119780, label: 'WhatsApp de ventas', kind: 'text', input: 'tel' },
        { entry: 1107179203, label: 'Ciudad o dirección', kind: 'text' },
        { entry: 1405630377, label: 'Sitio web', kind: 'text', input: 'url' },
      ] },
      closing(95054495, null, 1920298901),
    ],
  },
  {
    slug: 'pagina-web',
    formId: '1FAIpQLScoCZpSrCR1FxRWEx9EOFED_iNPYgigpCffvKmRIZc5jv15NQ',
    sheet: '1obz2XLmfubHgct0KC3sdyt0QAIxywEeaTLQcSLKaNwE',
    name: 'Página web', nav: 'Página web',
    eyebrow: 'ASESORÍA GRATUITA / PÁGINAS WEB A PEDIDO',
    title: 'Tu negocio,', titleAccent: 'abierto todo el día',
    lead: 'Responde estas preguntas para identificar qué tipo de página necesita tu negocio y prepararte una cotización personalizada. Si no sabes alguna respuesta, déjala en blanco: lo vemos juntos en la asesoría.',
    minutes: 6,
    card: 'Landing page, sitio corporativo, tienda o reservas. Te ayudamos a definir qué página necesitas.',
    whatsappLabel: 'Página web (asesoría gratuita)',
    sections: [
      contact([1833852943, 139347605, 1346367752, 1468497101]),
      { title: 'Tu negocio', questions: [
        { entry: 929785522, label: '¿A qué se dedica tu negocio?', help: 'Qué vendes u ofreces y a quién.', kind: 'long', required: true },
        { entry: 1104096903, label: '¿Tienes logo e identidad visual?', kind: 'radio', options: ['Sí, ya tengo logo y colores', 'Tengo logo, pero quiero renovarlo', 'No tengo; quiero cotizar también el diseño de marca'] },
        { entry: 502417450, label: '¿Ya tienes una página web?', help: 'Si sí, escribe la dirección (por ejemplo, minegocio.com).', kind: 'text' },
      ] },
      { title: 'Qué quieres lograr', questions: [
        { entry: 1115895082, label: '¿Para qué quieres la página?', help: 'Marca todo lo que aplique.', kind: 'checkbox', required: true, other: true,
          options: ['Mostrar mi negocio y que me contacten por WhatsApp', 'Vender productos en línea', 'Recibir reservas o citas', 'Mostrar mi catálogo o portafolio', 'Publicar noticias o artículos'] },
        { entry: 1507941834, label: '¿Qué tipo de página crees que necesitas?', help: 'Si no estás seguro, elige la última opción.', kind: 'radio', required: true,
          options: ['Una sola página con toda la información (landing page)', 'Sitio de varias páginas (inicio, servicios, nosotros, contacto…)', 'Tienda en línea', 'Sitio con reservas o agenda', 'No sé, quiero asesoría'] },
        { entry: 617335584, label: '¿Qué secciones te gustaría tener?', kind: 'checkbox', other: true,
          options: ['Inicio', 'Nosotros', 'Servicios o productos', 'Catálogo', 'Galería de fotos', 'Testimonios', 'Preguntas frecuentes', 'Contacto', 'Blog o noticias'] },
        { entry: 671301182, label: 'Si es tienda: ¿cuántos productos tendrías aproximadamente?', kind: 'text' },
        { entry: 617115153, label: '¿Qué funciones necesitas?', kind: 'checkbox', other: true,
          options: ['Botón de WhatsApp', 'Formulario de contacto', 'Mapa de ubicación', 'Enlaces a redes sociales', 'Pagos en línea', 'Reservas o agenda', 'Varios idiomas'] },
      ] },
      { title: 'Contenido y mantenimiento', questions: [
        { entry: 1528542014, label: '¿Tienes los textos y fotos para la página?', kind: 'radio', options: ['Sí, tengo todo listo', 'Tengo una parte', 'Necesito ayuda con textos y fotos'] },
        { entry: 2141205602, label: '¿Tienes dominio (la dirección .com o .co)?', kind: 'radio', options: ['Sí, ya tengo dominio', 'No tengo', 'No sé qué es'] },
        { entry: 1334180342, label: 'Si ya tienes dominio, ¿cuál es?', kind: 'text' },
        { entry: 1169856760, label: '¿Quién actualizará la página después?', kind: 'radio', options: ['Yo quiero poder editarla', 'Prefiero que ustedes la actualicen', 'Casi no va a cambiar'] },
        { entry: 774030559, label: 'Páginas que te gusten', help: 'Pega 2 o 3 enlaces de páginas que te gusten y cuéntanos por qué.', kind: 'long' },
      ] },
      closing(1318511731, 1920335002, 568024980, 'Nos ayuda a proponerte la opción que mejor se ajuste.'),
    ],
  },
  {
    slug: 'software-a-medida',
    formId: '1FAIpQLSfPvvuRwGzQ2Sl9dR12ZMgJMlYVWppFHdshU-k7D4YCaPEWHQ',
    sheet: '13xJFqGetHRHbZbrGHmtlUfgmmQ6ygY7VxaA5gG3iNRc',
    name: 'Software a medida', nav: 'Software a medida',
    eyebrow: 'DIAGNÓSTICO / SOFTWARE PERSONALIZADO',
    title: 'Ordenemos', titleAccent: 'tu operación',
    lead: 'Cuéntanos qué proceso de tu negocio quieres organizar o automatizar. Con tus respuestas preparamos una propuesta y una cotización personalizada. No necesitas saber de tecnología: responde con tus palabras.',
    minutes: 7,
    card: 'Inventario, ventas, citas, pedidos o cotizaciones. Diagnosticamos tu proceso y proponemos un sistema.',
    whatsappLabel: 'Software a medida (diagnóstico)',
    sections: [
      contact([14661213, 2056845015, 1097045323, 1494920561]),
      { title: 'Tu negocio', questions: [
        { entry: 1041063444, label: '¿A qué se dedica tu negocio?', kind: 'long', required: true },
        { entry: 548069723, label: '¿Cuántas personas trabajan en el negocio?', kind: 'radio', options: ['Solo yo', '2 a 5', '6 a 20', 'Más de 20'] },
      ] },
      { title: 'El problema', questions: [
        { entry: 1315593656, label: '¿Qué proceso quieres organizar o automatizar?', help: 'Por ejemplo: inventario, ventas, citas, pedidos, cotizaciones.', kind: 'long', required: true },
        { entry: 1490566915, label: '¿Cómo lo hacen hoy?', kind: 'checkbox', other: true, options: ['En papel o cuaderno', 'En Excel o Google Sheets', 'Por WhatsApp', 'Con otro programa'] },
        { entry: 470636698, label: 'Si usan otro programa, ¿cuál?', kind: 'text' },
        { entry: 2128614363, label: '¿Qué es lo que más tiempo les quita o más errores causa hoy?', kind: 'long', required: true },
        { entry: 394303954, label: '¿Qué áreas debería cubrir el sistema?', kind: 'checkbox', other: true,
          options: ['Inventario', 'Ventas o punto de venta', 'Facturación', 'Clientes', 'Citas o agenda', 'Pedidos', 'Cotizaciones', 'Empleados o turnos', 'Reportes'] },
      ] },
      { title: 'Uso', questions: [
        { entry: 435506875, label: '¿Quiénes lo usarán y cuántas personas?', help: 'Por ejemplo: “yo y 2 vendedores”.', kind: 'text' },
        { entry: 1110353098, label: '¿Desde dónde lo usarán?', kind: 'checkbox', options: ['Computador', 'Celular', 'Tablet'] },
        { entry: 656877738, label: '¿Necesita funcionar sin internet?', kind: 'radio', options: ['Sí', 'No', 'No sé'] },
        { entry: 1211139491, label: '¿Debe conectarse con algo que ya usan?', help: 'Por ejemplo: facturación electrónica, pagos en línea, WhatsApp, Excel u otro programa.', kind: 'long' },
        { entry: 1363059296, label: '¿Tienen información que haya que pasar al nuevo sistema?', kind: 'radio', options: ['Sí, en Excel o Sheets', 'Sí, en otro programa', 'Sí, en papel', 'No, empezamos de cero'] },
      ] },
      { title: 'Resultado ideal', questions: [
        { entry: 2037241395, label: 'Si el sistema ya existiera, ¿qué harías con él en un día normal?', help: 'Descríbelo con tus palabras, paso a paso si puedes.', kind: 'long', required: true },
        { entry: 906474384, label: '¿Conoces algún programa parecido a lo que imaginas?', help: 'Nombre o enlace, y qué te gusta o no de él.', kind: 'long' },
      ] },
      closing(809858323, 751423520, 1935813070, 'Nos ayuda a proponerte una solución por fases si hace falta.'),
    ],
  },
];
