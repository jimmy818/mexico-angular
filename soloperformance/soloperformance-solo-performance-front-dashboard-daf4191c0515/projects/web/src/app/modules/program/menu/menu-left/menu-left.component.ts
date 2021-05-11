import { Component, Input, OnInit } from '@angular/core';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';
import { MatDialog } from '@angular/material/dialog';
import { WarningDialogComponent } from '@web/shared/components/warning-dialog/warning-dialog.component';

@Component({
  selector: 'program-menu-left',
  templateUrl: './menu-left.component.html',
  styleUrls: ['./menu-left.component.scss']
})
export class MenuLeftComponent implements OnInit {

  @Input() phases: any[] = []

  constructor(
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
  }

  // Elimina la fase
  deletePhase(i: number): void {
    const dialogRef = this.dialog.open(WarningDialogComponent, {
      width: '352px',
      height: '184px',
      data: { text: 'Are you sure you want to delete this phase from the program?' }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) { this.phases.splice(i, 1) }
    });
  }
  // cambia de posicion la fase
  dropPhases(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.phases, event.previousIndex, event.currentIndex);
  }

  // Elimina la semana
  deleteWeek(i: number, ii: number): void {
    const dialogRef = this.dialog.open(WarningDialogComponent, {
      width: '352px',
      height: '184px',
      data: { text: 'Are you sure you want to delete this week from the phase?' }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) { this.phases[i].weeks.splice(ii, 1); }
    });
  }
  // cambia de posicion la semana
  dropWeeks(event: CdkDragDrop<string[]>, i: number) {
    moveItemInArray(this.phases[i].weeks, event.previousIndex, event.currentIndex);
  }

}
