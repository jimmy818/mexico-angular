import { ComponentRef } from '@angular/core';
import { GridStackItemComponent } from '../../../grid-stack-item/grid-stack-item.component';
import { Widget } from './widget.interface';
import { UserWidget } from './user-widget.interface';

export interface GridStackMetadata {

    /**
     * Obtiene o establece el dentificador único del widget.
     */
    id: number,

    /**
     * Obtiene o establece el elemento HTML del widget agregado en el grid (GridStack)
     */
    gridStackItem: HTMLElement,

    /**
     * Obtiene o establece el componente angular por creación dinámica
     */
    component: ComponentRef<GridStackItemComponent>

    /**
     * Obtiene o establece el widget origen del componente.
     */
    widget: Widget

    /**
     * Obtiene o establece la asignación del widget con el usuario. 
     * Sino tiene asignación significa que recién se está agregando. 
     * En caso de tener asignación significa que es un registro obtenido de BD
     */
    userWidget: UserWidget;
}