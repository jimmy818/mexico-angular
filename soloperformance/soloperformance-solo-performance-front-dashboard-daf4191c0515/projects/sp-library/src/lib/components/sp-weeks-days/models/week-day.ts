import { Day } from 'sp-core';

export class WeekDay {
    constructor(
        public day: Day,
        public selected = false
    ) { }
}