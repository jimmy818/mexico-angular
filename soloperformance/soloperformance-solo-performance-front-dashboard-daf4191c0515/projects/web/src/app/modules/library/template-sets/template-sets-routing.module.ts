import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TemplateSetsComponent } from './template-sets.component';

const routes: Routes = [
  {
    path: '',
    component: TemplateSetsComponent,
    children: [
      //{ path: '', redirectTo: '', pathMatch: 'full' }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TemplateSetsRoutingModule { }
