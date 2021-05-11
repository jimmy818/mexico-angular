import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { SpCardModule, SpHeaderModule, SpInputSearchModule } from 'sp-library';

import { TeamsRoutingModule } from './teams-routing.module';
import { TeamsComponent } from './teams.component';
import { TeamsListComponent } from './teams-list/teams-list.component';
import { TeamsDetailComponent } from './teams-detail/teams-detail.component';

const COMPONENTS = [TeamsComponent, TeamsListComponent, TeamsDetailComponent];

@NgModule({
  declarations: [...COMPONENTS],
  imports: [
    CommonModule,
    TeamsRoutingModule,
    MatButtonModule,
    SpInputSearchModule,
    SpCardModule,
    SpHeaderModule,
  ],
  exports: [...COMPONENTS],
})
export class TeamsModule {}
