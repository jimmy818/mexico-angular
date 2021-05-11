import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { throwError } from 'rxjs';
import { catchError, finalize, mergeMap } from 'rxjs/operators';

import { AuthService, UserInfo, LoginResult } from 'sp-core';

import { CONTROL_NAMES } from './login.constants';

@Component({
  selector: 'sp-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  @Output() afterLogin = new EventEmitter<LoginResult>();

  @Output() init = new EventEmitter<LoginResult>();

  @Output() forgotPassword = new EventEmitter<null>();

  @Output() error = new EventEmitter<LoginResult>();

  loggingIn = false;

  logo = 'assets/images/solo-performance.svg';

  loginForm: FormGroup;

  controlNames = CONTROL_NAMES;

  messageError = '';

  private redirectUrl = '';

  private loginResult: LoginResult;

  constructor(
    private fb: FormBuilder,
    private activatedRoute: ActivatedRoute,
    private authService: AuthService
  ) {

    // Crea formulario
    this.createForm();
  }

  ngOnInit(): void {

    // Verifica si existe sesión activa.
    this.loginResult = new LoginResult();
    if (this.authService.isUserAuthenticated()) {
      this.loginResult.isAuthenticated = true;
      this.loginResult.username = this.authService.userAuthenticated;
      // Evento al inicializar el login. Se envía nombre de usuario en sesión.
      this.init.emit(this.loginResult);
    } else {
      // Evento antes de cargar el componente de login.
      this.init.emit(this.loginResult);
      // Obtiene si se envió una ruta para redireccionamiento.
      this.activatedRoute.params.subscribe(params => {
        if (params["redirect"] != undefined) {
          this.redirectUrl = atob(params["redirect"]);
        }
      });
    }
  }

  login() {

    this.loggingIn = true;

    this.loginResult = new LoginResult();

    const username = this.loginForm.get(this.controlNames.username).value;
    const password = this.loginForm.get(this.controlNames.password).value;

    this.authService
      .login(username, password)
      .pipe(
        catchError(error => {
          this.messageError = 'The username or password is incorrect';
          this.loginResult.messageError = this.messageError;
          return throwError(`${error.statusText}: ${error.error.exception}`);
        }),
        mergeMap(() => {
          return this.authService
            .getUserInfo()
            .pipe(
              catchError(error => {
                this.messageError = 'Failed to get user data';
                this.loginResult.messageError = this.messageError;
                return throwError(`${error.statusText}: ${error.error.exception}`);
              }));
        }),
        finalize(() => {
          this.loggingIn = false;
        })
      )
      .subscribe((userInfo: UserInfo) => {
        this.messageError = null;
        this.loginResult.isAuthenticated = true;
        this.loginResult.username = this.authService.userAuthenticated;
        this.loginResult.userInfo = userInfo;
        // Verifica si se intentó acceder desde otra ruta y no desde el login para posteriormente permitir una redirección a dicha ruta.
        if (this.redirectUrl != null && this.redirectUrl.length > 0) {
          this.loginResult.redirectUrl = this.redirectUrl;
        }
        // Evento después de iniciar sesión.
        this.afterLogin.emit(this.loginResult);
      }, (error) => {
        this.loginResult.exceptionError = error;
        this.error.emit(this.loginResult);
      });
  }

  forgotPasswordClick(): void {
    this.forgotPassword.emit();
  }

  private createForm() {

    this.loginForm = this.fb.group({});

    const usernameControl = this.fb.control(null, [Validators.required, Validators.email]);
    const passwordControl = this.fb.control(null, [Validators.required, Validators.minLength(8)]);

    this.loginForm.addControl(this.controlNames.username, usernameControl);
    this.loginForm.addControl(this.controlNames.password, passwordControl);
  }
}
