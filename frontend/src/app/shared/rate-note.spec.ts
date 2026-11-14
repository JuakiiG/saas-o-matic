import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DisplayCurrency, DisplayedCurrency } from '../core/display-currency';
import { RateNote } from './rate-note';

function render(currency: DisplayedCurrency): ComponentFixture<RateNote> {
  TestBed.inject(DisplayCurrency).show(currency);
  const fixture = TestBed.createComponent(RateNote);
  fixture.detectChanges();
  return fixture;
}

function textOf(fixture: ComponentFixture<RateNote>, selector: string): string {
  const element = (fixture.nativeElement as HTMLElement).querySelector(selector);
  return (element?.textContent ?? '').replace(/\s+/g, ' ').trim();
}

describe('RateNote · SPEC-04/E-29 (2.6)', () => {
  it('should show nothing while the currency is EUR', () => {
    const fixture = render({ code: 'EUR' });

    expect((fixture.nativeElement as HTMLElement).textContent?.trim()).toBe('');
  });

  it.each<[DisplayedCurrency, string]>([
    [{ code: 'USD', rate: 1.1139, date: '2026-11-12' }, '1 EUR = 1,1139 USD · tipo del 12/11/2026'],
    [
      { code: 'CHF', rate: 0.92316, date: '2026-11-14' },
      '1 EUR = 0,92316 CHF · tipo del 14/11/2026',
    ],
    [
      { code: 'GBP', rate: 0.83583, date: '2026-01-01' },
      '1 EUR = 0,83583 GBP · tipo del 01/01/2026',
    ],
  ])(
    'should show the rate applied and its own date when the currency is %o',
    (currency, expected) => {
      const fixture = render(currency);

      expect(textOf(fixture, '.rate-applied')).toBe(expected);
    },
  );

  it('should say that converted amounts are only a guide', () => {
    const fixture = render({ code: 'USD', rate: 1.1139, date: '2026-11-12' });

    expect(textOf(fixture, '.rate-warning')).toBe(
      'Importes orientativos: cada uno se convierte por separado.',
    );
  });

  it('should follow the currency when it changes', () => {
    const fixture = render({ code: 'USD', rate: 1.1139, date: '2026-11-12' });

    TestBed.inject(DisplayCurrency).show({ code: 'EUR' });
    fixture.detectChanges();

    expect((fixture.nativeElement as HTMLElement).querySelector('.rate-note')).toBeNull();
  });
});
