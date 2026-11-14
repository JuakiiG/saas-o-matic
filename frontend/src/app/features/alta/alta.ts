import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  computed,
  inject,
  signal,
} from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { map } from 'rxjs';

import { ApiError, FieldError, FormErrors, formErrors } from '../../core/api-error';
import { BackendApi } from '../../core/backend-api';
import { MetaStore } from '../../core/meta-store';
import { Customer, MetaData, NewCustomer } from '../../core/models';
import { Remote } from '../../core/remote';
import { FormNotice } from '../../shared/form-notice';
import { LoadingNotice } from '../../shared/loading-notice';
import { MetaGate } from '../../shared/meta-gate';
import { AltaField, altaHelp, hasHelp } from './alta-help';

const CUSTOMER_ALREADY_EXISTS = 'customer_already_exists';
const NOTICE_ALREADY_EXISTS = 'Ya existe un cliente con ese identificador fiscal en ese país.';
const NO_META: MetaData = { countries: [], plans: [] };

/** Where the template shows the error of each field: the `id` its control points to. */
const ERROR_IDS: Readonly<Record<AltaField, string>> = {
  company_name: 'alta-name-error',
  tax_id: 'alta-tax-id-error',
  contact_email: 'alta-email-error',
  country: 'alta-country-error',
  plan: 'alta-plan-error',
};
const FIELDS = Object.keys(ERROR_IDS) as AltaField[];

/** A sign-up that has been sent: what the form held then and the state of its request. */
interface Submission {
  readonly written: NewCustomer;
  readonly state: Remote<Customer>;
}

/** What the template needs to know about one field. */
interface FieldView {
  readonly error: string;
  readonly invalid: boolean;
  readonly errorId: string | null;
}

/** What the form shows of the error of a sign-up. The code decides, never the text (E-11). */
function shownErrors(error: ApiError | null): FormErrors {
  if (error?.code === CUSTOMER_ALREADY_EXISTS) {
    // Sending the same again cannot help: no «Reintentar».
    return { byField: {}, notice: { messages: [NOTICE_ALREADY_EXISTS], retryable: false } };
  }
  return formErrors(error, FIELDS);
}

/** Sign-up of a customer (SPEC-04, 2.3). The backend decides; the form only helps. */
@Component({
  selector: 'app-alta',
  imports: [ReactiveFormsModule, RouterLink, FormNotice, LoadingNotice, MetaGate],
  templateUrl: './alta.html',
  styleUrl: './alta.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Alta {
  private readonly api = inject(BackendApi);
  private readonly metaStore = inject(MetaStore);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);

  // The controls are named after the fields of the contract, so an error of the backend finds
  // its control by its `field`.
  protected readonly form = new FormGroup({
    company_name: new FormControl('', { nonNullable: true }),
    tax_id: new FormControl('', { nonNullable: true }),
    contact_email: new FormControl('', { nonNullable: true }),
    country: new FormControl('', { nonNullable: true }),
    plan: new FormControl('', { nonNullable: true }),
  });
  private readonly written = toSignal(
    this.form.valueChanges.pipe(map((): NewCustomer => this.form.getRawValue())),
    { initialValue: this.form.getRawValue() },
  );
  private readonly attempted = signal(false);
  private readonly submission = signal<Submission | null>(null);

  private readonly meta = computed(() => {
    const state = this.metaStore.state();
    return state.status === 'data' ? state.data : NO_META;
  });
  private readonly help = computed(() => altaHelp(this.written(), this.meta()));
  private readonly failure = computed(() => {
    const state = this.submission()?.state;
    return state?.status === 'error' ? state.error : null;
  });
  private readonly rejected = computed(() => shownErrors(this.failure()));

  protected readonly countries = computed(() => this.meta().countries);
  protected readonly plans = computed(() => this.meta().plans);
  protected readonly fields = computed(() => this.toFieldViews());
  protected readonly notice = computed(() => this.rejected().notice);
  protected readonly saving = computed(() => this.submission()?.state.status === 'loading');
  /** No second sign-up while one is on its way, nor once it has been created (E-07). */
  protected readonly busy = computed(() => {
    const status = this.submission()?.state.status;
    return status === 'loading' || status === 'data';
  });

  /** «Guardar» and «Reintentar»: sends what the form holds now, if the help lets it through. */
  protected submit(): void {
    if (this.busy()) {
      return;
    }
    this.attempted.set(true);
    const written = this.form.getRawValue();
    if (hasHelp(altaHelp(written, this.meta()))) {
      return;
    }
    this.api
      .createCustomer(written)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((state) => this.follow({ written, state }));
  }

  private follow(submission: Submission): void {
    this.submission.set(submission);
    if (submission.state.status === 'data') {
      // The id is the one of the body: CORS does not expose `Location` (E-46). A navigation
      // that fails is not swallowed: the rejection reaches the error handler of the application.
      void this.router.navigateByUrl(`/clientes/${submission.state.data.id}`);
    }
  }

  private toFieldViews(): Readonly<Record<AltaField, FieldView>> {
    return {
      company_name: this.toFieldView('company_name'),
      tax_id: this.toFieldView('tax_id'),
      contact_email: this.toFieldView('contact_email'),
      country: this.toFieldView('country'),
      plan: this.toFieldView('plan'),
    };
  }

  private toFieldView(field: AltaField): FieldView {
    const error = this.shownHelp(field) ?? this.backendMessage(field) ?? '';
    const invalid = error !== '';
    return { error, invalid, errorId: invalid ? ERROR_IDS[field] : null };
  }

  /** The help stays quiet until the first attempt to send: an empty form is not a mistake. */
  private shownHelp(field: AltaField): string | null {
    return this.attempted() ? this.help()[field] : null;
  }

  /** The message of the backend stands while the field holds what the backend judged. */
  private backendMessage(field: AltaField): string | null {
    const judged = this.submission()?.written[field];
    const fieldError: FieldError | undefined = this.rejected().byField[field];
    return fieldError !== undefined && judged === this.written()[field] ? fieldError.message : null;
  }
}
