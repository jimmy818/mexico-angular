import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TeamsComponent } from './teams.component';
import { TeamsListComponent } from './teams-list/teams-list.component';

const routes: Routes = [
  {
    path: '',
    component: TeamsComponent,
    children: [
      {
        path: '',
        redirectTo: 'my-teams',
        pathMatch: 'full',
      },
      {
        path: 'mexico',
        component: TeamsListComponent,
      },
      {
        path: 'usa',
        component: TeamsListComponent,
      },
      {
        path: 'a',
        component: TeamsListComponent,
      },
      {
        path: 'junior',
        component: TeamsListComponent,
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TeamsRoutingModule { }
