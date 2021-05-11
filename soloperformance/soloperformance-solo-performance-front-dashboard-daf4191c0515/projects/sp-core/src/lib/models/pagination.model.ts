import { PaginationResponse } from './interfaces/pagination-response.interface';
import { Pagination as IPagination } from './interfaces/pagination.interface';
import { PaginationLink } from './interfaces/pagination-link.interface';

export class Pagination {
    constructor() { }

    static mapToModel(response: PaginationResponse) {
        return <IPagination>{
            totalRows: response.total_rows,
            perPage: response.per_page,
            currentPage: response.current_page,
            links: <PaginationLink>{
                first: response.links.first,
                last: response.links.last,
                next: response.links.next,
                prev: response.links.prev
            }
        }
    }
}