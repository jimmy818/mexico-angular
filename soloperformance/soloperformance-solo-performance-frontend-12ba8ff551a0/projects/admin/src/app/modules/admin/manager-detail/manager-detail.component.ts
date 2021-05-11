import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSelectChange } from '@angular/material/select';
import { map, mergeMap } from 'rxjs/operators';
import * as moment from 'moment';

import { SubscriptionType } from 'sp-core';

import { Team } from '@admin/shared/models/team.model';
import { UtilitiesService } from '@admin/core/services/utilities.service';
import { Institution } from '@admin/shared/models/institution.model';
import { AuthValidators } from '@admin/modules/auth/shared/auth.validators';
import { InstitutionManager } from '@admin/shared/models/institution-manager.model';

import { CONTROL_NAMES } from './control-names.constants';
import { InstitutionService } from '../shared/services/institution.service';
import { ManagerData } from '../shared/models/manager-data.model';
import { InstitutionManagerService } from '../shared/services/institution-manager.service';
import { TeamService } from '../shared/services/team.service';

@Component({
  selector: 'admin-manager-detail',
  templateUrl: './manager-detail.component.html',
  styleUrls: ['./manager-detail.component.scss']
})
export class ManagerDetailComponent implements OnInit {

  withInstitutionData = false;
  institutionId = 0;
  title = '';

  controlNames = CONTROL_NAMES;

  form: FormGroup;

  subscriptionType = SubscriptionType;

  subscriptionTypes: Array<SubscriptionType> = [
    SubscriptionType.trial,
    SubscriptionType.paying,
    SubscriptionType.demo
  ]

  get institutionForm(): FormGroup {
    return this.form.get('institution') as FormGroup;
  }

  get teamForm(): FormGroup {
    return this.form.get('institution.team') as FormGroup;
  }

  get managerForm(): FormGroup {
    return this.form.get('manager') as FormGroup;
  }

