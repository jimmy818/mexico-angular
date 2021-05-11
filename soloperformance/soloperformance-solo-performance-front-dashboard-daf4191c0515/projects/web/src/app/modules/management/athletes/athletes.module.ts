import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';

import { SpDialogModule } from 'sp-dialog';
import { SpCardModule } from 'sp-library';

import { TableModule } from '@web/shared/components/table/table.module';

import { AthletesComponent } from './athletes.component';


@NgModule({
  declarations: [AthletesComponent],
  imports: [
    RouterModule.forChild([{ path: '', component: AthletesComponent }]),
    CommonModule,
    MatTableModule,
    MatButtonModule,
    SpCardModule,
    SpDialogModule,
    TableModule,
  ]
})
export class AthletesModule { }
