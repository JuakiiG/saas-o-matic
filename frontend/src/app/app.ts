import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

import { CurrencySelector } from './shared/currency-selector';

/** Frame shared by every view: the header and the region where the current view is drawn. */
@Component({
  selector: 'app-root',
  imports: [RouterLink, RouterOutlet, CurrencySelector],
  templateUrl: './app.html',
  styleUrl: './app.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App {}
