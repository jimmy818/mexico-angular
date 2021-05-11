import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProgramsComponent } from './programs.component';
import { ProgramListComponent } from './program-list/program-list.component';

const routes: Routes = [
  {
    path: '',
    component: ProgramsComponent,
    children: [
      {
        path: '',
        redirectTo: 'my-programs',
        pathMatch: 'full'
      },
      {
        path: 'all-programs',
        component: ProgramListComponent
      },
      {
        path: 'my-programs',
        component: ProgramListComponent
      },
      {
        path: 'institutional-programs',
        component: ProgramListComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProgramsRoutingModule { }
