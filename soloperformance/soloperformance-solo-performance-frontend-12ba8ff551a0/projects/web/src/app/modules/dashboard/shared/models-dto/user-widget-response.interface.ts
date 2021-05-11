import { WidgetResponse } from './widget-response.interface';

export interface UserWidgetResponse {
    id: number;
    axis_x: number,
    axis_y: number,
    widget: WidgetResponse;
}