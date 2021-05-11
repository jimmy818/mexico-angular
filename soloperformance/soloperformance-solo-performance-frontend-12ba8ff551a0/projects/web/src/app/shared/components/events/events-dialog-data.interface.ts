import { EventApp } from './event-app.interface';

export interface EventsDialogData {
    date: Date;
    /**
     * Obtiene o establece si los eventos a obtener son del mes completo
     */
    isMonth: boolean,
    events: Array<EventApp>;
}