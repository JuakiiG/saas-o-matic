import { ChangeDetectionStrategy, Component, computed, input, output } from '@angular/core';

import { ApiError, noticeFor } from '../core/api-error';

/**
 * Error state of a remote call (SPEC-04, 2.7): the notice that corresponds to its code and a
 * way out, «Reintentar». The text is chosen here by the code; the one of the backend is not shown.
 */
@Component({
  selector: 'app-error-notice',
  template: `
    <div class="notice notice-error" role="alert">
      <p>{{ message() }}</p>
      <button type="button" (click)="retry.emit()">Reintentar</button>
    </div>
  `,
  styleUrl: './notice.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ErrorNotice {
  readonly error = input.required<ApiError>();
  readonly retry = output<void>();

  protected readonly message = computed(() => noticeFor(this.error()));
}
