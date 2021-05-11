import { weekdays } from 'moment';
import { Day, Week } from 'sp-core';

import { WeekDay } from './week-day';

export class WeekDays {

    public readonly days = new Week().days.map(day => new WeekDay(day))

    constructor() { }

    /**
     * Selecciona el día indicado de la semana
     * @param day Día a seleccionar
     */
    selectDay(day: Day) {
        this.days
            .filter(weekDay => weekDay.day === day)
            .forEach(weekDay => weekDay.selected = true);
    }

    /**
     * Verifica si existe algún día seleccionado en la semana
     */
    checkDaySelected() {
        return this.days.filter(weekDay => weekDay.selected === true).length > 0 ? true : false;
    }

    /**
     * Clona un objeto semana días.
     * Útil cuando no se quiere modificar un arreglo de semanas días sino hasta que así lo especifica alguna acción del usuario.
     * @param weekDays Semana, días a clonar
     */
    clone(weekDays: WeekDays): WeekDays {
        const weekDaysCloned = new WeekDays();
        weekDays.days.map(weekDay => {
            weekDaysCloned.days
                .filter(weekDayCloned => weekDayCloned.day === weekDay.day)
                .forEach(weekDayCloned => weekDayCloned.selected = weekDay.selected);
        });
        return weekDaysCloned;
    }
}