import { Pipe, PipeTransform } from '@angular/core';

import { Day } from 'sp-core';

@Pipe({
  name: 'day'
})
export class DayPipe implements PipeTransform {

  transform(day: Day): string {
    switch (day) {
      case Day.monday:
        return 'M';
      case Day.tuesday:
        return 'T';
      case Day.wednesday:
        return 'W';
      case Day.thursday:
        return 'T';
      case Day.friday:
        return 'F';
      case Day.saturday:
        return 'S';
      case Day.sunday:
        return 'S';
      default:
        return '';
    }
  }
}
