import { Pipe, PipeTransform } from '@angular/core';

import { SubscriptionType } from 'sp-core';

@Pipe({
  name: 'subscriptionType'
})
export class SubscriptionTypePipe implements PipeTransform {

  transform(type: SubscriptionType): string {
    switch (type) {
      case SubscriptionType.trial:
        return 'Trial';
      case SubscriptionType.paying:
        return 'Paying';
      case SubscriptionType.demo:
        return 'Demo';
      default:
        return '';
    }
  }

}
