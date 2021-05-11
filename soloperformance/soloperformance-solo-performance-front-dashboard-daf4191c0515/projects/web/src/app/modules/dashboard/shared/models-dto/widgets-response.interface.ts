import { PaginationResponse } from 'sp-core';

import { WidgetResponse } from './widget-response.interface';

export interface WidgetsResponse {
    data: Array<WidgetResponse>;
    pagination: PaginationResponse;
}