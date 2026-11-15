import { Routes } from '@angular/router';

const APPLICATION_NAME = 'SaaS-O-Matic';

/** The title of the document of a view: its name and, behind, the application's (E-57). */
function titleOf(view: string): string {
  return `${view} · ${APPLICATION_NAME}`;
}

// SPEC-04, 2.1. Every view is loaded lazily (`.claude/rules/frontend.md`).
export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    title: titleOf('Clientes'),
    loadComponent: () => import('./features/panel/panel').then((file) => file.Panel),
  },
  {
    path: 'clientes/nuevo',
    title: titleOf('Nuevo cliente'),
    loadComponent: () => import('./features/alta/alta').then((file) => file.Alta),
  },
  {
    path: 'clientes/:id',
    title: titleOf('Detalle del cliente'),
    loadComponent: () => import('./features/detalle/detalle').then((file) => file.Detalle),
  },
  {
    path: 'clientes/:id/simulacion',
    title: titleOf('Simulador'),
    loadComponent: () => import('./features/simulador/simulador').then((file) => file.Simulador),
  },
  {
    path: '**',
    loadComponent: () => import('./features/not-found/not-found').then((file) => file.NotFound),
  },
];
