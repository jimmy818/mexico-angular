export interface SpCoreConfig {

    /**
     * Endpoint base de los servicios para autenticación/refresh token
     */
    apiBaseUrl: string;

    tokenUrl: string;

    refreshTokenUrl: string;

    userInfoUrl: string;

    forgotPasswordUrl: string;

    loginUrl: string;
}