import { Widget } from './widget.interface';

export interface GridStackItemContent {
    
    widget: Widget;

    deleteWidget():void;

    duplicateWidget():void;
}