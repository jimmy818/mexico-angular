export interface SubscriptionDto {
    id: string;
    type: string;
    ends: Date;
    is_active: boolean;
    total_athletes: number;
    total_coaches: number;
    total_team: number;
    price: number;
    tax: number;
    fee_stripe: number;
    total: number;
    has_renewable: boolean;
    created_at: Date;
    updated_at: Date;
}