import { PaginationResponse } from 'sp-core';

import { UserWidgetResponse } from './user-widget-response.interface';

export interface UserWidgetsResponse {
    data: Array<UserWidgetResponse>;
    pagination:PaginationResponse;
}