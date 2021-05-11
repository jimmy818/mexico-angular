import { Pipe, PipeTransform } from '@angular/core';

import { Periodicity } from '@admin/shared/enums/periodicity.enum';

@Pipe({
  name: 'averageRevenue'
})
export class AverageRevenuePipe implements PipeTransform {

  transform(periodicity: Periodicity): string {
    switch (periodicity) {
      case Periodicity.weekly:
        return 'Weekly Revenue';
      case Periodicity.monthly:
        return 'Monthly Revenue';
      case Periodicity.yearly:
        return 'Yearly Revenue';
      default:
        return '';
    }
  }

}
