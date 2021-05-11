import { Component, Input, OnInit, ViewChild, AfterViewInit, AfterContentInit, OnDestroy } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { MatSelectionList } from '@angular/material/list';
import { Subject } from 'rxjs';
import { SubSink } from 'subsink';
import { finalize } from 'rxjs/operators';

import * as moment from 'moment';
import { DragScrollComponent } from 'ngx-drag-scroll';

import { Periodicity, ProgressSpinnerService, Athlete, Team, TeamService } from 'sp-core';
import { HeaderGroupAlignment } from 'sp-library';

import { EventService } from '@web/shared/services/event.service';
import { EventsComponent } from '@web/shared/components/events/events.component';
import { EventsDialogData } from '@web/shared/components/events/events-dialog-data.interface';
import { GridStackItemContent } from '../shared/models/interfaces/grid-stack-item-content.interface';
import { Widget } from '../shared/models/interfaces/widget.interface';
import { WidgetService } from '../shared/services/widget.service';
import { Filter } from './filter-value.interface';
import { EventSummary } from './event-summary.interface';
import { EventParams } from './event-params.interface';

@Component({
  selector: 'web-widget-main',
  templateUrl: './main-widget.component.html',
  styleUrls: ['./main-widget.component.scss']
})
export class MainWidgetComponent implements GridStackItemContent, OnInit, OnDestroy, AfterViewInit, AfterContentInit {

  @Input() widget: Widget;

  @ViewChild('teamList') teamList: MatSelectionList;

  @ViewChild('teamScroll', { read: DragScrollComponent }) teamScroll: DragScrollComponent;

  headerGroupAlignment = HeaderGroupAlignment;

  filters: Array<Filter> = [];
  filtersStats: Array<Filter> = [];
  eventsIsSelected = false;
  statsIsSelected = false;

  periodicity = Periodicity;
  selectedPeriodicity = Periodicity.week;
  periodicityDates: Array<Date> = [];

  teams: Array<Team> = [];
  selectedTeam: Team;

  athletes: Array<Athlete> = [];
  selectedAthlete: Athlete;

  selectedDate: Date = moment().toDate();

  exercisesNumberSelected = false;
  totalVolumeSelected = false;
  rpeSelected = false;
  preTrainingSurveySelected = false;
  sessionTimeSelected = false;

  leftBoundReached = false;
  rightBoundReached = false;

  events: Array<EventSummary> = [];

  private subsink = new SubSink();
  eventSubject = new Subject<EventParams>();

  get selectedTeamId(): number {
    return this.selectedTeam ? this.selectedTeam.id : null;
  }

  get selectedAthleteId(): number {
    return this.selectedAthlete ? this.selectedAthlete.id : null;
  }

