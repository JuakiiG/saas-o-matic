import { provideHttpClient } from '@angular/common/http';
import {
  ApplicationConfig,
  inject,
  provideAppInitializer,
  provideBrowserGlobalErrorListeners,
} from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { ExchangeRates } from './core/exchange-rates';
import { MetaStore } from './core/meta-store';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    // No interceptors: a header added by one would make the backend reject the CORS preflight
    // (SPEC-04, 2.9).
    provideHttpClient(),
    // `/meta` and the exchange rates are asked once each, when the application starts
    // (SPEC-04/E-39, E-26). The initializer returns nothing, so the start does not wait for the
    // answers: each view shows its loading state, and the selector offers euros meanwhile.
    provideAppInitializer(() => {
      inject(MetaStore).load();
      inject(ExchangeRates).load();
    }),
  ],
};
