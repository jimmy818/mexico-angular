import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'imgs'
})
export class ImgsPipe implements PipeTransform {

  transform(img: string): string {
    return img ? img : 'https://www.cobdoglaps.sa.edu.au/wp-content/uploads/2017/11/placeholder-profile.jpg';
  }

}
