import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { LoginResult } from 'sp-core';

@Component({
  selector: 'admin-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(
    private router: Router
  ) { }

  ngOnInit(): void {
  }


  initLogin(result: LoginResult): void {
    // Verifica si antes de inicializar el control de login ya se tiene usuario autenticado.
    if (result.isAuthenticated) {
      this.redirectToAdminPanel();
    }
  }

  afterLogin(result: LoginResult): void {
    // Verifica si se intentó acceder desde otra ruta y no desde el login, entonces una vez autenticado se redirecciona a dicha página.
    if (result.redirectUrl != null && result.redirectUrl.length > 0) {
      this.router.navigate([result.redirectUrl], { replaceUrl: true });
    }
    else {
      this.redirectToAdminPanel();
    }
  }

  forgotPassword(): void {
    this.router.navigate(['/auth/reset-password'], { replaceUrl: true });
  }

  private redirectToAdminPanel(): void {
    this.router.navigate(['/dashboard'], { replaceUrl: true });
  }
}
