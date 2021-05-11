import { BlockSubcoding } from './block-subcoding';
import { BlockCodingResponse } from './interfaces/block-coding-response.interface';

export class BlockCoding {

    constructor(
        public id?: number,
        public name?: string,
        public icon?: string,
        public subcodings: Array<BlockSubcoding> = []
    ) { }

    static fromResponse(response: BlockCodingResponse): BlockCoding {
        let blockCoding = new BlockCoding(
            response.id,
            response.name,
            response.icon
        );
        response.subcodings.forEach(subcodingResponse => {
            blockCoding.subcodings.push(new BlockSubcoding(
                subcodingResponse.id,
                subcodingResponse.name,
                subcodingResponse.coding
            ));
        });
        return blockCoding;
    }
}