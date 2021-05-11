import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, NavigationEnd, Router, Event } from '@angular/router';
import { FormAthletesComponent } from './athletes/form/form.component';
import { RolesFormComponent } from './roles/form/form.component';
import { TeamsFormComponent } from './teams/form/form.component';

@Component({
  selector: 'web-management',
  templateUrl: './management.component.html',
  styleUrls: ['./management.component.scss']
})
export class ManagementComponent implements OnInit {

  btnAdd: string;
  component: any;

  constructor(
    private RT: Router,
    private AR: ActivatedRoute,
    private MD: MatDialog,
  ) {
    this.RT.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        if (event.url.includes('/roles')) {
          this.btnAdd = 'user'
          this.component = RolesFormComponent
        } else if (event.url.includes('/teams')) {
          this.btnAdd = 'team'
          this.component = TeamsFormComponent;
        } else if (event.url.includes('/athletes')) {
          this.btnAdd = 'athlete'
          this.component = FormAthletesComponent
        } else {
          this.btnAdd = 'user'
          this.component = RolesFormComponent
        }
      }
    });
  }

  ngOnInit(): void {
  }

  add() {
    const dialogRef = this.MD.open(this.component, {
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

}
