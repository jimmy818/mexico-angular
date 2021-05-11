import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { SpCoreConfig, SpCoreModule } from 'sp-core';
import { SpProgressSpinnerModule } from 'sp-library';

import { environment } from '@web/env/environment';
import { CoreModule } from '@web/core/core.module';
import { SharedModule } from '@web/shared/shared.module';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthLayoutComponent } from './layouts/auth-layout/auth-layout.component';
import { MainLayoutComponent } from './layouts/main-layout/main-layout.component';

const spCoreConfig = <SpCoreConfig>{
  apiBaseUrl: environment.apiBaseUrl,
  tokenUrl: environment.tokenUrl,
  refreshTokenUrl: environment.refreshTokenUrl,
  userInfoUrl: environment.userInfoUrl,
  forgotPasswordUrl: environment.forgotPasswordUrl,
  loginUrl: environment.loginUrl
}

@NgModule({
  declarations: [
    AppComponent,
    AuthLayoutComponent,
    MainLayoutComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    SpCoreModule.forRoot(spCoreConfig),
    SpProgressSpinnerModule,
    CoreModule,
    SharedModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
