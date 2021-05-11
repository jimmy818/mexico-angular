import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'teams-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss']
})
export class TeamsFormComponent implements OnInit {

  constructor() { }

  name = new FormControl('', [Validators.required]);

  // getErrorMessage() {
  //   if (this.email.hasError('required')) {
  //     return 'You must enter a value';
  //   }
  //
  //   return this.email.hasError('email') ? 'Not a valid email' : '';
  // }

  ngOnInit(): void {
  }

}
