import { ChangeDetectionStrategy, Component, input } from '@angular/core';

/** Loading state of a remote call (SPEC-04, 2.7): announced to assistive technology as a status. */
@Component({
  selector: 'app-loading-notice',
  template: `<p class="notice notice-loading" role="status">{{ label() }}</p>`,
  styleUrl: './notice.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoadingNotice {
  readonly label = input.required<string>();
}
