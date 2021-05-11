import { Pipe, PipeTransform } from '@angular/core';

import { UtilitiesService } from '@admin/core/services/utilities.service';

@Pipe({
  name: 'dbName'
})
export class DbNamePipe implements PipeTransform {

  transform(value: string): string {
    return UtilitiesService.getDbName(value);
  }

}
