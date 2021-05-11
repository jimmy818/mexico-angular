import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from 'sp-core';

import { AuthLayoutComponent } from './layouts/auth-layout/auth-layout.component';
import { MainLayoutComponent } from './layouts/main-layout/main-layout.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'auth',
    pathMatch: 'full'
  },
  {
    path: 'auth',
    component: AuthLayoutComponent,
    loadChildren: () => import('@web/modules/auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: 'dashboard',
        canActivateChild: [AuthGuard],
        loadChildren: () => import('@web/modules/dashboard/dashboard.module').then(m => m.DashboardModule)
      },
      {
        path: 'library',
        canActivateChild: [AuthGuard],
        loadChildren: () => import('@web/modules/library/library.module').then(m => m.LibraryModule)
      },
      {
        path: 'program',
        canActivateChild: [AuthGuard],
        loadChildren: () => import('@web/modules/program/program.module').then(m => m.ProgramModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
