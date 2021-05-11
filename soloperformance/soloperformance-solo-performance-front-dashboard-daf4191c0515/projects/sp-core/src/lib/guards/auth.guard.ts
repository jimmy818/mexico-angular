import { Inject, Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, RouterStateSnapshot, Router, CanActivate, CanActivateChild } from '@angular/router';

import { SpCoreConfig } from '../sp-core-config.interface';
import { SP_CORE_CONFIG } from '../sp-core.constants';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate, CanActivateChild {
  constructor(
    @Inject(SP_CORE_CONFIG) private config: SpCoreConfig,
    private router: Router,
    private authService: AuthService
  ) { }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    return this.validate(next, state)
  }

  canActivateChild(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    return this.validate(next, state);
  }

  private validate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {

    // Si el usuario está autenticado permite cargar el módulo.
    if (this.authService.isUserAuthenticated()) {
      return true;
    }

    // Si el usuario no está autenticado envía al login.
    this.router.navigate([this.config.loginUrl, btoa(state.url)], { replaceUrl: true });

    return false;
  }
}
