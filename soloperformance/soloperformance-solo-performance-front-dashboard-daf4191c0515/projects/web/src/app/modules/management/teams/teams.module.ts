import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TeamsComponent } from './teams.component';
import { SpLibraryModule } from 'sp-library';
import { SharedModule } from '@web/shared/shared.module';
import { ImgsModule } from '@web/shared/components/imgs/imgs.module';
import { TableModule } from '@web/shared/components/table/table.module';



@NgModule({
  declarations: [TeamsComponent],
  imports: [
    RouterModule.forChild([{ path: '', component: TeamsComponent }]),
    CommonModule,
    SharedModule,
    SpLibraryModule,
    ImgsModule,
    TableModule
  ]
})
export class TeamsModule { }
