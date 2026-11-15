import { Locator, Page } from '@playwright/test';

// How the tests find what the views show. Kept in one place: if a view changes its markup,
// this is the only file to correct.

/** The value shown next to a label (`Usuarios activos` → `15`) inside a card or a panel. */
export function fact(container: Locator, label: string): Locator {
  return container
    .locator('dl > div')
    .filter({ has: container.page().getByText(label, { exact: true }) })
    .locator('dd');
}

/** The projection of the simulator: tiers, base, tax and total. */
export function projection(page: Page): Locator {
  return page.getByRole('region', { name: 'Proyección' });
}

/** The cards of the history of the detail, in the order they are shown. */
export function historyCards(page: Page): Locator {
  return page.locator('ul.history > li');
}

/** The cards of the list of the panel, in the order they are shown. */
export function resultCards(page: Page): Locator {
  return page.locator('ul.results > li');
}

/** The rate applied and its date, shown next to converted amounts. */
export function rateApplied(container: Locator | Page): Locator {
  return container.locator('.rate-applied');
}

/** The currency selector of the header. */
export function currencySelect(page: Page): Locator {
  return page.getByLabel('Divisa');
}
