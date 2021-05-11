import { User } from './user.interface';
import { Pagination } from './pagination.interface';

export interface Users {
    data: Array<User>;
    pagination: Pagination
}