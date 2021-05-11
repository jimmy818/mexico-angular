import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { throwError } from 'rxjs';
import { catchError, finalize } from 'rxjs/operators';

import { AuthService } from 'sp-core';
import { CONTROL_NAMES } from './forgot-password.constants';

@Component({
  selector: 'sp-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent implements OnInit {

  @Output() emailSent = new EventEmitter<null>();

  @Output() goToLogin = new EventEmitter<null>();

  @Output() error = new EventEmitter<string>();

  controlNames = CONTROL_NAMES;

  form: FormGroup;

  message: string;

  messageError: string;

  proccessing = false;

  logo = 'assets/images/solo-performance.svg';

  constructor(
    private fb: FormBuilder,
    private authService: AuthService
  ) {
    this.createForm();
  }

  ngOnInit(): void {
  }

  resetPassword(): void {

    this.proccessing = true;

    this.authService
      .forgotPassword(this.form.get(this.controlNames.email).value)
      .pipe(
        catchError(error => {
          this.message = null;
          this.messageError = 'Email not found or user is not active';
          return throwError(`${error.statusText}: ${error.error.exception}`);
        }),
        finalize(() => {
          this.proccessing = false;
        })
      )
      .subscribe(data => {
        this.messageError = null;
        this.message = 'Email sent. Please check it for instructions';
        this.emailSent.next();
      }, (error) => {
        this.error.emit(error);
      });
  }

  goToLoginClick(): void {
    this.goToLogin.emit();
  }

  private createForm() {

    this.form = this.fb.group({});

    const usernameControl = this.fb.control(null, [Validators.required, Validators.email]);

    this.form.addControl(this.controlNames.email, usernameControl);
  }
}
