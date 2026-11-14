import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink } from '@angular/router';

/** Page shown when the route matches no view (SPEC-04/E-34). */
@Component({
  selector: 'app-not-found',
  imports: [RouterLink],
  template: `
    <h1>Página no encontrada</h1>
    <p>La dirección que has abierto no corresponde a ninguna página.</p>
    <p><a routerLink="/">Volver al panel</a></p>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class NotFound {}
