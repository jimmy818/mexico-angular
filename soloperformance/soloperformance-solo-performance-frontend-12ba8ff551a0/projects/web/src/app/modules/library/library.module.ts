import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LibraryRoutingModule } from './library-routing.module';
import { LibraryComponent } from './library.component';
import { SpDialogModule } from 'sp-dialog';
import { SharedModule } from '@web/shared/shared.module';
import { RolesFormModule } from './roles/form/form.module';
import { TeamsFormModule } from './teams/form/form.module';
import { FormAthletesModule } from './athletes/form/form.module';


@NgModule({
  declarations: [
    LibraryComponent,
  ],
  imports: [
    CommonModule,
    LibraryRoutingModule,
    SpDialogModule,
    SharedModule,
    RolesFormModule,
    TeamsFormModule,
    FormAthletesModule
  ]
})
export class LibraryModule { }
