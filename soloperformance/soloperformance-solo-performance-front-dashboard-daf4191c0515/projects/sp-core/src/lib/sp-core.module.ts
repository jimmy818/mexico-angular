import { ModuleWithProviders, NgModule } from '@angular/core';
import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { SP_CORE_CONFIG } from './sp-core.constants';
import { SpCoreConfig } from './sp-core-config.interface';
import { AuthService } from './services/auth.service';
import { LocalStorageService } from './services/local-storage.service';
import { TokenInterceptor } from './interceptors/token.interceptor';
import { ProgressSpinnerService } from './services/progress-spinner.service';
import { UserService } from './services/user.service';
import { TeamService } from './services/team.service';

@NgModule({
  declarations: [],
  imports: [],
  exports: []
})
export class SpCoreModule {
  static forRoot(config?: SpCoreConfig): ModuleWithProviders<SpCoreModule> {

    return {
      ngModule: SpCoreModule,
      providers: [
        AuthService,
        ProgressSpinnerService,
        LocalStorageService,
        UserService,
        TeamService,
        {
          provide: HTTP_INTERCEPTORS,
          useClass: TokenInterceptor,
          multi: true
        },
        {
          provide: SP_CORE_CONFIG,
          useValue: config ||
            // Configuraciones por defecto
            <SpCoreConfig>{
              apiBaseUrl: '',
              tokenUrl: 'token/',
              refreshTokenUrl: 'token-refresh/',
              userInfoUrl: 'me',
              forgotPasswordUrl: 'reset-password/',
              loginUrl: 'auth/login'
            }
        }
      ]
    }
  }
}
