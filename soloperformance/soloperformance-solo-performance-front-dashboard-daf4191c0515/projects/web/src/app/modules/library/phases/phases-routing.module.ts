import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PhasesComponent } from './phases.component';
import { PhaseListComponent } from './phase-list/phase-list.component';

const routes: Routes = [
  {
    path: '',
    component: PhasesComponent,
    children: [
      { path: '', redirectTo: 'my-phases', pathMatch: 'full' },
      {
        path: 'all-phases',
        component: PhaseListComponent
      },
      {
        path: 'my-phases',
        component: PhaseListComponent
      },
      {
        path: 'institutional-phases',
        component: PhaseListComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PhasesRoutingModule { }
