import { Routes } from '@angular/router';

// SPEC-04, 2.1. Every view is loaded lazily (`.claude/rules/frontend.md`).
export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    loadComponent: () => import('./features/panel/panel').then((file) => file.Panel),
  },
  {
    path: 'clientes/nuevo',
    loadComponent: () => import('./features/alta/alta').then((file) => file.Alta),
  },
  {
    path: 'clientes/:id',
    loadComponent: () => import('./features/detalle/detalle').then((file) => file.Detalle),
  },
  {
    path: '**',
    loadComponent: () => import('./features/not-found/not-found').then((file) => file.NotFound),
  },
];
