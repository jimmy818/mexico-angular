import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { RolesComponent } from './roles.component';
import { SpLibraryModule } from 'sp-library';
import { SharedModule } from '@web/shared/shared.module';
import { TableModule } from '@web/shared/components/table/table.module';


@NgModule({
  declarations: [RolesComponent],
  imports: [
    RouterModule.forChild([{ path: '', component: RolesComponent }]),
    CommonModule,
    SharedModule,
    SpLibraryModule,
    TableModule
  ]
})
export class RolesModule { }
