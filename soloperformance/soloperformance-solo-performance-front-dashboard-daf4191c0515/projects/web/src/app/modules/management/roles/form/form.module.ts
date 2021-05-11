import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RolesFormComponent } from './form.component';
import { SpDialogModule } from 'sp-dialog';
import { SharedModule } from '@web/shared/shared.module';



@NgModule({
  declarations: [RolesFormComponent],
  imports: [
    CommonModule,
    SpDialogModule,
    SharedModule,
  ],
  exports: [RolesFormComponent]
})
export class RolesFormModule { }
