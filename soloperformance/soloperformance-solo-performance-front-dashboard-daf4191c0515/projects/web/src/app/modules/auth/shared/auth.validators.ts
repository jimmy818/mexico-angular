import { FormGroup } from '@angular/forms';

export class AuthValidators {

    /**
     * Validador de confirmación de contraseña. 
     * @param g Formulario con los campos correspondientes: contraseña y confirmación.
     * Es necesario que los campos se llamen 'password' y 'passwordConfirm' respectivamente.
     */
    static confirmPassword(
        g: FormGroup
    ): { [key: string]: boolean } | null {

        const password = g.get('password').value;
        const confirmPassword = g.get('passwordConfirm').value;

        // Verifica que ambos tengan un valor.
        if (!password || !confirmPassword) {
            return null;
        }

        // Verifica si la contraseña y su confirmación corresponden.
        if (password === confirmPassword) {
            return null;
        }

        // Retorna que los campos no corresponden.
        return { 'match': true };
    }

}