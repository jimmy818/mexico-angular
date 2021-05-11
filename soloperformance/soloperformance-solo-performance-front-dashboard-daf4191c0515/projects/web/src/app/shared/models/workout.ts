import { BlockCoding } from './block-coding';

export class Workout {
    constructor(
        public name?: string,
        public blockCategories: Array<BlockCoding> = []
    ) { }
}