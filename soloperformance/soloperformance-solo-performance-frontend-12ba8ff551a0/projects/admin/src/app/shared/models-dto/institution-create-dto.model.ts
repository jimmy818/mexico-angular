export interface InstitutionCreateDto {
    name: string;
    active: boolean;
    identifier_name: string;
    type: number;
    ends: string;
    total_athletes: number;
    total_coaches: number;
    total_team: number;
    total: number;
    tax: number;
    price: number;
    fee_stripe: number;
    has_renewable: boolean;
}