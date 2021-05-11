import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@web/shared/shared.module';
import { TeamsFormComponent } from './form.component';
import { SpDialogModule } from 'sp-dialog';
import { UploadImageModule } from '@web/shared/components/upload-image/upload-image.module';

@NgModule({
  declarations: [TeamsFormComponent],
  imports: [
    CommonModule,
    SpDialogModule,
    SharedModule,
    UploadImageModule
  ],
  exports: [TeamsFormComponent]
})
export class TeamsFormModule { }
