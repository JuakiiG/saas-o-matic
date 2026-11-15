import { contrastRatio } from './support/contrast';
import { expect, test } from './support/fixtures';

// SPEC-04/CA-19 (2.8): the focus ring and the border of the form fields have a contrast of 3:1
// or more against white and against the background of the page. The colours are the ones the
// browser paints, read from its computed styles, not the ones the style sheets write.

const MINIMUM = 3;
const WHITE = 'rgb(255, 255, 255)';
const FIELDS = [
  { view: '/clientes/nuevo', label: 'Nombre de la empresa' },
  { view: '/clientes/nuevo', label: 'País' },
  { view: '/', label: 'Buscar cliente' },
  { view: '/', label: 'Divisa' },
] as const;

for (const { view, label } of FIELDS) {
  test(`should paint the focus ring and the border of «${label}» with a contrast of 3:1 or more (SPEC-04/CA-19)`, async ({
    page,
  }) => {
    await page.goto(view);
    const field = page.getByLabel(label, { exact: true });
    await expect(field).toBeEnabled();
    await field.focus();

    const painted = await field.evaluate((element) => {
      const style = getComputedStyle(element);
      return {
        focusVisible: element.matches(':focus-visible'),
        ring: { style: style.outlineStyle, width: style.outlineWidth, colour: style.outlineColor },
        border: {
          style: style.borderTopStyle,
          width: style.borderTopWidth,
          colour: style.borderTopColor,
        },
        field: style.backgroundColor,
        page: getComputedStyle(document.body).backgroundColor,
      };
    });

    expect(painted.focusVisible, 'the field shows its focus').toBe(true);
    expect(painted.ring).toMatchObject({ style: 'solid', width: '3px' });
    expect(painted.border).toMatchObject({ style: 'solid', width: '1px' });
    expect(painted.field, 'background of the field').toBe(WHITE);
    expect(painted.page, 'background of the page').not.toBe(WHITE);
    for (const background of [painted.field, painted.page]) {
      expect(
        contrastRatio(painted.ring.colour, background),
        `focus ring ${painted.ring.colour} on ${background}`,
      ).toBeGreaterThanOrEqual(MINIMUM);
      expect(
        contrastRatio(painted.border.colour, background),
        `border ${painted.border.colour} on ${background}`,
      ).toBeGreaterThanOrEqual(MINIMUM);
    }
  });
}
