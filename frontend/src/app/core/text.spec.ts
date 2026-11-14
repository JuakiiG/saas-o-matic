import { codePointLength, hasLoneSurrogate, replaceLoneSurrogates, trimSpaces } from './text';

// Invisible or unusual characters are built from their code, never typed.
const SPACE = String.fromCodePoint(0x20);
const TAB = String.fromCodePoint(0x09);
const NO_BREAK_SPACE = String.fromCodePoint(0xa0);
const DOUBLE_STRUCK_A = String.fromCodePoint(0x1d538);
const GRINNING_FACE = String.fromCodePoint(0x1f600);
const HIGH_SURROGATE = String.fromCharCode(0xd800);
const LOW_SURROGATE = String.fromCharCode(0xdc00);
const REPLACEMENT = String.fromCodePoint(0xfffd);

describe('codePointLength · SPEC-04/E-41, E-50', () => {
  it.each([
    ['an empty text', '', 0],
    ['plain letters', 'abc', 3],
    ['121 letters with a tilde (5.4)', 'ñ'.repeat(121), 121],
    ['61 characters outside the basic plane (5.4)', DOUBLE_STRUCK_A.repeat(61), 61],
    ['100 emoji, 200 UTF-16 units (5.3)', GRINNING_FACE.repeat(100), 100],
    ['100 letters and a space (5.3)', 'x'.repeat(100) + SPACE, 101],
  ])('should count code points when the text is %s', (_case, text, expected) => {
    expect(codePointLength(text)).toBe(expected);
  });
});

describe('trimSpaces · SPEC-04/E-41, E-46', () => {
  it.each([
    ['spaces at both ends (5.4)', SPACE + SPACE + 'Ejemplo Uno SL' + SPACE, 'Ejemplo Uno SL'],
    ['a single letter between spaces (5.4)', SPACE + 'A' + SPACE, 'A'],
    ['only spaces', SPACE.repeat(3), ''],
    ['spaces inside', 'Ejemplo' + SPACE + SPACE + 'Uno', 'Ejemplo' + SPACE + SPACE + 'Uno'],
    ['a leading tab (5.4)', TAB + 'AB', TAB + 'AB'],
    ['a trailing no-break space (5.4)', 'AB' + NO_BREAK_SPACE, 'AB' + NO_BREAK_SPACE],
    ['a space after a no-break space', 'AB' + NO_BREAK_SPACE + SPACE, 'AB' + NO_BREAK_SPACE],
  ])('should remove only U+0020 from the ends when the text has %s', (_case, text, expected) => {
    expect(trimSpaces(text)).toBe(expected);
  });
});

describe('hasLoneSurrogate · SPEC-04/E-45', () => {
  it.each([
    ['an empty text', '', false],
    ['plain letters', 'AB', false],
    ['a well-formed pair, an emoji', 'a' + GRINNING_FACE + 'b', false],
    ['a high surrogate alone (5.4)', 'AB' + HIGH_SURROGATE, true],
    ['a low surrogate alone', LOW_SURROGATE + 'AB', true],
    ['the two halves in the wrong order', LOW_SURROGATE + HIGH_SURROGATE, true],
    ['a pair followed by a lone half', GRINNING_FACE + HIGH_SURROGATE, true],
  ])('should tell whether the text is ill-formed when it has %s', (_case, text, expected) => {
    expect(hasLoneSurrogate(text)).toBe(expected);
  });
});

describe('replaceLoneSurrogates · SPEC-04 2.2', () => {
  it.each([
    ['a lone half between letters (5.3)', 'a' + HIGH_SURROGATE + 'b', 'a' + REPLACEMENT + 'b'],
    ['two lone halves', LOW_SURROGATE + HIGH_SURROGATE, REPLACEMENT + REPLACEMENT],
    ['a well-formed pair', 'a' + GRINNING_FACE + 'b', 'a' + GRINNING_FACE + 'b'],
    ['nothing to replace', '100% a+b&c#d', '100% a+b&c#d'],
  ])(
    'should put U+FFFD in place of each lone half when the text has %s',
    (_case, text, expected) => {
      expect(replaceLoneSurrogates(text)).toBe(expected);
    },
  );
});
