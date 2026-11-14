import { formatPercent, formatRate, tierLabel } from './format';

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
