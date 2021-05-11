import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ManagementComponent } from './management.component';

const routes: Routes = [
  {
    path: '',
    component: ManagementComponent,
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'roles' },
      {
        path: 'roles',
        loadChildren: () => import('./roles/roles.module').then(m => m.RolesModule)
      },
      {
        path: 'teams',
        loadChildren: () => import('./teams/teams.module').then(m => m.TeamsModule)
      },
      {
        path: 'athletes',
        loadChildren: () => import('./athletes/athletes.module').then(m => m.AthletesModule)
      },
      {
        path: 'coaches',
        loadChildren: () => import('./coaches/coaches.module').then(m => m.CoachesModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ManagementRoutingModule { }
