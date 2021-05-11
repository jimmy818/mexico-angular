export interface UserCreateDto {
    full_name: string;
    email: string;
    phone: string;
    gender: number;
    birthdate: string;
    password: string;
    confirm_password: string;
    country_code: number;
    photo: string;
    type: number;
    region: number;
    team: number;
    institution: number;
}