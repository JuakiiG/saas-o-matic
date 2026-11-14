import { isRouteCustomerId } from './customer-id';

const ARABIC_INDIC_DIGIT_ONE = String.fromCodePoint(0x661);

// The texts of the table of SPEC-04, 5.7: what the route carries after `/clientes/`.
describe('isRouteCustomerId · SPEC-04/E-47, E-15', () => {
  it.each([['1'], ['7'], ['999'], ['1234567890123456'], ['9007199254740991']])(
    'should accept %s, which the backend is asked about',
    (text) => {
      expect(isRouteCustomerId(text)).toBe(true);
    },
  );

  it.each([
    ['letters', 'abc'],
    ['a leading zero', '01'],
    ['a plus sign', '+1'],
    ['a decimal point', '1.0'],
    ['an exponent', '1e0'],
    ['an underscore', '1_0'],
    ['a trailing space', '1 '],
    ['a leading space', ' 1'],
    ['zero alone', '0'],
    ['a negative number', '-1'],
    ['a digit that is not ASCII', ARABIC_INDIC_DIGIT_ONE],
    ['16 digits just above 2^53 − 1', '9007199254740992'],
    ['16 digits above 2^53 − 1 (L-06)', '9007199254740993'],
    ['the largest 16 digits', '9999999999999999'],
    ['17 digits', '99999999999999999'],
    ['an empty text', ''],
  ])('should reject a text with %s, without calling the API', (_case, text) => {
    expect(isRouteCustomerId(text)).toBe(false);
  });
});
