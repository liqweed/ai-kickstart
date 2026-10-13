// Runs in <head> before the first paint, so a chosen theme never flashes the other one. Astro doesn't
// hash is:inline scripts, so astro.config.mjs hashes this exact text into the CSP.
export const THEME_BOOT =
  'try{var t=localStorage.getItem("aik.site.theme");if(t==="light"||t==="dark")document.documentElement.dataset.kk=t}catch(e){}';
