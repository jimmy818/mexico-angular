import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { DragDropModule } from '@angular/cdk/drag-drop';

import { DialogComponent } from './dialog.component';
import { DialogTitleComponent } from './dialog-title/dialog-title.component';
import { DialogContentComponent } from './dialog-content/dialog-content.component';
import { DialogActionsComponent } from './dialog-actions/dialog-actions.component';

const COMPONENTS = [
  DialogComponent,
  DialogTitleComponent,
  DialogContentComponent,
  DialogActionsComponent
]

@NgModule({
  declarations: [COMPONENTS],
  imports: [
    CommonModule,
    MatButtonModule,
    MatDialogModule,
    DragDropModule
  ],
  exports: [COMPONENTS]
})
export class SpDialogModule { }
