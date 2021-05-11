import { DataResponse } from './data-response.interface';
import { AthleteResponse } from './athlete-response.interface';

export interface AthletesResponse extends DataResponse {
    data: Array<AthleteResponse>;
}