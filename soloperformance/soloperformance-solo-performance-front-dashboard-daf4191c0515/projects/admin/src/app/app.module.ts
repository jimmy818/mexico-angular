import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { SpCoreConfig, SpCoreModule } from 'sp-core';
import { SpLibraryModule } from 'sp-library';

import { environment } from '@admin/env/environment';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CoreModule } from './core/core.module';
import { SharedModule } from './shared/shared.module';
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
    BrowserAnimationsModule,
    HttpClientModule,
    SpCoreModule.forRoot(spCoreConfig),
    SpLibraryModule,
    AppRoutingModule,
    CoreModule,
    SharedModule
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }