import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';

import { SpLibraryModule } from 'sp-library';
import { SharedModule } from '@admin/shared/shared.module';

import { AdminRoutingModule } from './admin-routing.module';
import { TeamDetailComponent } from './team-detail/team-detail.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ManagerDetailComponent } from './manager-detail/manager-detail.component';
import { InstitutionListComponent } from './shared/components/institution-list/institution-list.component';

const components = [
  DashboardComponent,
  ManagerDetailComponent,
  TeamDetailComponent,
  InstitutionListComponent
]

@NgModule({
  declarations: [
    components
  ],
  imports: [
    AdminRoutingModule,
    ReactiveFormsModule,
    SpLibraryModule,
    SharedModule
  ],
  exports: [
    components
  ],
  providers: []
})
export class AdminModule { }