import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatSelectChange } from '@angular/material/select';

import { Gender } from 'sp-core';

@Component({
  selector: 'sp-gender-select',
  templateUrl: './gender-select.component.html',
  styleUrls: ['./gender-select.component.scss']
})
export class GenderSelectComponent implements OnInit {

  @Input() required = false;

  @Output() genderChange = new EventEmitter<MatSelectChange>();

  genders: Array<Gender> = [];

  constructor() {
    this.genders.push(Gender.female);
    this.genders.push(Gender.male);
    this.genders.push(Gender.other);
  }

  ngOnInit(): void {
  }

  selectionChanged(matSelect: MatSelectChange): void {
    this.genderChange.emit(matSelect);
  }
}
