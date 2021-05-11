import { UserResponse } from './user-response.interface';
import { PaginationResponse } from './pagination-response.interface';

export interface UsersResponse {
    data: Array<UserResponse>;
    pagination: PaginationResponse
}