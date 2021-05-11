export interface WidgetResponse {
    /**
     * Representa el identificador del registro en la tabla.
     * Adicional también representa el tipo de widget. 1: Team list, 2:Athlete list, etc...
     */
    id: number;
    name: string;
    image: string;
}