import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AssignProgramComponent } from './dialogs/assign-program/assign-program.component';
import { PhaseDialogComponent } from './dialogs/phase/phase.component';
import { ProgramDialogComponent } from './dialogs/program/program.component';

@Component({
  selector: 'web-program',
  templateUrl: './program.component.html',
  styleUrls: ['./program.component.scss']
})
export class ProgramComponent implements OnInit {

  programs: any[] = [
    {
      name: 'Jump & Agility Program',
      phases: [
        { id: 1, name: 'Strenght Upper/Lower', weeks: [{}, {}, {}], number: 375, active: true },
        { id: 2, name: 'Strenght Upper/Lower', weeks: [{}], number: 70, active: false },
        // { id: 3, name: 'Strenght Upper/Lower', weeks: [{}], number: 234, active: false },
        // { id: 4, name: 'Strenght Upper/Lower', weeks: [{}], number: 264, active: false },
        // { id: 4, name: 'Strenght Upper/Lower', weeks: [{}], number: 264, active: false },

      ],
      athletes: [
        { photo: 'https://randomuser.me/api/portraits/men/3.jpg', name: 'juan' },
        { photo: 'https://randomuser.me/api/portraits/men/89.jpg', name: 'Carlos' },
        { photo: 'https://randomuser.me/api/portraits/men/50.jpg', name: 'Pepe' },
        { photo: 'https://randomuser.me/api/portraits/men/39.jpg', name: 'Cristian' },
        { photo: 'https://randomuser.me/api/portraits/men/43.jpg', name: 'Manuel' },
        { photo: 'https://randomuser.me/api/portraits/men/13.jpg', name: 'Jose' },
      ],
      teams: [
        { photo: 'https://randomuser.me/api/portraits/men/32.jpg', name: 'juan' },
        { photo: 'https://randomuser.me/api/portraits/men/83.jpg', name: 'Carlos' },
        { photo: 'https://randomuser.me/api/portraits/men/54.jpg', name: 'Pepe' },
        { photo: 'https://randomuser.me/api/portraits/men/36.jpg', name: 'Cristian' },
        { photo: 'https://randomuser.me/api/portraits/men/47.jpg', name: 'Manuel' },
        { photo: 'https://randomuser.me/api/portraits/men/18.jpg', name: 'Jose' },
      ]
    }
  ]


  constructor(
    private MD: MatDialog,
  ) { }

  ngOnInit(): void {
  }

  add(view: string): void {
    let component: any;
    switch (view) {
      case 'assign':
        component = AssignProgramComponent
        break;
      case 'program':
        component = ProgramDialogComponent
        break;
      case 'phase':
        component = PhaseDialogComponent
        break;
      default:
        break;
    }
    const dialogRef = this.MD.open(component, {
      width: '600px',
      disableClose: true,
      data: <any>{
        institutionId: null
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      // Si no se obtuvo respuesta no procede con las acciones.
      if (!result) {
        return;
      }
      // this.selectedInstitution = null;
      // TODO: Envíar notificación de que se requiere actualizar la lista de instituciones.
    });
  }

  newProgram(): void {
    this.programs.push({
      name: '',
      phase: [],
      athletes: [],
      teams: []
    })
  }

}
