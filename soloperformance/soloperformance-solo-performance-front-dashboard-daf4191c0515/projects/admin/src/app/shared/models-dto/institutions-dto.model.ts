import { InstitutionDto } from './institution-dto.model';
import { PaginationDto } from './pagination-dto.model';
import { ResponsePaginationDto } from './response-pagination-dto.model';

export interface InstitutionsDto extends ResponsePaginationDto {
    data: Array<InstitutionDto>;
    pagination: PaginationDto;
}