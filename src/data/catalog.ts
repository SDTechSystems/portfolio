export type Locale = 'es' | 'en';
// Edit these entries to add, rename, reorder or hide categories.
// Products may belong to several categories; an empty category has a contact message.
export const categories = [
  { id: 'erp', label: { es: 'Software ERP', en: 'ERP software' }, visible: true },
  { id: 'pos', label: { es: 'Punto de venta', en: 'Point of sale' }, visible: true },
  { id: 'custom', label: { es: 'Software a medida', en: 'Custom software' }, visible: true },
  { id: 'akashic', label: { es: 'Akashic Vault', en: 'Akashic Vault' }, visible: true },
  { id: 'websites', label: { es: 'Páginas web a medida', en: 'Custom websites' }, visible: true },
  { id: 'landing', label: { es: 'Landing pages', en: 'Landing pages' }, visible: true },
];
export const assignments: Record<string, string[]> = {
  'akashic-vault': ['akashic'],
  openmultipos: ['erp', 'pos', 'custom'],
  'easy-drink': ['pos'],
  'akashic-tv': ['custom'],
  invitacion: ['websites', 'custom'],
  tasktone: ['custom', 'websites'],
};
export const siteConfig = {
  name: 'SD Tech Systems',
  author: 'Juan Sebastián Duque Valencia',
  email: 'contacto@sdtechsystems.dev',
  github: 'https://github.com/SDTechSystems',
  // WhatsApp Business with country code, digits only (57 = Colombia).
  whatsapp: '573058147293',
  defaultLocale: 'es' as Locale,
};

// wa.me link that opens the chat with a pre-written message.
export const waLink = (text:string) => `https://wa.me/${siteConfig.whatsapp}?text=${encodeURIComponent(text)}`;
export const waMessages = {
  portfolio: { es:'Hola Juan, estuve viendo el portafolio de SD Tech Systems y me gustaría hablar sobre un proyecto.', en:'Hi Juan, I was looking at the SD Tech Systems portfolio and would like to talk about a project.' },
  projects: { es:'Hola Juan, vi los proyectos de tu portafolio y quiero saber cuál solución se adapta a mi negocio.', en:'Hi Juan, I saw the projects in your portfolio and would like to know which solution fits my business.' },
  contact: { es:'Hola Juan, vengo de la sección de contacto de tu portafolio. Tengo una idea y me gustaría conversarla contigo.', en:'Hi Juan, I’m coming from the contact section of your portfolio. I have an idea and would like to discuss it with you.' },
  quotes: { es:'Hola Juan, quiero cotizar un proyecto con SD Tech Systems, pero aún no sé cuál formulario llenar.', en:'Hi Juan, I’d like a quote from SD Tech Systems, but I’m not sure which form to fill in.' },
  project: (name:string,locale:Locale) => locale==='es'
    ? `Hola Juan, estuve viendo ${name} en tu portafolio y me interesa una solución así para mi negocio.`
    : `Hi Juan, I was looking at ${name} in your portfolio and I’m interested in a similar solution for my business.`,
  brands: { es:'Hola Juan, vi los diseños de marca de tu portafolio y quiero cotizar la identidad de mi negocio.', en:'Hi Juan, I saw the brand designs in your portfolio and I’d like a quote for my business identity.' },
  // Tells Juan exactly which showcase design the client liked, with its link.
  brand: (name:string,style:string,url:string,locale:Locale) => locale==='es'
    ? `Hola Juan, me gustó el diseño de marca «${name}» (${style.toLowerCase()}) de tu portafolio y quiero algo así para mi negocio: ${url}`
    : `Hi Juan, I liked the «${name}» brand design (${style.toLowerCase()}) in your portfolio and I’d like something like it for my business: ${url}`,
  demo: (name:string,locale:Locale) => locale==='es'
    ? `Hola Juan, estuve probando la demo de ${name} en tu portafolio y quiero saber más.`
    : `Hi Juan, I was trying the ${name} demo in your portfolio and would like to know more.`,
};

// "Act. nov 2026" from an ISO date or a bare year.
export const formatUpdated = (value:string,locale:Locale) => {
  if(/^\d{4}$/.test(value)) return value;
  const date=new Date(`${value}T12:00:00`);
  return new Intl.DateTimeFormat(locale==='es'?'es-CO':'en-US',{day:'numeric',month:'short',year:'numeric'}).format(date).replace('.','');
};

// Routes to full, anonymous product showcases (relative to each language root).
export const demoKinds = {
  'akashic-vault': 'reconstructed', openmultipos: 'adapted', 'easy-drink': 'reconstructed',
  'akashic-tv': 'reconstructed', tasktone: 'concept', invitacion: 'adapted',
} as const;
export const interactiveDemos: Record<string,string> = Object.fromEntries(
  Object.keys(demoKinds).map(id=>[id,`demos/${id}/`]),
);
export type SoftwareDemoId = Exclude<keyof typeof demoKinds, 'invitacion'>;
export const demoLabel = (id:string,locale:Locale) => id==='invitacion'
  ? (locale==='es'?'Ver sitio interactivo':'Explore interactive website')
  : (locale==='es'?'Explorar demo':'Explore demo');
