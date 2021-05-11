import { Pipe, PipeTransform } from '@angular/core';

import { Gender } from 'sp-core';

@Pipe({
  name: 'gender'
})
export class GenderPipe implements PipeTransform {

  transform(gender: Gender): string {
    switch (gender) {
      case Gender.female:
        return 'Female';
      case Gender.male:
        return 'Male';
      case Gender.other:
        return 'Other';
    }
  }
}