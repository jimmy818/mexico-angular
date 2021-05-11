import { Day } from './enums/day.enum';

export class Week {
    public readonly days = [
        Day.monday,
        Day.tuesday,
        Day.wednesday,
        Day.thursday,
        Day.friday,
        Day.saturday,
        Day.sunday
    ];
    constructor() { }
}