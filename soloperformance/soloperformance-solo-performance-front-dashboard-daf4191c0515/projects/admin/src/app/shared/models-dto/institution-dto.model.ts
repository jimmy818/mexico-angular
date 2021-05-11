import { SubscriptionDto } from './subscription-dto.model';

export interface InstitutionDto {
    id: number;
    name: string;
    identifier_name: string;
    created_at: Date;
    updated_at: Date;
    revanue: number;
    active: boolean;
    subscription: SubscriptionDto;
}