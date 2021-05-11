import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@web/shared/shared.module';
import { WarningDialogComponent } from './warning-dialog.component';

@NgModule({
  declarations: [WarningDialogComponent],
  imports: [
    CommonModule, SharedModule
  ],
  exports: [WarningDialogComponent]
})
export class WarningDialogModule { }
