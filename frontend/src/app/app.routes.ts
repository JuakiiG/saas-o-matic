import { Routes } from '@angular/router';

// SPEC-04, 2.1. Every view is loaded lazily (`.claude/rules/frontend.md`).
export const routes: Routes = [
  {
    path: '**',
    loadComponent: () => import('./features/not-found/not-found').then((file) => file.NotFound),
  },
];
