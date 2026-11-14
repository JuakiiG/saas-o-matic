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

import { formErrors } from '../../core/api-error';
import { BackendApi } from '../../core/backend-api';
import { CUSTOMER_NOT_FOUND, CustomerLoader } from '../../core/customer-loader';
import { MetaStore } from '../../core/meta-store';
import { NewSimulation } from '../../core/models';
import { CustomerNotFound } from '../../shared/customer-not-found';
import { ErrorNotice } from '../../shared/error-notice';
import { FormNotice } from '../../shared/form-notice';
import { LoadingNotice } from '../../shared/loading-notice';
import { MetaGate } from '../../shared/meta-gate';
import { Projector } from './projector';
import { QuotePanel } from './quote-panel';
import { MAX_ACTIVE_USERS, SLIDER_MAX_USERS, countsOf, parseCount } from './simulador-help';
import { SIMULADOR_FIELDS, Saving, errorOf, fieldViews, saveNoticeOf } from './simulador-view';

const INITIAL_USERS = 10;

/** The customer as the simulator names it: the company and the name of its country. */
interface CustomerLine {
  readonly name: string;
  readonly country: string;
  readonly detailLink: string;
}

/** Simulator of a customer: a live projection and the way to save it (SPEC-04, 2.5). */
@Component({
  selector: 'app-simulador',
  imports: [
    ReactiveFormsModule,
    RouterLink,
    CustomerNotFound,
    ErrorNotice,
    FormNotice,
    LoadingNotice,
    MetaGate,
    QuotePanel,
  ],
  providers: [CustomerLoader, Projector],
  templateUrl: './simulador.html',
  styleUrl: './simulador.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Simulador {
  private readonly api = inject(BackendApi);
  private readonly loader = inject(CustomerLoader);
  private readonly meta = inject(MetaStore);
  private readonly projector = inject(Projector);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);

  protected readonly sliderMax = SLIDER_MAX_USERS;
  protected readonly usersBox = new FormControl(String(INITIAL_USERS), { nonNullable: true });
  protected readonly slider = new FormControl(INITIAL_USERS, { nonNullable: true });
  protected readonly storageBox = new FormControl('0', { nonNullable: true });
  protected readonly callsBox = new FormControl('0', { nonNullable: true });
  // The group is what turns the submit of the `<form>` into `ngSubmit`.
  protected readonly form = new FormGroup({
    users: this.usersBox,
    slider: this.slider,
    storage: this.storageBox,
    calls: this.callsBox,
  });
  private readonly usersText = toSignal(this.usersBox.valueChanges, {
    initialValue: this.usersBox.value,
  });
  private readonly storageText = toSignal(this.storageBox.valueChanges, {
    initialValue: this.storageBox.value,
  });
  private readonly callsText = toSignal(this.callsBox.valueChanges, {
    initialValue: this.callsBox.value,
  });
  private readonly counts = computed(() =>
    countsOf(this.usersText(), this.storageText(), this.callsText()),
  );

  private readonly saved = signal<Saving | null>(null);
  private readonly loaded = computed(() => {
    const state = this.loader.state();
    return state.status === 'data' ? state.data : null;
  });
  private readonly customerId = computed(() => this.loaded()?.id ?? null);
  private readonly projectionError = computed(() => errorOf(this.projector.projection()?.state));
  private readonly saveError = computed(() => errorOf(this.saved()?.state));
  private readonly errors = computed(() => ({
    projection: formErrors(this.projectionError(), SIMULADOR_FIELDS),
    save: formErrors(this.saveError(), SIMULADOR_FIELDS),
    sent: this.saved()?.sent ?? null,
  }));
  /** True when the amounts on screen are the ones of the users written (E-23). */
  private readonly current = computed(() => {
    const projection = this.projector.projection();
    return projection?.state.status === 'data' && projection.users === this.counts().active_users;
  });

  protected readonly notFound = computed(
    () =>
      this.loader.state().status === 'not-found' ||
      this.projectionError()?.code === CUSTOMER_NOT_FOUND ||
      this.saveError()?.code === CUSTOMER_NOT_FOUND,
  );
  protected readonly loading = computed(() => this.loader.state().status === 'loading');
  protected readonly loadError = computed(() => errorOf(this.loader.state()));
  protected readonly customer = computed(() => this.toCustomerLine());
  protected readonly quote = this.projector.quote;
  protected readonly updating = computed(() => !this.current());
  protected readonly projecting = computed(
    () => this.quote() === null && this.projector.projection()?.state.status === 'loading',
  );
  protected readonly projectionNotice = computed(() => this.errors().projection.notice);
  protected readonly saveNotice = computed(() =>
    saveNoticeOf(this.saveError(), this.errors().save.notice, this.customerId()),
  );
  protected readonly saving = computed(() => this.saved()?.state.status === 'loading');
  protected readonly saveDisabled = computed(() => this.simulationToSave() === null);
  protected readonly fields = computed(() => fieldViews(this.counts(), this.errors()));

  constructor() {
    this.projector.start(this.customerId, this.usersBox);
    this.usersBox.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe((text) => this.moveSlider(text));
    this.slider.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe((users) => this.usersBox.setValue(String(users)));
  }

  protected retryCustomer(): void {
    this.loader.retry();
  }

  protected retryProjection(): void {
    this.projector.retry();
  }

  /** «Guardar», and «Reintentar» after a failed save: saves what the form holds now. */
  protected save(): void {
    const simulation = this.simulationToSave();
    if (simulation === null) {
      return;
    }
    this.api
      .saveSimulation(simulation)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((state) => this.followSave({ sent: simulation, state }));
  }

  private followSave(saving: Saving): void {
    this.saved.set(saving);
    if (saving.state.status === 'data') {
      // A navigation that fails is not swallowed: it reaches the error handler of the application.
      void this.router.navigateByUrl(`/clientes/${saving.sent.customer_id}`);
    }
  }

  /** The slider follows the text box, stopping at its maximum; an invalid text leaves it be. */
  private moveSlider(text: string): void {
    const users = parseCount(text, MAX_ACTIVE_USERS);
    if (users !== null) {
      this.slider.setValue(Math.min(users, SLIDER_MAX_USERS), { emitEvent: false });
    }
  }

  /** What «Guardar» would send, or `null` while it cannot be pressed (E-23). */
  private simulationToSave(): NewSimulation | null {
    const id = this.customerId();
    const counts = this.counts();
    const status = this.saved()?.state.status;
    const busy = status === 'loading' || status === 'data';
    if (id === null || busy || !this.current() || counts.active_users === null) {
      return null;
    }
    if (counts.storage_gb === null || counts.estimated_api_calls === null) {
      return null;
    }
    return {
      customer_id: id,
      active_users: counts.active_users,
      storage_gb: counts.storage_gb,
      estimated_api_calls: counts.estimated_api_calls,
    };
  }

  private toCustomerLine(): CustomerLine | null {
    const customer = this.loaded();
    if (customer === null) {
      return null;
    }
    return {
      name: customer.company_name,
      country: this.meta.countryName(customer.country),
      detailLink: `/clientes/${customer.id}`,
    };
  }
}
