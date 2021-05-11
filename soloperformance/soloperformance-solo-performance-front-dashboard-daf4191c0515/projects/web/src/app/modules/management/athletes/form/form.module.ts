import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { FormAthletesComponent } from './form.component';
import { SpDialogModule } from 'sp-dialog';
import { SharedModule } from '@admin/shared/shared.module';


@NgModule({
  declarations: [FormAthletesComponent],
  imports: [
    CommonModule,
    SpDialogModule,
    SharedModule,
    ReactiveFormsModule,
  ],
  exports: [FormAthletesComponent]
})
export class FormAthletesModule { }
