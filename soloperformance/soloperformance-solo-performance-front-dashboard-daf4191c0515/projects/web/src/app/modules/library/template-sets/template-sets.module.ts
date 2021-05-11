import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SpCardModule } from 'sp-library';

import { TemplateSetsRoutingModule } from './template-sets-routing.module';
import { TemplateSetsComponent } from './template-sets.component';


@NgModule({
  declarations: [TemplateSetsComponent],
  imports: [
    CommonModule,
    TemplateSetsRoutingModule,
    SpCardModule
  ]
})
export class TemplateSetsModule { }
