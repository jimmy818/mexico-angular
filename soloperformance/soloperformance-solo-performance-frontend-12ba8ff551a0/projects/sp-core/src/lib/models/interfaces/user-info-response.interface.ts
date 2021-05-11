export interface UserInfoResponse {
    id: number;
    type: number;
    region: number;
    full_name: string;
    country_code: number;
    phone: string;
    gender: number;
    birthday: string;
    photo: string;
    email: string;
    team: number;
    institution: number;
    username: string;
    email_verified: boolean;
    subscription_active: boolean;
    is_active: boolean;
}