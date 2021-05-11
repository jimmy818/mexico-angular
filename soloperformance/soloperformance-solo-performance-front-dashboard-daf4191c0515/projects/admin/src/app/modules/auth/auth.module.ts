import { NgModule } from '@angular/core';

import { SpLibraryModule } from 'sp-library';
import { SharedModule } from '@admin/shared/shared.module';

import { AuthRoutingModule } from './auth-routing.module';
import { LoginComponent } from './login/login.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';

@NgModule({
  declarations: [
    LoginComponent,
    ForgotPasswordComponent
  ],
  imports: [
    AuthRoutingModule,
    SpLibraryModule,
    SharedModule
  ]
})
export class AuthModule { }
