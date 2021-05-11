import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenuRightComponent } from './menu-right.component';
import { MatButtonModule } from '@angular/material/button';

@NgModule({
  declarations: [MenuRightComponent],
  imports: [CommonModule, MatButtonModule],
  exports: [MenuRightComponent]
})
export class MenuRightModule { }
