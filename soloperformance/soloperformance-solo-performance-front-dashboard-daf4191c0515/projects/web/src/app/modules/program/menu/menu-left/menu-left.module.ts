import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { MenuLeftComponent } from './menu-left.component';
import { WarningDialogModule } from '@web/shared/components/warning-dialog/warning-dialog.module';


@NgModule({
  declarations: [MenuLeftComponent],
  imports: [
    CommonModule, MatButtonModule, WarningDialogModule, DragDropModule
  ],
  exports: [MenuLeftComponent]
})
export class MenuLeftModule { }
