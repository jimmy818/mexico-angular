import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProfilingComponent } from './profiling.component';

const routes: Routes = [
  {
    path: '',
    component: ProfilingComponent,
    children: [
      { path: '', redirectTo: 'profiling', pathMatch: 'full' },
      {
        path: 'teams',
        loadChildren: () =>
          import('./teams/teams.module').then((m) => m.TeamsModule),
      },
      // {
      //   path: 'athletes',
      //   loadChildren: () =>
      //     import('./athletes/athletes.module').then((m) => m.AthletesModule),
      // },
      // {
      //   path: 'templates',
      //   loadChildren: () =>
      //     import('./templates/templates.module').then((m) => m.TemplatesModule),
      // },
      // {
      //   path: 'test',
      //   loadChildren: () =>
      //     import('./test/test.module').then((m) => m.TestModule),
      // },
    ],
  },
  // {
  //   path: 'workout-builder',
  //   loadChildren: () => import('./workout-builder/workout-builder.module').then(m => m.WorkoutBuilderModule)
  // }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ProfilingRoutingModule {}
