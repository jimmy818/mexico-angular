import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Params, Router, Event } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { RolesFormComponent } from './roles/form/form.component';
import { TeamsFormComponent } from './teams/form/form.component';
import { FormAthletesComponent } from './athletes/form/form.component';


@Component({
  selector: 'web-library',
  templateUrl: './library.component.html',
  styles: [`
    .menu a{
      font-family: Caros;
      font-style: normal;
      font-weight: 500;
      font-size: 14px;
      line-height: 24px;
      text-align: center;
      color: #6E788F;
      text-decoration: none;
      padding-left: 42px;
    }
    .menu.bold a{
      font-weight: bold;
      line-height: 22px;
      color: #10181F;
    }
    .menu a.active{
      color: #EA1C2C;
    }
    .btn-primary, .btn-primary:active{
      border-color: #192D3F!important;
      background: #192D3F!important;
      border-radius: 6px;
    }
    .btn-primary:focus, .btn-primary:active{
      box-shadow: 0 0 0 0.2rem rgba(25, 45, 63, 0.5)!important;
    }
  `]
})
export class LibraryComponent implements OnInit {

  btnAdd: string;
  component: any;

  constructor(
    private RT: Router,
    private AR: ActivatedRoute,
    private MD: MatDialog,
  ) {
    this.RT.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        console.log(event.url);
        if (event.url.includes('/roles')) {
          this.btnAdd = 'User'
          this.component = RolesFormComponent
        } else if (event.url.includes('/teams')) {
          this.btnAdd = 'Team'
          this.component = TeamsFormComponent;
        } else if (event.url.includes('/athletes')) {
          this.btnAdd = 'Athlete'
          this.component = FormAthletesComponent
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
