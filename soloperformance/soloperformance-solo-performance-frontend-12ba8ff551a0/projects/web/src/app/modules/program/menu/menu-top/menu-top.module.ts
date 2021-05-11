import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenuTopComponent } from './menu-top.component';


@NgModule({
  declarations: [MenuTopComponent],
  imports: [
    CommonModule
  ],
  exports: [MenuTopComponent]
})
export class MenuTopModule { }
