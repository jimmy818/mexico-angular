import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { FormGroup, FormBuilder, FormArray } from '@angular/forms';
import { forkJoin } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { MatSelectionList } from '@angular/material/list';
import { MatCheckboxChange } from '@angular/material/checkbox';

import { ProgressSpinnerService } from 'sp-core';

import { BlockCoding } from '@web/shared/models/block-coding';
import { BlockType } from '@web/shared/models/block-type';
import { WorkoutService } from '@web/shared/services/workout.service';

interface Athlete {
  id: number;
  name: string;
  photo: string;
  selected: boolean;
}

@Component({
  selector: 'web-workout-add',
  templateUrl: './workout-add.component.html',
  styleUrls: ['./workout-add.component.scss']
})
export class WorkoutAddComponent implements OnInit {

  @ViewChild('athletesList') athletesList: MatSelectionList;

  workoutForm: FormGroup;

  categories: Array<BlockCoding> = [];

  blockTypes: Array<BlockType> = [];

  exercisesNumbers: Array<number> = [1, 2, 3, 4, 5, 6];

  athletes: Array<Athlete> = [];
  filteredAthletes: Array<Athlete> = [];

  selectedBlock: FormGroup;
  hoveredBlock: any;

  selectAllAthletesChecked = false;

  searchAthleteValue = '';

  get categoriesForm(): FormArray {
    return this.workoutForm.get('categories') as FormArray;
  }

  get selectedBlockAthletes(): Array<Athlete> {
    return this.selectedBlock.get('athletes').value as Array<Athlete>;
  }

  private timeout: any;

  constructor(
    private fb: FormBuilder,
    private spinnerService: ProgressSpinnerService,
    private workoutService: WorkoutService
  ) {
    this.createForm();
  }

  ngOnInit(): void {

    // TODO: Obtener los atletas cuando se tenga el flujo de filtrar por equipo y atletas asignados a un programa.
    this.athletes.push({ id: 1, name: 'Athlete 1', photo: 'assets/images/example-athlete-photo-1.svg', selected: false });
    this.athletes.push({ id: 2, name: 'Athlete 2', photo: 'assets/images/example-athlete-photo-2.svg', selected: false });
    this.athletes.push({ id: 3, name: 'Athlete 3', photo: 'assets/images/example-athlete-photo-1.svg', selected: false });
    this.athletes.push({ id: 4, name: 'Athlete 4', photo: 'assets/images/example-athlete-photo-2.svg', selected: false });
    this.athletes.push({ id: 5, name: 'Athlete 5', photo: 'assets/images/example-athlete-photo-1.svg', selected: false });
    this.athletes.push({ id: 6, name: 'Athlete 6', photo: 'assets/images/example-athlete-photo-2.svg', selected: false });
    this.athletes.push({ id: 7, name: 'Athlete 7', photo: 'assets/images/example-athlete-photo-1.svg', selected: false });
    this.athletes.push({ id: 8, name: 'Athlete 8', photo: 'assets/images/example-athlete-photo-2.svg', selected: false });
    this.athletes.push({ id: 9, name: 'Athlete 9', photo: 'assets/images/example-athlete-photo-1.svg', selected: false });
    this.athletes.push({ id: 9, name: 'Athlete 10', photo: 'assets/images/example-athlete-photo-2.svg', selected: false });

    this.filteredAthletes = this.copyAthletes();

    this.spinnerService.start();
    forkJoin([
      this.workoutService.getBlockCodings(),
      this.workoutService.getBlockTypes()
    ]).pipe(
      finalize(() => {
        this.spinnerService.stop();
      })
    ).subscribe(data => {
      this.categories = data[0];
      this.blockTypes = data[1];
    });

  }

  addBlock(category: BlockCoding): void {

    let index = this.categoriesForm.controls.findIndex(categoryForm => categoryForm.get('id').value === category.id);

    let categoryForm: FormGroup;
    if (index !== -1) {
      categoryForm = <FormGroup>this.categoriesForm.at(index);
    }
    if (!categoryForm) {
      categoryForm = this.createCategoryForm(category);
      this.categoriesForm.push(categoryForm);
    }
    (<FormArray>(categoryForm.get('blocks'))).push(this.createBlockForm());
  }

  mouseoverBlock(block: any): void {
    this.hoveredBlock = block;
  }

  mouseoutBlock(): void {
    this.hoveredBlock = null;
  }

  selectBlock(block: FormGroup): void {

    if (this.selectedBlock === block) {
      return;
    }

    this.searchAthleteValue = '';

    this.selectedBlock = block;
    setTimeout(() => {
      this.filterAthletes();
    }, 0);
  }

