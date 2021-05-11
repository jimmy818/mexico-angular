import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { SpHeaderModule, SpInputSearchModule, SpCardModule } from 'sp-library';

import { BlocksRoutingModule } from './blocks-routing.module';
import { BlocksComponent } from './blocks.component';
import { BlockListComponent } from './block-list/block-list.component';

const COMPONENTS = [
  BlocksComponent,
  BlockListComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule,
    BlocksRoutingModule,
    MatButtonModule,
    SpInputSearchModule,
    SpHeaderModule,
    SpCardModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class BlocksModule { }
