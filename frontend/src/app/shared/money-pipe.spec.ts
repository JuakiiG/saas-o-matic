import { TestBed } from '@angular/core/testing';

import { DisplayCurrency, ForeignCurrencyCode } from '../core/display-currency';
import { MoneyPipe } from './money-pipe';

const NO_BREAK_SPACE = String.fromCodePoint(0xa0);
// Rates of the example of SPEC-04, 4.2.
const RATES: Record<ForeignCurrencyCode, number> = { USD: 1.1139, GBP: 0.83583, CHF: 0.92316 };
const RATE_DATE = '2026-11-12';

// One row per row of the table of amounts of SPEC-04, 5.1: cents, EUR, USD, GBP, CHF.
const AMOUNTS: [number, string, string, string, string][] = [
  [0, '0,00', '0,00', '0,00', '0,00'],
  [1, '0,01', '0,01', '0,01', '0,01'],
  [5, '0,05', '0,06', '0,04', '0,05'],
  [1000, '10,00', '11,14', '8,36', '9,23'],
  [14000, '140,00', '155,95', '117,02', '129,24'],
  [2940, '29,40', '32,75', '24,57', '27,14'],
  [16940, '169,40', '188,69', '141,59', '156,38'],
  [123450, '1234,50', '1375,11', '1031,83', '1139,64'],
  [60520570, '605.205,70', '674.138,63', '505.849,08', '558.701,69'],
];

// CA-01: every cell of the table of amounts of 5.1, through the only pipe that formats money.
describe('MoneyPipe · SPEC-04/E-28, E-29 (CA-01)', () => {
  function pipeShowing(code: 'EUR' | ForeignCurrencyCode): MoneyPipe {
    const displayCurrency = TestBed.inject(DisplayCurrency);
    if (code !== 'EUR') {
      displayCurrency.show({ code, rate: RATES[code], date: RATE_DATE });
    }
    return TestBed.runInInjectionContext(() => new MoneyPipe());
  }

  it.each(AMOUNTS)('should show %d cents exactly when the currency is EUR', (cents, euro) => {
    expect(pipeShowing('EUR').transform(cents)).toBe(`${euro}${NO_BREAK_SPACE}EUR`);
  });

  it.each(AMOUNTS)('should convert %d cents when the currency is USD', (cents, _euro, dollar) => {
    expect(pipeShowing('USD').transform(cents)).toBe(`${dollar}${NO_BREAK_SPACE}USD`);
  });

  it.each(AMOUNTS)('should convert %d cents when the currency is GBP', (cents, _e, _d, pound) => {
    expect(pipeShowing('GBP').transform(cents)).toBe(`${pound}${NO_BREAK_SPACE}GBP`);
  });

  it.each(AMOUNTS)(
    'should convert %d cents when the currency is CHF',
    (cents, _e, _d, _p, franc) => {
      expect(pipeShowing('CHF').transform(cents)).toBe(`${franc}${NO_BREAK_SPACE}CHF`);
    },
  );

  it('should go back to exact euros when EUR is chosen again', () => {
    const pipe = pipeShowing('USD');

    TestBed.inject(DisplayCurrency).show({ code: 'EUR' });

    expect(pipe.transform(16940)).toBe(`169,40${NO_BREAK_SPACE}EUR`);
  });

  it('should show exact euros, whatever the currency chosen, when euros are asked for (E-29)', () => {
    const pipe = pipeShowing('USD');

    expect(pipe.transform(16940, 'EUR')).toBe(`169,40${NO_BREAK_SPACE}EUR`);
    expect(pipe.transform(16940)).toBe(`188,69${NO_BREAK_SPACE}USD`);
  });

  it('should differ by one cent from the sum of its parts when converted (5.1)', () => {
    const pipe = pipeShowing('USD');

    expect(pipe.transform(14000)).toBe(`155,95${NO_BREAK_SPACE}USD`);
    expect(pipe.transform(2940)).toBe(`32,75${NO_BREAK_SPACE}USD`);
    expect(pipe.transform(16940)).toBe(`188,69${NO_BREAK_SPACE}USD`);
  });
});
