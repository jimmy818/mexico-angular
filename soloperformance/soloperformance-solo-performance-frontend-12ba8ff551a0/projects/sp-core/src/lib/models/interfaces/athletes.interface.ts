import { Athlete } from './athlete.interface';
import { Data } from './data.interface';

export interface Athletes extends Data {
    data: Array<Athlete>;
}