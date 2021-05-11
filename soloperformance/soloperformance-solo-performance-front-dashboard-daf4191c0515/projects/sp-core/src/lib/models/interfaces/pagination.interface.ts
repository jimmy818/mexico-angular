import { PaginationLink } from './pagination-link.interface';

export interface Pagination {
    totalRows: number;
    perPage: number;
    currentPage: number;
    links: PaginationLink;
}