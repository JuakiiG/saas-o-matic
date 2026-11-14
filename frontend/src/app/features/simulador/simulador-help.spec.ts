import {
  MAX_ACTIVE_USERS,
  MAX_API_CALLS,
  MAX_STORAGE_GB,
  SLIDER_MAX_USERS,
  parseCount,
} from './simulador-help';

const ARABIC_DIGITS = String.fromCodePoint(0x661) + String.fromCodePoint(0x665);

describe('parseCount · SPEC-04/E-22, E-36, E-49 (2.5)', () => {
  it.each([
    ['0', 0],
    ['10', 10],
    ['015', 15],
    ['000000000000000000000015', 15],
    ['100000', 100000],
  ])('should read «%s», only ASCII digits within the limits, as %d', (text, expected) => {
    expect(parseCount(text, MAX_ACTIVE_USERS)).toBe(expected);
  });

  it.each([
    '',
    ' ',
    '-1',
    '+15',
    '1,5',
    '15.0',
    '2.0',
    '1e3',
    '1 5',
    ' 15',
    '15 ',
    '0x10',
    '100001',
    '100000.000000000001',
    '9'.repeat(400),
    ARABIC_DIGITS,
  ])('should not accept «%s»: the text decides, not the number it would make', (text) => {
    expect(parseCount(text, MAX_ACTIVE_USERS)).toBeNull();
  });

  it('should take the limits of each field from SPEC-02 and SPEC-03', () => {
    expect(MAX_ACTIVE_USERS).toBe(100_000);
    expect(MAX_STORAGE_GB).toBe(1_000_000);
    expect(MAX_API_CALLS).toBe(1_000_000_000);
    expect(SLIDER_MAX_USERS).toBe(500);
  });

  it.each([
    ['1000000', MAX_STORAGE_GB, 1_000_000],
    ['1000001', MAX_STORAGE_GB, null],
    ['1000000000', MAX_API_CALLS, 1_000_000_000],
    ['1000000001', MAX_API_CALLS, null],
  ])('should read «%s» against the limit %d as %s', (text, max, expected) => {
    expect(parseCount(text, max)).toBe(expected);
  });
});
