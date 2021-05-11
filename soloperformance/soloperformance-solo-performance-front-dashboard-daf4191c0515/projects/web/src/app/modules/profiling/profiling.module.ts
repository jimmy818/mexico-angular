import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { SpHeaderModule } from 'sp-library';

import { ProfilingRoutingModule } from './profiling-routing.module';
import { ProfilingComponent } from './profiling.component';

const COMPONENTS = [ProfilingComponent];

@NgModule({
  declarations: [...COMPONENTS],
  imports: [
    CommonModule,
    ProfilingRoutingModule,
    MatButtonModule,
    SpHeaderModule,
  ],
  exports: [...COMPONENTS],
})
export class ProfilingModule {}
