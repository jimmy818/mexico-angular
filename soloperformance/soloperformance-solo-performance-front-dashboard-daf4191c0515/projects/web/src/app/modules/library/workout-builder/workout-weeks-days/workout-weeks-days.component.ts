import { Component, OnInit, Output, EventEmitter, Inject, ViewEncapsulation } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

import { WeekDays } from 'sp-library';

@Component({
  selector: 'web-workout-weeks-days',
  templateUrl: './workout-weeks-days.component.html',
  styleUrls: ['./workout-weeks-days.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class WorkoutWeeksDaysComponent implements OnInit {

  @Output() weeksDaysChange = new EventEmitter<Array<WeekDays>>();

  weeksDays: Array<WeekDays> = [];

  constructor(
    @Inject(MAT_DIALOG_DATA) private data: Array<WeekDays>,
    private dialogRef: MatDialogRef<WorkoutWeeksDaysComponent>
  ) { }

  ngOnInit(): void {
    // Asigna las semanas días al componente. Se clona debido a que aún no se quiere afectar el arreglo sino hasta que se indica continuar con el proceso de agregar workout
    this.weeksDays = this.data.map(weekDays => {
      return new WeekDays().clone(weekDays);
    });
  }

  onWeeksDaysChange(weeksDays: Array<WeekDays>): void {
    this.weeksDays = weeksDays;
    this.weeksDaysChange.emit(this.weeksDays);
  }

  continueClick(): void {
    this.dialogRef.close(this.weeksDays);
  }
}
