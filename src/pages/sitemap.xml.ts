import type { APIRoute } from 'astro';
import { projects } from '../data/projects';
import { forms } from '../data/forms';
export const GET: APIRoute = ({ site }) => {
  const base=import.meta.env.BASE_URL;
  const urls=[...['es','en'].flatMap(lang=>[`${lang}/`,...projects.map(p=>`${lang}/proyectos/${p.id}/`)]),...forms.map(f=>`es/formularios/${f.slug}/`)];
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls.map(path=>`<url><loc>${new URL(base+path,site).href}</loc></url>`).join('')}</urlset>`,{headers:{'Content-Type':'application/xml; charset=utf-8'}});
};
