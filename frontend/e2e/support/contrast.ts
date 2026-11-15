// The contrast ratio of WCAG 2.2 between two colours, as the browser reports them in a computed
// style (`rgb(29, 78, 216)`). Only opaque colours: a translucent one has no contrast of its own.

const OPAQUE_RGB = /^rgb\((\d+), (\d+), (\d+)\)$/;

function channels(colour: string): number[] {
  const match = OPAQUE_RGB.exec(colour);
  if (match === null) {
    throw new Error(`Not an opaque rgb() colour: «${colour}»`);
  }
  return match.slice(1).map(Number);
}

function linear(channel: number): number {
  const value = channel / 255;
  return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
}

function luminance(colour: string): number {
  const [red, green, blue] = channels(colour).map(linear);
  return 0.2126 * red + 0.7152 * green + 0.0722 * blue;
}

/** From 1 (the same colour) to 21 (black on white). */
export function contrastRatio(one: string, other: string): number {
  const [darker, lighter] = [luminance(one), luminance(other)].sort((a, b) => a - b);
  return (lighter + 0.05) / (darker + 0.05);
}
