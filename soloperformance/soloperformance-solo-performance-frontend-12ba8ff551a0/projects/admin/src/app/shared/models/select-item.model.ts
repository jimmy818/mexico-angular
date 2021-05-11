import { Periodicity } from '../enums/periodicity.enum';

export interface SelectItem {
    value: string | Periodicity;
    text: string;
}