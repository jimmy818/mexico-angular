import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'rowStatus'
})
export class RowStatusPipe implements PipeTransform {

  transform(status: boolean): unknown {
    return (status ? 'Active' : 'Inactive');
  }

}
