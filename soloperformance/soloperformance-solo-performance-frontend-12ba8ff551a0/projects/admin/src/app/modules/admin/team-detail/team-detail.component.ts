import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'admin-team-detail',
  templateUrl: './team-detail.component.html',
  styleUrls: ['./team-detail.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class TeamDetailComponent implements OnInit {

  teamDetailForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.teamDetailForm = this.fb.group({
      name: '',
      lastName: '',
      email: ''
    })
  }

  ngOnInit(): void {
  }

}
