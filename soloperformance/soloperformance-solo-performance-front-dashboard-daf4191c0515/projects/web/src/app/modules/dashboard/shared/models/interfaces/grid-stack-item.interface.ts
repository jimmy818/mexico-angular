import { Type } from '@angular/core';

import { GridStackItemContent } from './grid-stack-item-content.interface';
import { Widget } from './widget.interface';

export class GridStackItem {
    content: Type<GridStackItemContent>;
    widget: Widget;
}