  get authForm(): FormGroup {
    return this.form.get('manager.auth') as FormGroup;
  }

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<ManagerDetailComponent>,
    private snackBar: MatSnackBar,
    private userService: InstitutionService,
    private teamService: TeamService,
    private managerService: InstitutionManagerService,
    @Inject(MAT_DIALOG_DATA) private data: ManagerData
  ) {
    this.institutionId = data.institutionId;
    this.withInstitutionData = !this.institutionId; // Si se envía ID de institución no debe pedir datos de institución.
    this.title = this.withInstitutionData ? 'New User' : 'New Institution Manager';
    this.createForm();
  }

  ngOnInit(): void {
  }

  genderChange(matSelect: MatSelectChange) {
    this.managerForm.get(this.controlNames.managerGender).setValue(matSelect.value);
  }

  save() {
    // Si se indicó que se requiere datos de institución entonces se crea un institution, team, institution manager.
    if (this.withInstitutionData) {
      this.createInstitution();
    } else {
      // En caso contrario sólo se crea un institution manager.
      this.createManager();
    }
  }

  /**
   * Crea la institución, así como un equipo y un administrador predeterminados.
   */
  private createInstitution(): void {

    // Verifica que la información del formulario esté correcto antes de proceder
    if (this.form.invalid) {
      return;
    }

    // Realiza el mapeo de los campos de formulario a los modelos
    const institution = this.mapFormToInstitution();
    const team = this.mapFormToTeam();
    const manager = this.mapFormToManager();

    // Envía a crear la institución
    this.userService
      .create(institution)
      .pipe(mergeMap(institutionResponse => {
        // Envía a crear el equipo
        return this.teamService
          .create(team, institutionResponse.id)
          .pipe(mergeMap(teamResponse => {
            // Envía a crear al administrador de la institución
            return this.managerService
              .create(manager, teamResponse.id, institutionResponse.id)
              .pipe(map(managerResponse => {
                institutionResponse.team = teamResponse;
                institutionResponse.manager = managerResponse;
                return institutionResponse;
              }));
          }));
      }))
      .subscribe(institutionResponse => {
        console.log(institutionResponse);
        this.dialogRef.close(institutionResponse);
      }, (error) => {
        this.snackBar.open(error.error.errors, 'Error', {
          duration: 5000,
          horizontalPosition: 'center',
          verticalPosition: 'bottom',
        });
      }, () => {
        // TODO: Detener spinner.
        //console.log('Completo');
      });
  }

  /**
   * Crea un administrador de institución
   */
  private createManager(): void {

    // Verifica que la información del formulario esté correcto antes de proceder
    if (this.form.invalid) {
      return;
    }

    // Realiza el mapeo de los campos de formulario a los modelos
    const manager = this.mapFormToManager();

    // Envía a crear un administrador de la institución seleccionada.
    this.managerService
      .create(manager, null, this.institutionId)
      .subscribe(institutionResponse => {
        console.log(institutionResponse);
        this.dialogRef.close(institutionResponse);
      }, (error) => {
        this.snackBar.open(error.error.errors, 'Error', {
          duration: 5000,
          horizontalPosition: 'center',
          verticalPosition: 'bottom',
        });
      }, () => {
        // TODO: Detener spinner.
        //console.log('Completo');
      });
  }

  private createForm() {

    this.form = this.fb.group({});

    // Sólo agrega el grupo de institución si se indicó que se requiere.
    // Aplica para cuando la pantalla se llama desde la creación de una nueva institución/usuario.
    if (this.withInstitutionData) {
      this.form.addControl('institution', this.createInstitutionForm());
    }

    this.form.addControl('manager', this.createManagerForm());
  }

  private createInstitutionForm(): FormGroup {

    const institutionGroup = this.fb.group({});

    const institutionNameCtrl = this.fb.control(null, [Validators.required]);
    institutionNameCtrl.valueChanges.subscribe(value => {
      this.teamForm.get(this.controlNames.teamName).setValue(value);
    });
    institutionGroup.addControl(this.controlNames.institutionName, institutionNameCtrl);

    const institutionDbNameCtrl = this.fb.control(null);
    institutionGroup.addControl(this.controlNames.institutionDbName, institutionDbNameCtrl);

    const institutionTypeCtrl = this.fb.control(null, [Validators.required]);
    institutionTypeCtrl.setValue(SubscriptionType.trial);
    institutionGroup.addControl(this.controlNames.institutionType, institutionTypeCtrl);

    const teamGroup = this.fb.group({});
    const teamNameCtrl = this.fb.control({ value: null, disabled: true });
    teamGroup.addControl(this.controlNames.teamName, teamNameCtrl);
    institutionGroup.addControl('team', teamGroup);

    return institutionGroup;
  }

  private createManagerForm(): FormGroup {

    const managerGroup = this.fb.group({});

    const managerNameCtrl = this.fb.control(null, [Validators.required]);
    managerGroup.addControl(this.controlNames.managerName, managerNameCtrl);

    const managerLastnameCtrl = this.fb.control(null, [Validators.required]);
    managerGroup.addControl(this.controlNames.managerLastname, managerLastnameCtrl);

    const managerEmailCtrl = this.fb.control(null, [Validators.required, Validators.email]);
    managerGroup.addControl(this.controlNames.managerEmail, managerEmailCtrl);

    const managerPhoneCtrl = this.fb.control(null, [Validators.maxLength(10), Validators.required, Validators.pattern(/^-?(0|[1-9]\d*)?$/)]);
    managerGroup.addControl(this.controlNames.managerPhone, managerPhoneCtrl);

    const managerGenderCtrl = this.fb.control(null, [Validators.required]);
    //managerGenderControl.setValue(GenderEnum.other);
    managerGroup.addControl(this.controlNames.managerGender, managerGenderCtrl);

    const managerBirthdateCtrl = this.fb.control(null);
    managerGroup.addControl(this.controlNames.managerBirthdate, managerBirthdateCtrl);

    // ==================================
    // = Grupo de contraseñas
    // ==================================

    const authGroup = this.fb.group({});

    const passwordCtrl = this.fb.control(null, [Validators.required, Validators.minLength(8)]);
    authGroup.addControl(this.controlNames.password, passwordCtrl);

    const passwordConfirmCtrl = this.fb.control(null, [Validators.required]);
    authGroup.addControl(this.controlNames.passwordConfirm, passwordConfirmCtrl);

    authGroup.setValidators(AuthValidators.confirmPassword);

    managerGroup.addControl('auth', authGroup);

    return managerGroup;
  }

  private mapFormToInstitution(): Institution {

    let institution = new Institution();
    institution.name = this.institutionForm.get(this.controlNames.institutionName).value;

    institution.dbName = UtilitiesService.getDbName(this.institutionForm.get(this.controlNames.institutionName).value);
    institution.type = this.institutionForm.get(this.controlNames.institutionType).value;

    // Opciones según tipo de usuario.
    if (institution.type === SubscriptionType.trial) {
      // Fecha de expiración
      let currentDate = moment();
      institution.expirationDate = currentDate.add(14, 'days').toDate();
      // Total de equipos.
      institution.totalTeams = 1;
    } else {
      // TODO: Consultar si se capturará
      institution.totalTeams = 10;
    }

    // TODO: Verificar lógica de negocio
    institution.totalAthletes = 10;
    institution.totalCoaches = 10;

    institution.hasRenewable = false;
    institution.isActive = true;

    return institution;
  }

  private mapFormToTeam(): Team {
    const team = new Team();
    team.name = this.teamForm.get(this.controlNames.teamName).value;
    return team;
  }

  private mapFormToManager(): InstitutionManager {

    const manager = new InstitutionManager();

    manager.name = this.managerForm.get(this.controlNames.managerName).value;
    manager.lastname = this.managerForm.get(this.controlNames.managerLastname).value;
    manager.email = this.managerForm.get(this.controlNames.managerEmail).value;
    manager.phone = this.managerForm.get(this.controlNames.managerPhone).value;
    manager.gender = this.managerForm.get(this.controlNames.managerGender).value;

    const birthdate = this.managerForm.get(this.controlNames.managerBirthdate).value;
    if (birthdate) {
      manager.birthdate = birthdate;
    } else {
      manager.birthdate = moment().toDate();
    }

    manager.password = this.authForm.get(this.controlNames.password).value;
    manager.passwordConfirm = this.authForm.get(this.controlNames.passwordConfirm).value;

    return manager;
  }
}
