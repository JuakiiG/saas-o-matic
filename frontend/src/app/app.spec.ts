import { TestBed } from '@angular/core/testing';

import { App } from './app';
import { appConfig } from './app.config';

// SPEC-04, 2.1: a header shared by every view carries the application name and the link to the
// panel. The currency selector joins it with the currencies piece.
describe('App · SPEC-04 2.1', () => {
  async function render(): Promise<HTMLElement> {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: appConfig.providers,
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
});
