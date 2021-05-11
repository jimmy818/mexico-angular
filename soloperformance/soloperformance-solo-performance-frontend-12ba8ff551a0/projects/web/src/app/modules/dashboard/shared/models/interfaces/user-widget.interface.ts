import { WidgetType } from '../enums/widget-type.enum';

export interface UserWidget {

    /**
     * Identificador del widget en la lista de widget de usuario
     */
    id: number,
    name: string;
    image: string;

    /**
     * Posición X configurada para el widget
     */
    axisX: number,

    /**
     * Posición Y configurada para el widget
     */
    axisY: number,

    /**
     * Tipo de widget. Main widget, Team list, etc
     */
    type: WidgetType;

    /**
     * Tamaño de columna según el tipo de widget
     */
    size: number;
}