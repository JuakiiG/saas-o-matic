import { Observable, catchError, map, of, startWith, timeout } from 'rxjs';

import { ApiError, toApiError } from './api-error';

/** The three explicit states of every remote call (SPEC-04, 2.7). */
export type Remote<T> =
  | { readonly status: 'loading' }
  | { readonly status: 'error'; readonly error: ApiError }
  | { readonly status: 'data'; readonly data: T };

/** No call to the backend waits longer than this (SPEC-04/E-33). */
export const BACKEND_TIMEOUT_MS = 10_000;

/**
 * Gives a request its three states: it starts loading and ends in data or in an error.
 *
 * It never fails: an error is a state, with its code, so that a view cannot forget to show it.
 * When the wait runs out the request is cancelled; unsubscribing cancels it too, which is how a
 * newer search or quote replaces the one in flight.
 */
export function toRemote<T>(request: Observable<T>, timeoutMs: number): Observable<Remote<T>> {
  return request.pipe(
    timeout(timeoutMs),
    map((data): Remote<T> => ({ status: 'data', data })),
    catchError((failure: unknown) =>
      of<Remote<T>>({ status: 'error', error: toApiError(failure) }),
    ),
    startWith<Remote<T>>({ status: 'loading' }),
  );
}
