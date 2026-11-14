import { MetaData, NewCustomer } from '../../core/models';
import { codePointLength, hasLoneSurrogate, trimSpaces } from '../../core/text';

// Help of the sign-up form (SPEC-04, 2.3). It rejects only what the backend would reject for
// sure and measures as the backend does: lengths in code points, trimming U+0020 only. The
// rest is for the backend to decide, the check character of the tax id included (E-06).

export type AltaField = keyof NewCustomer;

/** What the help says about each field; `null` when it has nothing to say. */
export type AltaHelp = Readonly<Record<AltaField, string | null>>;

const NAME_MIN_LENGTH = 2;
const NAME_MAX_LENGTH = 120;
const TAX_ID_MAX_LENGTH = 30;
const EMAIL_MAX_LENGTH = 254;
const AT_SIGN = '@';

// A lone surrogate cannot travel in JSON: the backend would answer with an error of the whole
// request, which names no field to correct (E-45).
const MALFORMED_TEXT = 'El texto contiene un carácter que no se puede enviar.';

function nameHelp(written: string): string | null {
  if (hasLoneSurrogate(written)) {
    return MALFORMED_TEXT;
  }
  const length = codePointLength(trimSpaces(written));
  return length < NAME_MIN_LENGTH || length > NAME_MAX_LENGTH
    ? 'El nombre debe tener entre 2 y 120 caracteres.'
    : null;
}

function taxIdHelp(written: string): string | null {
  if (hasLoneSurrogate(written)) {
    return MALFORMED_TEXT;
  }
  if (written === '') {
    return 'Escribe el identificador fiscal.';
  }
  // Measured untrimmed, as the backend does before it normalizes the identifier.
  return codePointLength(written) > TAX_ID_MAX_LENGTH
    ? 'El identificador fiscal admite 30 caracteres como máximo.'
    : null;
}

function emailHelp(written: string): string | null {
  if (hasLoneSurrogate(written)) {
    return MALFORMED_TEXT;
  }
  const email = trimSpaces(written);
  if (email === '') {
    return 'Escribe el email de contacto.';
  }
  if (codePointLength(email) > EMAIL_MAX_LENGTH) {
    return 'El email admite 254 caracteres como máximo.';
  }
  // This much of the rule of the backend and no more: the whole of it here would be a second
  // implementation, and the validators of the framework reject what the backend stores (E-44).
  const hasInnerAtSign =
    email.includes(AT_SIGN) && !email.startsWith(AT_SIGN) && !email.endsWith(AT_SIGN);
  return hasInnerAtSign ? null : 'El email debe llevar una @ que no esté al principio ni al final.';
}

function choiceHelp(
  code: string,
  offered: readonly { readonly code: string }[],
  message: string,
): string | null {
  return offered.some((option) => option.code === code) ? null : message;
}

/** The help for what the form holds, with the countries and plans that `/meta` offers. */
export function altaHelp(written: NewCustomer, meta: MetaData): AltaHelp {
  return {
    company_name: nameHelp(written.company_name),
    tax_id: taxIdHelp(written.tax_id),
    contact_email: emailHelp(written.contact_email),
    country: choiceHelp(written.country, meta.countries, 'Elige un país.'),
    plan: choiceHelp(written.plan, meta.plans, 'Elige un plan.'),
  };
}

/** True when the help has something to say about any field, so the form is not sent. */
export function hasHelp(help: AltaHelp): boolean {
  return Object.values(help).some((message) => message !== null);
}
