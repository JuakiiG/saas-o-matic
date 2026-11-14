import { provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { App } from './app';
import { appConfig } from './app.config';

// SPEC-04/E-34 and the last row of the table of 2.1. The rows of the four views join this file
// as each view arrives (CA-11).
describe('Routes · SPEC-04/E-34', () => {
  async function open(url: string): Promise<HTMLElement> {
    TestBed.configureTestingModule({
      imports: [App],
      // The real configuration of the application, with the network replaced: no test goes out.
      providers: [...appConfig.providers, provideHttpClientTesting()],
    });
    const fixture = TestBed.createComponent(App);
    await expect(TestBed.inject(Router).navigateByUrl(url)).resolves.toBe(true);
    await fixture.whenStable();
    return fixture.nativeElement as HTMLElement;
  }

  it('should show the panel when the route is the root (SPEC-04 2.1)', async () => {
    const page = await open('/');

    expect(page.querySelector('main h1')?.textContent?.trim()).toBe('Clientes');
  });

  it('should show the sign-up when the route is /clientes/nuevo (SPEC-04 2.1)', async () => {
    const page = await open('/clientes/nuevo');

    expect(page.querySelector('main h1')?.textContent?.trim()).toBe('Nuevo cliente');
  });

  it('should show the detail when the route is /clientes/:id (SPEC-04 2.1)', async () => {
    const page = await open('/clientes/7');

    expect(page.querySelector('main h1')?.textContent?.trim()).toBe('Detalle del cliente');
  });

  it('should show the not found page when the route matches no view', async () => {
    const page = await open('/esta-ruta-no-existe');

    expect(page.querySelector('main h1')?.textContent?.trim()).toBe('Página no encontrada');
  });

  it('should offer a link to the panel when the route matches no view', async () => {
    const page = await open('/clientes/7/otra-cosa');

    const link = page.querySelector('main a');
    expect(link?.textContent?.trim()).toBe('Volver al panel');
    expect(link?.getAttribute('href')).toBe('/');
  });
});
