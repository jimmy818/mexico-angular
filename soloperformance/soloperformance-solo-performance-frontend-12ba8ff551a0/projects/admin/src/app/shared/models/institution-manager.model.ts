import { Gender } from 'sp-core';

export class InstitutionManager {
    constructor(
        public name = '',
        public lastname = '',
        public email = '',
        public phone = '',
        public password = '',
        public passwordConfirm = '',
        public gender?: Gender,
        public birthdate?: Date
    ) { }
}