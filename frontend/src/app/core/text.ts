// Text measures shared by the search box and the forms. They measure exactly as the backend does
// (SPEC-01, 2.12), so that the browser never rejects a text the backend would accept.

const SPACE = ' ';
// Unicode mode: the two halves of a well-formed pair (an emoji) are one code point and do not
// match. `isWellFormed()` is ES2024 and the CLI compiles for ES2022 (SPEC-04, 2.3).
const LONE_SURROGATE = /\p{Surrogate}/u;
const EVERY_LONE_SURROGATE = /\p{Surrogate}/gu;
const REPLACEMENT_CHARACTER = String.fromCodePoint(0xfffd);

/** Length in code points, not in UTF-16 units: an emoji counts as one character. */
export function codePointLength(text: string): number {
  return [...text].length;
}

/** Removes U+0020 from both ends and nothing else: `trim()` would also remove tabs and line breaks. */
export function trimSpaces(text: string): string {
  let start = 0;
  let end = text.length;
  while (start < end && text[start] === SPACE) {
    start += 1;
  }
  while (end > start && text[end - 1] === SPACE) {
    end -= 1;
  }
  return text.slice(start, end);
}

/** True when the text holds half of a surrogate pair on its own, which JSON and URLs cannot carry. */
export function hasLoneSurrogate(text: string): boolean {
  return LONE_SURROGATE.test(text);
}

/** The same text with U+FFFD in place of each lone half, so that it can travel in a URL. */
export function replaceLoneSurrogates(text: string): string {
  return text.replace(EVERY_LONE_SURROGATE, REPLACEMENT_CHARACTER);
}
