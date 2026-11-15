import {
  formatDateTime,
  formatInteger,
  formatPercent,
  formatRate,
  formatRateDate,
  tierLabel,
} from './format';

const NO_BREAK_SPACE = String.fromCodePoint(0xa0);

describe('formatRate · SPEC-04 2.6', () => {
  it.each([
    [1.1139, '1,1139'],
    [0.92316, '0,92316'],
    [1.12345678, '1,123457'],
    [1, '1'],
  ])('should show %d with the decimals it brings, up to six', (rate, expected) => {
    expect(formatRate(rate)).toBe(expected);
  });
});

describe('formatPercent · SPEC-04 2.8', () => {
  it.each([
    [2100, `21${NO_BREAK_SPACE}%`],
    [1900, `19${NO_BREAK_SPACE}%`],
    [2150, `21,5${NO_BREAK_SPACE}%`],
    [0, `0${NO_BREAK_SPACE}%`],
  ])('should show %d basis points as a percentage', (basisPoints, expected) => {
    expect(formatPercent(basisPoints)).toBe(expected);
  });
});

describe('tierLabel · SPEC-04 2.8', () => {
  it.each([
    [1, 10, 'del 1 al 10'],
    [11, 50, 'del 11 al 50'],
    [51, null, 'del 51 en adelante'],
  ])('should name the tier from %d to %s by its limits', (fromUsers, toUsers, expected) => {
    expect(tierLabel(fromUsers, toUsers)).toBe(expected);
  });
});

describe('formatDateTime · SPEC-04 2.8', () => {
  const CREATED_AT = '2026-11-12T14:30:00Z';

  it.each([
    [CREATED_AT, 'Europe/Madrid', '12/11/2026, 15:30'],
    [CREATED_AT, 'America/New_York', '12/11/2026, 09:30'],
    [CREATED_AT, 'UTC', '12/11/2026, 14:30'],
    ['2026-11-12T23:30:00Z', 'Europe/Madrid', '13/11/2026, 00:30'],
    ['2026-07-01T08:05:00Z', 'Europe/Madrid', '01/07/2026, 10:05'],
  ])('should show the UTC time %s in the zone %s as «%s»', (createdAt, timeZone, expected) => {
    expect(formatDateTime(createdAt, timeZone)).toBe(expected);
  });

  it('should use the time zone of the browser when none is given', () => {
    const browserZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    expect(formatDateTime(CREATED_AT)).toBe(formatDateTime(CREATED_AT, browserZone));
    expect(formatDateTime(CREATED_AT)).toContain('/11/2026');
  });

  it('should show the text as it arrives when it is not a date', () => {
    expect(formatDateTime('ayer')).toBe('ayer');
  });

  // `Date` reads these three as a date, and the fourth as the 2nd of March: an invented date.
  it.each(['Ejemplo 7', '1', '12/11/2026', '2026-02-30T10:00:00Z'])(
    'should show «%s» as it arrives: it is not a date with the shape of the contract',
    (text) => {
      expect(formatDateTime(text, 'Europe/Madrid')).toBe(text);
    },
  );

  // Real dates, but not written the way the contract writes them (SPEC-01: `…T14:30:00Z`).
  it.each([
    '2026-11-12',
    '2026-11-12 14:30:00',
    '2026-11-12T14:30:00+01:00',
    '2026-11-12T14:30:00.500Z',
    '2026-11-12T24:00:00Z',
  ])('should show «%s» as it arrives: only the shape of the contract is converted', (text) => {
    expect(formatDateTime(text, 'Europe/Madrid')).toBe(text);
  });
});

describe('formatRateDate · SPEC-04 2.6', () => {
  // The date of a rate has no time: it is turned round as a text and never goes through a
  // `Date`, which in a time zone behind UTC would show the day before (5.5).
  it.each([
    ['2026-11-12', '12/11/2026'],
    ['2026-01-01', '01/01/2026'],
    ['2026-12-31', '31/12/2026'],
  ])('should show the date %s as %s, whatever the time zone', (date, expected) => {
    expect(formatRateDate(date)).toBe(expected);
  });

  it('should show the text as it arrives when it has not the shape of a date', () => {
    expect(formatRateDate('hoy')).toBe('hoy');
  });
});

describe('formatInteger · SPEC-04 2.8', () => {
  // The Spanish format groups from five digits on: `1000` has no separator.
  it.each([
    [0, '0'],
    [15, '15'],
    [1000, '1000'],
    [20000, '20.000'],
    [250000, '250.000'],
    [1000000000, '1.000.000.000'],
  ])('should show %d the Spanish way, as «%s»', (value, expected) => {
    expect(formatInteger(value)).toBe(expected);
  });
});