  removeBlock(categoryIdx: number, blockIdx: number): void {

    let blocksArray = this.categoriesForm.at(categoryIdx).get('blocks') as FormArray;

    // Des-asigna el bloque si se trata del que se está eliminando.
    if (this.selectedBlock === blocksArray.at(blockIdx)) {
      this.selectedBlock = null;
    }

    // Verifica si existe más de 1 bloque en la categoría, para sólo eliminar el bloque.
    if (blocksArray.length > 1) {
      blocksArray.removeAt(blockIdx);
    }
    // Si solo existe 1 registro de bloque elimina toda la categoría.
    else {
      this.categoriesForm.removeAt(categoryIdx);
    }
  }

  /**
   * Realiza el fitlrado de los atletas que correspondan con el texto capturada
   * @param value Texto o cadena a filtrar
   */
  onInputSearchValueChange(value: string): void {
    this.searchAthleteValue = value;
    if (this.timeout) {
      clearTimeout(this.timeout);
    }
    this.timeout = setTimeout(() => {
      this.filterAthletes(value);
    }, 250);
  }

  /**
   * Acciones a realizar por cada cambio en el checkbox de seleccionar todo.
   * @param change Datos de checkbox
   */
  onAthletesSelectAll(change: MatCheckboxChange): void {
    if (change.checked) {
      this.athletesList.selectAll();
    } else {
      this.athletesList.deselectAll();
    }
    this.assignUnassignAthletesToBlock();
  }

  /**
   * Acciones a realizar por cada cambio en la selección de atletas en la lista
   */
  onAthleteListSelectionChange(): void {
    this.assignUnassignAthletesToBlock();
  }

  private filterAthletes(value?: string): void {
    // Filtra los atletas según el campo de búsqueda.
    let filteredAthletes: Array<Athlete>;
    if (value) {
      filteredAthletes = this.copyAthletes().filter(athlete => athlete.name.toLowerCase().indexOf(value.toLowerCase()) !== -1);
    } else {
      filteredAthletes = this.copyAthletes();
    }
    // Selecciona los atletas asignados al bloque.
    this.selectedBlockAthletes.forEach(blockAthlete => {
      const athletesFound = filteredAthletes.filter(athlete => athlete.id === blockAthlete.id);
      if (athletesFound.length) {
        athletesFound[0].selected = true;
      }
    });
    this.filteredAthletes = filteredAthletes;
    setTimeout(() => {
      this.setSelectAllChecked();
    }, 0);
  }

  onCreateClick():void{
    
  }

  private copyAthletes(): Array<Athlete> {
    return JSON.parse(JSON.stringify(this.athletes)) as Array<Athlete>;
  }

  private assignUnassignAthletesToBlock(): void {
    if (!this.selectedBlock) {
      return;
    }
    // 
    this.setSelectAllChecked();
    // Atletas asignados al bloque.
    const selectedBlockAthletes = this.selectedBlockAthletes;
    // Agrega o elimina atletas asignados al bloque según la selección actual de los atletas filtrados en la lista.
    this.athletesList.options.forEach(option => {
      const athleteOption = option.value as Athlete;
      const athleteFound = selectedBlockAthletes.filter(athlete => athlete.id === athleteOption.id);
      // Si el atleta está seleccionado en la lista se agrega. 
      // Siempre y cuando no esté ya agregado.
      if (option.selected) {
        if (!athleteFound.length) {
          selectedBlockAthletes.push(athleteOption);
        }
      }
      // Si el atleta en la lista NO está seleccionado se elimina de los atletas asignados al bloque.
      // Siempre y cuando esté asignado al atleta.
      else {
        if (athleteFound.length) {
          const index = selectedBlockAthletes.indexOf(athleteFound[0]);
          selectedBlockAthletes.splice(index, 1);
        }
      }
    });
  }

  private setSelectAllChecked(): void {
    this.selectAllAthletesChecked = this.athletesList.selectedOptions.selected.length === this.filteredAthletes.length;
  }

  private createForm(): void {
    this.workoutForm = this.fb.group({});

    const categoriesForm = this.fb.array([]);
    this.workoutForm.addControl('categories', categoriesForm);
  }

  private createCategoryForm(category: BlockCoding): FormGroup {

    let categoryForm = this.fb.group({});

    const idCtrl = this.fb.control(category.id);
    categoryForm.addControl('id', idCtrl);

    const nameCtrl = this.fb.control(category.name);
    categoryForm.addControl('name', nameCtrl);

    const iconCtrl = this.fb.control(category.icon);
    categoryForm.addControl('icon', iconCtrl);

    const subcodingsCtrl = this.fb.control(category.subcodings);
    categoryForm.addControl('subcodings', subcodingsCtrl);

    const blocksCtrl = this.fb.array([]);
    categoryForm.addControl('blocks', blocksCtrl);

    return categoryForm;
  }

  private createBlockForm(): FormGroup {

    let blockForm = this.fb.group({});

    const idCtrl = this.fb.control(null);
    blockForm.addControl('id', idCtrl);

    const athletesCtrl = this.fb.control([]);
    blockForm.addControl('athletes', athletesCtrl);

    const exercisesNumberCtrl = this.fb.control(null);
    blockForm.addControl('exercisesNumber', exercisesNumberCtrl);

    return blockForm;
  }
}
