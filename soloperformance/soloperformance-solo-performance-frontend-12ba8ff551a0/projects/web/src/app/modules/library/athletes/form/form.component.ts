import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'athletes-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss']
})
export class FormAthletesComponent implements OnInit {

  form: FormGroup;

  constructor() { }

  email = new FormControl('', [Validators.required, Validators.email]);

  getErrorMessage() {
    if (this.email.hasError('required')) {
      return 'You must enter a value';
    }

    return this.email.hasError('email') ? 'Not a valid email' : '';
  }

  ngOnInit(): void {
  }

}
