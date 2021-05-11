export interface UserPostRequest {
    type: number;
    full_name: string;
    email: string;
    password: string;
    confirm_password: string;
    country_code: number;
    phone: string;
    birthday: string;
    photo?: string;
    region: number;
    gender: number;
    heigth?: number;
    weigth?: number;
    team?: number;
    institution: number;
}