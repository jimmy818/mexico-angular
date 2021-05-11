import { TeamCreateResponseDto } from './team-create-response-dto.model';
import { UserCreateResponseDto } from './user-create-response-dto.model';

export interface InstitutionCreateResponseDto {
    id: number;
    name: string;
    identifier_name: string;
    created_at: Date;
    updated_at: Date;
    revanue: number;
    active: boolean;
    // Variables que no retorna el servicio de creación de instituciones. Se complementan con otros servicio.
    manager: UserCreateResponseDto;
    team: TeamCreateResponseDto;
}