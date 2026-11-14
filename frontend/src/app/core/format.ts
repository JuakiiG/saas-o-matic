// Formats of the interface (SPEC-04, 2.6 and 2.8). Everything is shown the Spanish way.

const LOCALE = 'es-ES';
const CENTS_PER_UNIT = 100;
const BASIS_POINTS_PER_UNIT = 10000;

const EURO = currencyFormat('EUR');
const RATE = new Intl.NumberFormat(LOCALE, { maximumFractionDigits: 6 });
const PERCENT = new Intl.NumberFormat(LOCALE, { style: 'percent', maximumFractionDigits: 2 });
const INTEGER = new Intl.NumberFormat(LOCALE, { maximumFractionDigits: 0 });
const RATE_DATE = /^([0-9]{4})-([0-9]{2})-([0-9]{2})$/;
const DATE_TIME_PARTS: Intl.DateTimeFormatOptions = {
  day: '2-digit',
  month: '2-digit',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
};

function currencyFormat(currency: string): Intl.NumberFormat {
  return new Intl.NumberFormat(LOCALE, { style: 'currency', currency, currencyDisplay: 'code' });
}

/**
 * An amount in euro cents, as the backend sends it, shown exactly (`16940` is `169,40 EUR`).
 *
 * Integers only: the euros are an exact division and the cents are the remainder, written over
 * the fraction that `Intl` produces. The amount is never divided by 100, which would be floating
 * point on money (ADR-002). Amounts from the backend are never negative.
 */
export function formatEuroCents(cents: number): string {
  const remainder = cents % CENTS_PER_UNIT;
  const euros = (cents - remainder) / CENTS_PER_UNIT;
  const fraction = String(remainder).padStart(2, '0');
  return EURO.formatToParts(euros)
    .map((part) => (part.type === 'fraction' ? fraction : part.value))
    .join('');
}

/**
 * An amount in euro cents converted to another currency, only to be shown.
 *
 * This is the one place where money goes through floating point (ADR-002): the result is
 * rounded when formatted and is never stored nor sent to the backend.
 */
export function formatConverted(cents: number, currency: string, rate: number): string {
  return currencyFormat(currency).format((cents * rate) / CENTS_PER_UNIT);
}

/** An exchange rate with the decimals it brings, up to six (`1,1139`, `0,92316`). */
export function formatRate(rate: number): string {
  return RATE.format(rate);
}

/**
 * The date of an exchange rate (`2026-11-12`) as day/month/year (`12/11/2026`). It has no time,
 * so it is turned round as a text and never goes through a `Date`: in a time zone behind UTC
 * that would show the day before (SPEC-04, 2.6). A text without that shape is shown as it is.
 */
export function formatRateDate(date: string): string {
  const parts = RATE_DATE.exec(date);
  return parts === null ? date : `${parts[3]}/${parts[2]}/${parts[1]}`;
}

/** A tax rate in basis points as a percentage (`2100` is `21 %`). A rate is not money. */
export function formatPercent(basisPoints: number): string {
  return PERCENT.format(basisPoints / BASIS_POINTS_PER_UNIT);
}

/**
 * A date with time of the backend (`created_at`, in UTC) shown in the time zone of the browser
 * (`12/11/2026, 15:30`). The zone is a parameter only so that a test does not depend on the
 * machine it runs on. A text that is not a date is shown as it arrives: it is not hidden.
 */
export function formatDateTime(createdAt: string, timeZone?: string): string {
  const moment = new Date(createdAt);
  if (Number.isNaN(moment.getTime())) {
    return createdAt;
  }
  return new Intl.DateTimeFormat(LOCALE, { ...DATE_TIME_PARTS, timeZone }).format(moment);
}

/** A count (users, gigabytes, calls) the Spanish way: `250.000`. */
export function formatInteger(value: number): string {
  return INTEGER.format(value);
}

/** Name of a pricing tier by its limits; the last one has no upper limit. */
export function tierLabel(fromUsers: number, toUsers: number | null): string {
  return toUsers === null ? `del ${fromUsers} en adelante` : `del ${fromUsers} al ${toUsers}`;
}
