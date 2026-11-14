import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../environments/environment';
import { App } from './app';
import { appConfig } from './app.config';

// SPEC-04, 2.1: a header shared by every view carries the application name, the link to the
// panel and the currency selector.
describe('App · SPEC-04 2.1', () => {
  async function render(): Promise<HTMLElement> {
    await TestBed.configureTestingModule({
      imports: [App],
      // The real configuration of the application, with the network replaced: no test goes out.
      providers: [...appConfig.providers, provideHttpClientTesting()],
    }).compileComponents();
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    return fixture.nativeElement as HTMLElement;
  }

  it('should show the application name in the header when it starts', async () => {
    const page = await render();

    expect(page.querySelector('header')?.textContent).toContain('SaaS-O-Matic');
  });

  it('should link to the panel from the header when it starts', async () => {
    const page = await render();

    const link = page.querySelector('header nav a');
    expect(link?.textContent?.trim()).toBe('Panel');
    expect(link?.getAttribute('href')).toBe('/');
  });

  it('should leave the main region to the current view when it starts', async () => {
    const page = await render();

    expect(page.querySelector('main router-outlet')).not.toBeNull();
    expect(page.querySelectorAll('h1').length).toBe(0);
  });

  // Until the currencies piece this test expected `/meta` alone. E-26 adds the rates to the
  // start; the list is still the exact one: anything else asked at the start fails it.
  it('should ask at the start for /meta and for the rates, once each, and for nothing else (SPEC-04/E-39, E-26)', async () => {
    await render();

    const requests = TestBed.inject(HttpTestingController).match(() => true);
    expect(requests.map((request) => request.request.urlWithParams)).toEqual([
      `${environment.apiBaseUrl}/meta`,
      environment.ratesUrl,
    ]);
  });

  it('should carry the currency selector in the header, with its label (SPEC-04 2.1)', async () => {
    const page = await render();

    const select = page.querySelector('header select');
    const label = page.querySelector(`header label[for="${select?.id ?? ''}"]`);
    expect(select?.id).toBe('currency-select');
    expect(label?.textContent?.trim()).toBe('Divisa');
  });
});
