import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TableComponent } from './table.component';
import { SpLibraryModule } from 'sp-library';
import { SharedModule } from '@admin/shared/shared.module';


@NgModule({
  declarations: [TableComponent],
  imports: [
    CommonModule,
    SharedModule,
    SpLibraryModule
  ],
  exports: [TableComponent]
})
export class TableModule { }
