import { provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { App } from './app';
import { appConfig } from './app.config';

// CA-11: the five rows of the table of SPEC-04, 2.1, the not found page among them (E-34), and
// the title each of the five views gives to the document (E-57).
describe('Routes · SPEC-04/E-34, E-57 (CA-11)', () => {
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

  it('should show the simulator when the route is /clientes/:id/simulacion (SPEC-04 2.1)', async () => {
    const page = await open('/clientes/7/simulacion');

    expect(page.querySelector('main h1')?.textContent?.trim()).toBe('Simulador');
  });

  // SPEC-04/E-57: the name of the view and, behind, the name of the application.
  it.each([
    ['/', 'Clientes · SaaS-O-Matic'],
    ['/clientes/nuevo', 'Nuevo cliente · SaaS-O-Matic'],
    ['/clientes/7', 'Detalle del cliente · SaaS-O-Matic'],
    ['/clientes/7/simulacion', 'Simulador · SaaS-O-Matic'],
    ['/esta-ruta-no-existe', 'Página no encontrada · SaaS-O-Matic'],
  ])('should title the document of %s as «%s» (SPEC-04/E-57)', async (url, title) => {
    document.title = 'The title of a page opened before';

    await open(url);

    expect(document.title).toBe(title);
  });

  // The router only changes the title when the route brings one: without its own, the not
  // found page would keep the title of the view the user comes from.
  it('should title the not found page with its own title when it is reached from the panel (SPEC-04/E-57)', async () => {
    await open('/');
    expect(document.title).toBe('Clientes · SaaS-O-Matic');

    await expect(TestBed.inject(Router).navigateByUrl('/esta-ruta-no-existe')).resolves.toBe(true);

    expect(document.title).toBe('Página no encontrada · SaaS-O-Matic');
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
