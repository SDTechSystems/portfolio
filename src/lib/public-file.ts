import fs from 'node:fs';
import path from 'node:path';
// True when a file exists in public/ at build time. Lets pages show a blank placeholder
// until a photo or screenshot is added, without broken images.
export const publicExists = (file: string) => fs.existsSync(path.join(process.cwd(), 'public', file));
