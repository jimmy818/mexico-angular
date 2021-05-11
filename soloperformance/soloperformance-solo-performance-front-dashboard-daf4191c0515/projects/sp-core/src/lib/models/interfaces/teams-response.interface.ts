import { PaginationResponse } from './pagination-response.interface';

import { TeamResponse } from './team-response.interface';

export class TeamsResponse {
    data: Array<TeamResponse>;
    pagination: PaginationResponse
}