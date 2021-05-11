import { Team } from './team.interface';
import { Pagination } from './pagination.interface';

export interface Teams {
    data: Array<Team>;
    pagination: Pagination
}