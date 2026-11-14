import { provideHttpClient } from '@angular/common/http';
import {
  ApplicationConfig,
  inject,
  provideAppInitializer,
  provideBrowserGlobalErrorListeners,
} from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { MetaStore } from './core/meta-store';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    // No interceptors: a header added by one would make the backend reject the CORS preflight
    // (SPEC-04, 2.9).
    provideHttpClient(),
    // `/meta` is asked once, when the application starts (SPEC-04/E-39). The initializer returns
    // nothing, so the start does not wait for the answer: each view shows its loading state.
    provideAppInitializer(() => inject(MetaStore).load()),
  ],
};
