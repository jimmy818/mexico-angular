import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SpLibraryModule } from 'sp-library';

import { AuthRoutingModule } from './auth-routing.module';
import { LoginComponent } from './login/login.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';

const components = [
  LoginComponent,
  ForgotPasswordComponent
];

@NgModule({
  declarations: [
    components
  ],
  imports: [
    CommonModule,
    AuthRoutingModule,
    SpLibraryModule
  ]
})
export class AuthModule { }
