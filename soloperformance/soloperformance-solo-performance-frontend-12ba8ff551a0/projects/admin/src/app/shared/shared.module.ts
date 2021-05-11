import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MaterialModule } from '../material/material.module';

import { AdminChartTitlePipe } from './pipes/admin-chart-title.pipe';
import { AdminChartSubtitlePipe } from './pipes/admin-chart-subtitle.pipe';
import { AverageRevenuePipe } from './pipes/average-revenue.pipe';
import { RowStatusPipe } from './pipes/row-status.pipe';
import { DbNamePipe } from './pipes/db-name.pipe';
import { HeaderComponent } from './components/header/header.component';
import { SpLibraryModule } from 'sp-library';

const components = [
  HeaderComponent,
  AdminChartTitlePipe,
  AdminChartSubtitlePipe,
  AverageRevenuePipe,
  RowStatusPipe,
  DbNamePipe
];

@NgModule({
  declarations: [
    components
  ],
  imports: [
    CommonModule,
    MaterialModule,
    SpLibraryModule
  ],
  exports: [
    CommonModule,
    MaterialModule,
    SpLibraryModule,
    components
  ]
})
export class SharedModule { }
