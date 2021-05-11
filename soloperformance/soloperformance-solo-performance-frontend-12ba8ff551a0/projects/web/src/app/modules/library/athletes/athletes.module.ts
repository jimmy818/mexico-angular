import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AthletesComponent } from './athletes.component';
import { RouterModule } from '@angular/router';
import { SharedModule } from '@web/shared/shared.module';
import { SpLibraryModule } from 'sp-library';
import { TableModule } from '@web/shared/components/table/table.module';
// import { FormAthletesModule } from './form/form.module';


@NgModule({
  declarations: [AthletesComponent],
  imports: [
    RouterModule.forChild([{ path: '', component: AthletesComponent }]),
    CommonModule,
    SharedModule,
    SpLibraryModule,
    TableModule,
  ]
})
export class AthletesModule { }
