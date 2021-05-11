import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BlockListComponent } from './block-list/block-list.component';

import { BlocksComponent } from './blocks.component';

const routes: Routes = [
  {
    path: '',
    component: BlocksComponent,
    children: [
      { path: '', redirectTo: 'my-blocks', pathMatch: 'full' },
      {
        path: 'all-blocks',
        component: BlockListComponent
      },
      {
        path: 'my-blocks',
        component: BlockListComponent
      },
      {
        path: 'institutional-blocks',
        component: BlockListComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BlocksRoutingModule { }
