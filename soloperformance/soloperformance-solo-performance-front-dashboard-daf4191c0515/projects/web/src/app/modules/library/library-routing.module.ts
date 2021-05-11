import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LibraryComponent } from './library.component';

const routes: Routes = [
  {
    path: '',
    component: LibraryComponent,
    children: [
      { path: '', redirectTo: 'programs', pathMatch: 'full' },
      {
        path: 'programs',
        loadChildren: () => import('./programs/programs.module').then(m => m.ProgramsModule)
      },
      {
        path: 'phases',
        loadChildren: () => import('./phases/phases.module').then(m => m.PhasesModule)
      },
      {
        path: 'workouts',
        loadChildren: () => import('./workouts/workouts.module').then(m => m.WorkoutsModule)
      },
      {
        path: 'blocks',
        loadChildren: () => import('./blocks/blocks.module').then(m => m.BlocksModule)
      },
      {
        path: 'exercises',
        loadChildren: () => import('./exercises/exercises.module').then(m => m.ExercisesModule)
      },
      {
        path: 'template-sets',
        loadChildren: () => import('./template-sets/template-sets.module').then(m => m.TemplateSetsModule)
      }
    ]
  },
  {
    path: 'workout-builder',
    loadChildren: () => import('./workout-builder/workout-builder.module').then(m => m.WorkoutBuilderModule)
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LibraryRoutingModule { }
