import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CoachesComponent } from './coaches.component';
import { RouterModule } from '@angular/router';
import { SpLibraryModule, SpCardModule } from 'sp-library';


@NgModule({
  declarations: [CoachesComponent],
  imports: [
    RouterModule.forChild([{ path: '', component: CoachesComponent }]),
    CommonModule,
    SpCardModule,
    SpLibraryModule
  ]
})
export class CoachesModule { }
