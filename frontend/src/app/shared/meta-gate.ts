import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';

import { MetaStore } from '../core/meta-store';
import { ErrorNotice } from './error-notice';
import { LoadingNotice } from './loading-notice';

/**
 * Wraps a view that shows countries or plans (SPEC-04, 2.1): while `/meta` is loading it shows
 * the loading state, if it failed it shows the error with «Reintentar», which asks for `/meta`
 * again, and only with the data does it show the view. No view ever shows a bare code.
 */
@Component({
  selector: 'app-meta-gate',
  imports: [ErrorNotice, LoadingNotice],
  template: `
    @if (error(); as failure) {
      <app-error-notice [error]="failure" (retry)="retry()" />
    } @else if (loading()) {
      <app-loading-notice label="Cargando…" />
    } @else {
      <ng-content />
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MetaGate {
  private readonly meta = inject(MetaStore);

  protected readonly loading = computed(() => this.meta.state().status === 'loading');
  protected readonly error = computed(() => {
    const state = this.meta.state();
    return state.status === 'error' ? state.error : null;
  });

  protected retry(): void {
    this.meta.retry();
  }
}
