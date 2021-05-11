import { ModuleWithProviders, NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { A11yModule } from '@angular/cdk/a11y';

import { GenderPipe, SubscriptionTypePipe } from './pipes';
import { ProgressSpinnerComponent } from './components/progress-spinner/progress-spinner.component';
import { HeaderComponent } from './components/header/header.component';
import { HeaderGroupComponent } from './components/header/header-group/header-group.component';
import { HeaderIconComponent } from './components/header/header-icon/header-icon.component';
import { CardComponent } from './components/card/card.component';
import { GenderSelectComponent } from './components/gender-select/gender-select.component';
import { LoginComponent } from './components/login/login.component';
import { ForgotPasswordComponent } from './components/forgot-password/forgot-password.component';
import { InputSearchComponent } from './components/input-search/input-search.component';
import { ViewContainerDirective } from './directives/view-container.directive';
import { ChartLineComponent } from './components/chart-line/chart-line.component';

const components = [
  ProgressSpinnerComponent,
  LoginComponent,
  ForgotPasswordComponent,
  HeaderComponent,
  HeaderIconComponent,
  HeaderGroupComponent,
  CardComponent,
  GenderSelectComponent,
  InputSearchComponent,
  ChartLineComponent
];

const pipes = [
  GenderPipe,
  SubscriptionTypePipe
];

const directives = [
  ViewContainerDirective
];

@NgModule({
  declarations: [
    components,
    pipes,
    directives
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    MatDialogModule,
    MatIconModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    A11yModule
  ],
  exports: [
    components,
    pipes,
    directives
  ]
})
export class SpLibraryModule { }
