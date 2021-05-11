import { BlockTypeResponse } from './interfaces/block-type-response.interface';

export class BlockType {

    constructor(
        public id?: number,
        public name?: string,
        public isActive?: boolean
    ) { }

    static fromResponse(response: BlockTypeResponse): BlockType {
        return new BlockType(
            response.id,
            response.name,
            response.active
        );
    }
}