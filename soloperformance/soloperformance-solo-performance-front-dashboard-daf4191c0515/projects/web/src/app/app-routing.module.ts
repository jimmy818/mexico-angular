import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from 'sp-core';

import { AuthLayoutComponent } from './layouts/auth-layout/auth-layout.component';
import { MainLayoutComponent } from './layouts/main-layout/main-layout.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full',
  },
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: 'dashboard',
        canActivateChild: [AuthGuard],
        loadChildren: () =>
          import('@web/modules/dashboard/dashboard.module').then(
            (m) => m.DashboardModule
          ),
      },
      {
        path: 'management',
        canActivateChild: [AuthGuard],
        loadChildren: () =>
          import('@web/modules/management/management.module').then(
            (m) => m.ManagementModule
          ),
      },
      {
        path: 'program',
        canActivateChild: [AuthGuard],
        loadChildren: () =>
          import('@web/modules/program/program.module').then(
            (m) => m.ProgramModule
          ),
      },
      {
        path: 'library',
        canActivateChild: [AuthGuard],
        loadChildren: () =>
          import('@web/modules/library/library.module').then(
            (m) => m.LibraryModule
          ),
      },
      {
        path: 'profiling',
        canActivateChild: [AuthGuard],
        loadChildren: () =>
          import('@web/modules/profiling/profiling.module').then(
            (m) => m.ProfilingModule
          ),
      },
    ],
  },
  {
    path: 'auth',
    component: AuthLayoutComponent,
    loadChildren: () =>
      import('@web/modules/auth/auth.module').then((m) => m.AuthModule),
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
