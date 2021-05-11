export interface UserResponse {
    id: number;
    type: number,
    full_name: string;
    gender: number;
    email: string;
    institution: number;
    username: string;
    email_verified: boolean;
    is_active: boolean;
    heigth: number;
    weigth: number;
    photo?: string;
    region?: number,
    country_code?: number;
    phone?: string;
    birthday?: string;
}