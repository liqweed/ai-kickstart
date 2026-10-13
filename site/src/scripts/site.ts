// The site's only script bundle. Each part checks for its own markup, so one file serves every page.
import { initBanners } from "./banners.ts";
import { initCatalog } from "./catalog.ts";
import { initNews } from "./news.ts";
import { initPrompts } from "./prompts.ts";
import { initSetup } from "./setup.ts";
import { initStart } from "./start.ts";
import { initTheme } from "./theme.ts";

initTheme();
initPrompts();
initBanners();
initStart();
initSetup();
initCatalog();
initNews();

// Phone header: keep the current place visible in the scrolling nav.
const current = document.querySelector<HTMLElement>('.site-nav [aria-current="page"]');
current?.scrollIntoView({ block: "nearest", inline: "nearest" });
