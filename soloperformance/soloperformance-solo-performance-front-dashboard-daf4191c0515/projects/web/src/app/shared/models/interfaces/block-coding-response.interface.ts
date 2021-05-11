import { BlockSubcodingResponse } from './block-subcoding-response.interface';

export interface BlockCodingResponse {
    id: number;
    name: string;
    icon: string;
    subcodings: Array<BlockSubcodingResponse>;
}