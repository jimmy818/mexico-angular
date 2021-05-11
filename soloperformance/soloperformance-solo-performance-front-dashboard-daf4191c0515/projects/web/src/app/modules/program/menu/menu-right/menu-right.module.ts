import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MenuRightComponent } from './menu-right.component';

@NgModule({
  declarations: [MenuRightComponent],
  imports: [CommonModule, MatButtonModule],
  exports: [MenuRightComponent]
})
export class MenuRightModule { }