  constructor(
    private iconRegistry: MatIconRegistry,
    private domSanitizer: DomSanitizer,
    private dialog: MatDialog,
    private spinnerService: ProgressSpinnerService,
    private eventService: EventService,
    private widgetService: WidgetService,
    private teamService: TeamService
  ) {
    this.iconRegistry.addSvgIcon('chevron-left', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/chevron-left.svg'));
    this.iconRegistry.addSvgIcon('chevron-right', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/chevron-right.svg'));
    this.iconRegistry.addSvgIcon('add', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/add.svg'));

    this.filters.push({ name: 'periods', text: 'Periods', selected: false, isIndividual: false });
    this.filters.push({ name: 'programs', text: 'Programs', selected: false, isIndividual: false });
    this.filters.push({ name: 'phases', text: 'Phases', selected: false, isIndividual: false });
    this.filters.push({ name: 'workouts', text: 'Workouts', selected: false, isIndividual: false });
    this.filters.push({ name: 'events', text: 'Events', selected: false, isIndividual: true });
    this.filters.push({ name: 'stats', text: 'Stats', selected: false, isIndividual: true });

    this.filtersStats.push({ name: 'exercisesNumber', text: 'Number of exercises', selected: false, isIndividual: true, selectedMax: 2 });
    this.filtersStats.push({ name: 'totalVolume', text: 'Total volume', selected: false, isIndividual: true, selectedMax: 2 });
    this.filtersStats.push({ name: 'rpe', text: 'RPE', selected: false, isIndividual: true, selectedMax: 2 });
    this.filtersStats.push({ name: 'preTrainingSurvey', text: 'Pre training survey', selected: false, isIndividual: true, selectedMax: 2 });
    this.filtersStats.push({ name: 'sessionTime', text: 'Session time', selected: false, isIndividual: true, selectedMax: 2 });
  }

  ngOnInit(): void {

    // TODO: Crear observables para cada cambio de atleta, equipo, filtros y escucharlos en conjunto para cada cambio de eventos.
    this.subsink.sink = this.eventSubject.subscribe(params => {
      if (this.eventsIsSelected) {
        let events: Array<EventSummary> = [];
        this.events = [];
        if (params.byYear) {
          events = [];
          this.spinnerService.start();
          this.eventService
            .getSummaryByYear(params.year, this.selectedTeamId, this.selectedAthleteId)
            .pipe(finalize(() => {
              this.spinnerService.stop();
            }))
            .subscribe(data => {
              data.forEach(event => {
                events.push({ date: moment(event.date).toDate(), count: event.events });
              });
              this.events = events;
            });
        } else {
          events = [];
          this.spinnerService.start();
          this.eventService
            .getSummaryByDates(params.dateBegin, params.dateEnd, this.selectedTeamId, this.selectedAthleteId)
            .pipe(finalize(() => {
              this.spinnerService.stop();
            }))
            .subscribe(data => {
              data.forEach(event => {
                events.push({ date: moment(event.date).toDate(), count: event.events });
              });
              this.events = events;
            });
        }
      }
    });

    this.getPeriodicityValues();

    // Obtiene la lista de equipos.
    this.spinnerService.start();
    this.teamService
      .getList()
      .pipe(
        finalize(() => {
          this.spinnerService.stop();
        }))
      .subscribe(response => {
        this.teams = response.data;
      });
  }

  ngOnDestroy(): void {
    this.subsink.unsubscribe();
  }

  ngAfterViewInit(): void {
    this.changeStatusFilter(this.filtersStats, this.filtersStats.filter(filter => filter.name === 'exercisesNumber')[0]);
  }

  ngAfterContentInit(): void {
  }

  onEventClick(event: EventSummary): void {
    const isMonth = this.selectedPeriodicity === Periodicity.year;
    this.spinnerService.start();
    this.eventService
      .getListByDate(event.date, isMonth, this.selectedTeamId, this.selectedAthleteId)
      .pipe(finalize(() => {
        this.spinnerService.stop();
      }))
      .subscribe(data => {
        this.dialog.open(EventsComponent,
          {
            maxWidth: '630px',
            data: <EventsDialogData>{
              date: event.date,
              isMonth: isMonth,
              events: data
            }
          });
      });
  }

  deleteWidget(): void {
    this.widgetService.requestRemoveWidgetFromUser(this.widget.gridStackItemId);
  }

  duplicateWidget(): void {
    this.widgetService.requestDuplicateWidgetFromUser(this.widget);
  }

  selectTeam(team: Team): void {
    this.selectedTeam = team;
    this.athletes = [];
    this.selectedAthlete = null;
    this.spinnerService.start();
    this.teamService
      .getAthletes(team.id)
      .pipe(finalize(() => {
        this.spinnerService.stop();
      }))
      .subscribe(data => {
        this.athletes = data;
        this.getEvents();
      });

  }

  selectAthlete(athlete: any): void {
    this.selectedAthlete = athlete;
    this.getEvents();
  }

  goToTeams(): void {
    this.selectedTeam = null;
    this.selectedAthlete = null;
    this.getEvents();
  }

  /**
   * Verifica si la fecha indicada corresponde a la fecha actual del sistema.
   * Se validan sólo las fechas para evitar problemas con la sección tiempo.
   * @param date Fecha a verificar si es la fecha actual.
   */
  checkCurrentDate(date: Date): boolean {
    return moment(date).format('YYYYMMDD') === moment().format('YYYYMMDD');
  }

  /**
   * Verifica si el mes de la fecha indicada corresponde al mes actual del sistema.
   * Se validan sólo a nivel año-mes
   * @param date Fecha a verificar si es del mes actual.
   */
  checkCurrentMonth(date: Date): boolean {
    return moment(date).format('YYYYMM') === moment().format('YYYYMM');
  }

  onPeriodicityClick(periodicity: Periodicity) {
    this.selectedPeriodicity = periodicity;
    this.getPeriodicityValues();
  }

  onFilterClick(filterClicked: Filter): void {
    this.changeStatusFilter(this.filters, filterClicked);
  }

  onDailyLoadFilterClick(filterClicked: Filter): void {
    this.changeStatusFilter(this.filtersStats, filterClicked);
  }

  prevMonth(): void {
    this.changeMonth(-1);
  }

  nextMonth(): void {
    this.changeMonth(1);
  }

  prevPeriodicity(): void {
    this.changePeriodicity(-1);
  }

  nextPeriodicity(): void {
    this.changePeriodicity(1);
  }

  goToMonth(date: Date): void {
    this.selectedDate = moment(this.selectedDate).month(date.getMonth()).date(1).toDate();
    this.selectedPeriodicity = Periodicity.month;
    this.getPeriodicityValues();
  }

  moveLeft() {
    this.teamScroll.moveLeft();
  }

  moveRight() {
    this.teamScroll.moveRight();
  }

  reachesLeftBound(reached: boolean): void {
    this.leftBoundReached = reached;
  }

  reachesRightBound(reached: boolean): void {
    this.rightBoundReached = reached;
  }

  private changeStatusFilter(
    filters: Array<Filter>,
    filterClicked: Filter
  ): void {

    // Des-selecciona todos los elementos previos. Siempre y cuando no sean individuales ni tampoco el actual.
    if (!filterClicked.isIndividual) {
      filters
        .filter(filter => !filter.isIndividual && filter.name !== filterClicked.name)
        .forEach(filter => {
          filter.selected = false;
        });
    }

    // Cambia el estatus del elemento actualmente seleccionado.
    filters
      .filter(filter => filter.name === filterClicked.name)
      .forEach(filter => {
        filter.selected = !filter.selected;
        setTimeout(() => {
          switch (filter.name) {
            case 'stats':
              // Si el filtro seleccionado es la opción de gráfica de estadística se actualiza el indicador para visualizar/ocultar la gráfica.
              this.statsIsSelected = filter.selected;
              break;
            case 'events':
              // Si el filtro seleccionado es la opción de eventos se actualiza el indicador para visualizar/ocultar los eventos
              this.eventsIsSelected = filter.selected;
              if (this.eventsIsSelected) {
                this.getEvents();
              }
              break;
            case 'exercisesNumber':
              this.exercisesNumberSelected = filter.selected;
              break;
            case 'totalVolume':
              this.totalVolumeSelected = filter.selected;
              break;
            case 'rpe':
              this.rpeSelected = filter.selected;
              break;
            case 'preTrainingSurvey':
              this.preTrainingSurveySelected = filter.selected;
              break;
            case 'sessionTime':
              this.sessionTimeSelected = filter.selected;
              break;
          }
        }, 0);
      });

    // Mantener seleccionados un máximo de N elementos.
    // 1.- Sólo aplica para filtros que tienen comportamiento individual. Los que funcionan en grupo como radiobutton no aplica un máximo.
    // 2.- Sólo si se tiene especificado un máximo de elementos a seleccionar a la vez.
    if (filterClicked.isIndividual && filterClicked.selectedMax) {
      const selectedFilters = filters.filter(filter => filter.selected);
      // maxOrder = selectedFilters.length permite recalcular el orden de selección (selectedOrder) cuando el número de filtros selecionados es menor al máximo permitido.
      let maxOrder = (selectedFilters.length > filterClicked.selectedMax) ? filterClicked.selectedMax : selectedFilters.length;
      // Asigna o desasigna el orden de selección según el estado del filtro.
      filterClicked.selectedOrder = filterClicked.selected ? selectedFilters.length : null;
      selectedFilters
        // Si está seleccionado pero no tiene especificado un orden de selección le coloca 0. Para los filtros que nacen seleccionados.
        .map(filter => {
          if (!filter.selectedOrder) {
            filter.selectedOrder = 0;
          }
          return filter;
        })
        // Ordena descendentement para mantener seleccionados únicamente los últimos N filtros seleccionados según el máximo indicado.
        .sort((a, b) => b.selectedOrder - a.selectedOrder)
        .forEach((filter, index) => {
          // Si el filtro se considera dentro del máximo de elementos a seleccionar se reasigna el orden de N...,2,1
          if (index < filterClicked.selectedMax) {
            filter.selectedOrder = maxOrder--;
          }
          // Se des-selecciona el elemento.
          else {
            filter.selected = false;
            filter.selectedOrder = null;
          }
        });
    }
  }

  private changeMonth(factor: number): void {
    this.selectedDate = moment(this.selectedDate).add(1 * factor, 'M').date(1).toDate();
    this.getPeriodicityValues();
  }

  private changePeriodicity(factor: number): void {
    switch (this.selectedPeriodicity) {
      case Periodicity.week:
        this.selectedDate = moment(this.selectedDate).add(1 * factor, 'w').toDate();
        break;
      case Periodicity.month:
        this.selectedDate = moment(this.selectedDate).add(1 * factor, 'M').date(1).toDate();
        break;
      case Periodicity.year:
        this.selectedDate = moment(this.selectedDate).add(1 * factor, 'y').date(1).toDate();
        break;
    }
    this.getPeriodicityValues();


  }

  private getPeriodicityValues(): void {

    this.periodicityDates = [];

    let momentDate = moment(this.selectedDate);

    switch (this.selectedPeriodicity) {

      // Obtiene los valores de periodicidad en base a la semana seleccionada.
      case Periodicity.week:
        const firstDayOfWeek = momentDate.weekday(0);
        for (let i = 0; i < 7; i++) {
          this.periodicityDates.push(moment(firstDayOfWeek).add(i, 'd').toDate());
        }
        break;

      // Obtiene los valores de periodicidad en base a los días correspondientes del mes seleccionado.
      case Periodicity.month:
        // Obtien fecha correspondiente a último día del mes de la fecha seleccionada.
        const endOfMonth = momentDate.endOf('month');
        for (let i = endOfMonth.date() - 1; i >= 0; i--) {
          this.periodicityDates.push(moment(endOfMonth).add(-i, 'd').toDate());
        };
        break;

      // Obtiene los valores de períodicidad de 1 año
      case Periodicity.year:
        for (let i = 0; i < 12; i++) {
          this.periodicityDates.push(momentDate.month(i).date(1).toDate());
        }
        break;
    }

    this.getEvents();
  }

  private getEvents(): void {
    // Existe un cambio de periodicidad, por lo que se solicita obtener la información de bd.
    if (this.selectedPeriodicity === Periodicity.year) {
      this.eventSubject.next({
        byYear: true,
        year: this.periodicityDates[0].getFullYear()
      });
    } else if (this.periodicityDates.length) {
      this.eventSubject.next({
        byYear: false,
        dateBegin: this.periodicityDates[0],
        dateEnd: this.periodicityDates[this.periodicityDates.length - 1]
      });
    }
  }
}
