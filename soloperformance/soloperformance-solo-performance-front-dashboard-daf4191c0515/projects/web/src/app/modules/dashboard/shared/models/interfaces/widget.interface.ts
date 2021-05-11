import { WidgetType } from '../enums/widget-type.enum';

export interface Widget {
    type: WidgetType,
    name: string;
    image: string;
    /**
     * Tamaño en columnas del widget. Valores predefinidos según el tipo de widget
     */
    size: number;

    gridStackItemId: number;
}