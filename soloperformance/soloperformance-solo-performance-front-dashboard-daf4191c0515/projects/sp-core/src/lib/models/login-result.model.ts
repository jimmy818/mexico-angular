import { UserInfo } from './interfaces/user-info.interface';

export class LoginResult {
    constructor(
        public isAuthenticated = false,
        public username?: string,
        public redirectUrl?: string,
        /**
         * Obtiene o establece el mensaje de error para visualizar al usuario. Mensaje amigable.
         */
        public messageError?: string,
        /**
         * Obtiene o establece la excepción devuelva por el api. Mensaje para uso interno
         */
        public exceptionError?: string
    ) { }
}
