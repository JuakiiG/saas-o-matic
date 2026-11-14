import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';

/**
 * General notice of a form (SPEC-04, 2.3 and 2.7): what went wrong that belongs to no field of
 * it. The form gives the texts, which it chooses by the code of the error, and says whether
 * sending again can help. Whatever is projected (a link, in the simulator) goes after the texts.
 */
@Component({
  selector: 'app-form-notice',
  template: `
    <div class="notice notice-error form-notice" role="alert">
      @for (message of messages(); track $index) {
        <p>{{ message }}</p>
      }
      <ng-content />
      @if (retryable()) {
        <button type="button" (click)="retry.emit()">Reintentar</button>
      }
    </div>
  `,
  styleUrl: './notice.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FormNotice {
  readonly messages = input.required<readonly string[]>();
  readonly retryable = input(false);
  readonly retry = output<void>();
}
