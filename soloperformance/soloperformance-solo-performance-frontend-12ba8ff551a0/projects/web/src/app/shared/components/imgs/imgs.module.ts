import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImgsComponent } from './imgs.component';
import { ImgsPipe } from './imgs.pipe';


@NgModule({
  declarations: [ImgsComponent, ImgsPipe],
  imports: [CommonModule],
  exports: [ImgsComponent]
})
export class ImgsModule { }
