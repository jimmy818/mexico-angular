import { SubscriptionType } from 'sp-core';

import { Team } from './team.model';
import { InstitutionManager } from './institution-manager.model';

export class Institution {
    constructor(
        public id = 0,
        public name = '',
        public dbName = '',
        public type = SubscriptionType.trial,
        public expirationDate?: Date,   // Fecha de expiración del plan especificada para el tipo de usuario: Trial, Paying, Demo.
        public totalAthletes = 0,  // Total de atletas permitido según el tipo de usuario
        public totalCoaches = 0,   // Total de coaches permitido según el tipo de usuario

        /**
         * Total de equipos permitidos según el tipo de usuario. Para trial siempre será 1.
         */
        public totalTeams = 0,

        public total = 0,
        public tax = 0,
        public price = 0,
        public stripeFee = 0,

        public hasRenewable = false,
        public isActive = false,

        public team = new Team(),
        public managers: Array<InstitutionManager> = []
    ) { }
}