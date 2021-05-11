import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenuLeftComponent } from './menu-left.component';



@NgModule({
  declarations: [MenuLeftComponent],
  imports: [
    CommonModule
  ],
  exports: [MenuLeftComponent]
})
export class MenuLeftModule { }
