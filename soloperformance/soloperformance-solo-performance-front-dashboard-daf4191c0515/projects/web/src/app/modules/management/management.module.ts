import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { SpDialogModule } from 'sp-dialog';
import { SpInputSearchModule, SpHeaderModule, SpCardModule } from 'sp-library';

import { ManagementRoutingModule } from './management-routing.module';
import { ManagementComponent } from './management.component';
import { RolesFormModule } from './roles/form/form.module';
import { TeamsFormModule } from './teams/form/form.module';
import { FormAthletesModule } from './athletes/form/form.module';


@NgModule({
  declarations: [ManagementComponent],
  imports: [
    CommonModule,
    ManagementRoutingModule,
    MatButtonModule,
    SpInputSearchModule,
    SpHeaderModule,
    SpDialogModule,
    SpCardModule,
    RolesFormModule,
    TeamsFormModule,
    FormAthletesModule
  ]
})
export class ManagementModule { }
