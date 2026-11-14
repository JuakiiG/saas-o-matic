import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink } from '@angular/router';

/**
 * View «Cliente no encontrado» of the detail and of the simulator (SPEC-04/E-15): the id of the
 * route has not the shape of an id, or the backend says there is no such customer.
 */
@Component({
  selector: 'app-customer-not-found',
  imports: [RouterLink],
  template: `
    <h1>Cliente no encontrado</h1>
    <p>No hay ningún cliente en esta dirección.</p>
    <p><a routerLink="/">Volver al panel</a></p>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CustomerNotFound {}
