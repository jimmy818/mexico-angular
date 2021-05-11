import { AfterViewInit, Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

import { Chart } from 'chart.js';
import { HeaderGroupAlignment } from 'sp-library';

import { AdminChart } from '@admin/shared/enums/admin-chart.enum';
import { Periodicity } from '@admin/shared/enums/periodicity.enum';
import { SelectItem } from '@admin/shared/models/select-item.model';
import { InstitutionDto } from '@admin/shared/models-dto/institution-dto.model';
import { InstitutionDetailResponse } from '@admin/shared/models-dto/institution-detail-response.model';

import { InstitutionService } from '../shared/services/institution.service';
import { ManagerDetailComponent } from '../manager-detail/manager-detail.component';
import { ManagerData } from '../shared/models/manager-data.model';

@Component({
  selector: 'admin-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, AfterViewInit {

  selectedInstitution: InstitutionDto;

  institutionDetail: InstitutionDetailResponse;

  headerGroupAlignment = HeaderGroupAlignment;
  adminChart = AdminChart;

  currentChart = AdminChart.newUsers;

  adminChartData: any = [];
  adminChartContext: CanvasRenderingContext2D;
  adminChartBackground: CanvasGradient;
  averageRevenueChartPeriodicity: Periodicity;

  totalRevenueChart: any = [];
  totalRevenueChartContext: CanvasRenderingContext2D;
  totalRevenueChartPeriodicity: Periodicity;

  totalUsersChart: any = [];
  totalUsersChartContext: CanvasRenderingContext2D;
  totalUsersChartPeriodicity: Periodicity;

  activeUsersChart: any = [];
  activeUsersChartContext: CanvasRenderingContext2D;
  activeUsersChartPeriodicity: Periodicity;

  churnedCustomersChart: any = [];
  churnedCustomersChartContext: CanvasRenderingContext2D;
  churnedCustomersChartPeriodicity: Periodicity;

  periodicity: Array<SelectItem> = [
    { value: Periodicity.weekly, text: 'Weekly' },
    { value: Periodicity.monthly, text: 'Monthly' },
    { value: Periodicity.yearly, text: 'Yearly' }
  ];

  constructor(
    private domSanitizer: DomSanitizer,
    private matIconRegistry: MatIconRegistry,
    private dialog: MatDialog,
    private institutionService: InstitutionService
  ) {
    this.matIconRegistry.addSvgIcon('trash', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/trash.svg'));
    this.matIconRegistry.addSvgIcon('password', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/password.svg'));
    this.matIconRegistry.addSvgIcon('edit', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/edit.svg'));
    this.matIconRegistry.addSvgIcon('back', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/keyboard-backspace.svg'));
    this.matIconRegistry.addSvgIcon('account', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/account-circle-outline.svg'));
    this.matIconRegistry.addSvgIcon('manager', this.domSanitizer.bypassSecurityTrustResourceUrl('assets/icons/account-circle-outline.svg'));

    // Configuraciones de gráficas.
    Chart.defaults.global.defaultFontFamily = "'Caros', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif";
    Chart.defaults.global.defaultFontSize = 12;
    Chart.defaults.global.defaultFontColor = '#A8ABB9';

    let periodicity = <Periodicity>this.periodicity.find(p => p.value == Periodicity.monthly).value;
    this.averageRevenueChartPeriodicity = this.totalRevenueChartPeriodicity = this.totalUsersChartPeriodicity = this.activeUsersChartPeriodicity = this.churnedCustomersChartPeriodicity = periodicity;
  }

  ngOnInit(): void {

    // Reporte administrativo
    const canvas = (<HTMLCanvasElement>document.getElementById("adminChartCanvas"))
    canvas.height = 100;
    this.adminChartContext = canvas.getContext("2d");
    this.adminChartBackground = this.adminChartContext.createLinearGradient(0, 0, 0, canvas.height * 4);
    this.adminChartBackground.addColorStop(0, "#6993FF");
    this.adminChartBackground.addColorStop(1, "rgba(105, 147, 255, 0.2)");

    // Visualiza por defecto el reporte de usuarios.
    this.showTrackingChart(AdminChart.newUsers);


    const canvasR2 = (<HTMLCanvasElement>document.getElementById("totalMontlyRevenueChart"));
    canvasR2.height = 250;
    this.totalRevenueChartContext = canvasR2.getContext("2d");
    this.showAdminChartSecondary(AdminChart.totalRevenue, Periodicity.monthly);

    const canvasR3 = (<HTMLCanvasElement>document.getElementById("totalUsersChart"));
    canvasR3.height = 250;
    this.totalUsersChartContext = canvasR3.getContext("2d");
    this.loadTotalUsersChart(Periodicity.monthly);

    const canvasR4 = (<HTMLCanvasElement>document.getElementById("montlyActiveUsersChart"));
    canvasR4.height = 250;
    this.activeUsersChartContext = canvasR4.getContext("2d");
    this.showAdminChartSecondary(AdminChart.activeUsers, Periodicity.monthly);

    const canvasR5 = (<HTMLCanvasElement>document.getElementById("churnedCustomersChart"));
    canvasR5.height = 250;
    this.churnedCustomersChartContext = canvasR5.getContext("2d");
    this.showAdminChartSecondary(AdminChart.churnedCustomers, Periodicity.monthly);
  }

  ngAfterViewInit() { }

  selectPeriodicity(chart: AdminChart, $event: any): void {
    this.showAdminChartSecondary(chart, $event.value);
  }

  selectAverageRevenueChart($event: any) {
    let periodicity = $event.value;
    switch (periodicity) {
      case Periodicity.weekly:
        this.showTrackingChart(AdminChart.averageWeeklyRevenue);
        break;
      case Periodicity.monthly:
        this.showTrackingChart(AdminChart.averageMonthlyRevenue);
        break;
      case Periodicity.yearly:
        this.showTrackingChart(AdminChart.averageYearlyRevenue);
        break;
    }
  }

  showTrackingChart(chart: AdminChart): void {

    this.currentChart = chart;

    let data: Array<number> = [];
    for (let index = 0; index < 12; index++) {
      data.push(Math.ceil(Math.random() * 100));
    }

    this.adminChartData = new Chart(this.adminChartContext, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
          {
            label: 'Data',
            fill: true,
            data: data,
            backgroundColor: this.adminChartBackground,
            borderColor: '#6993FF'
          }
        ]
      },
      options: {
        legend: {
          display: false,
          labels: {
            fontColor: '#000000'
          }
        },
        scales: {
          xAxes: [{
            display: true,
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            display: true
          }],
        }
      }
    });
  }

  addNewUser() {
    const dialogRef = this.dialog.open(ManagerDetailComponent, {
      width: '600px',
      disableClose: true,
      data: <ManagerData>{
        institutionId: null
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      // Si no se obtuvo respuesta no procede con las acciones.
      if (!result) {
        return;
      }
      this.selectedInstitution = null;
      // TODO: Envíar notificación de que se requiere actualizar la lista de instituciones.
    });
  }

  addNewManager() {
    const dialogRef = this.dialog.open(ManagerDetailComponent, {
      width: '600px',
      disableClose: true,
      data: <ManagerData>{
        institutionId: this.selectedInstitution.id
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      // Si no se obtuvo respuesta no procede con las acciones.
      if (!result) {
        return;
      }
      // Obtiene información actualizada de la institución.
      this.getInstitutionDetail(this.selectedInstitution);
    });
  }

  /**
   * Visualiza el detalle de la institución seleccionada.
   * @param institution Institución a mostrar su detalle
   */
  showUserDetail(institution: InstitutionDto): void {
    this.selectedInstitution = institution;
    this.getInstitutionDetail(institution);
  }

  hideUserDetail() {
    this.selectedInstitution = null;
  }

  editUser(user: InstitutionDto): void {
    console.log(user);
  }

  private showAdminChartSecondary(
    chart: AdminChart,
    periodicity: Periodicity
  ): void {

    let data1: Array<number> = [];
    data1.push(Math.ceil(Math.random() * 100));
    data1.push(Math.ceil(Math.random() * 100));
    data1.push(Math.ceil(Math.random() * 100));
    data1.push(Math.ceil(Math.random() * 100));

    let data2: Array<number> = [];
    data2.push(Math.ceil(Math.random() * 100));
    data2.push(Math.ceil(Math.random() * 100));
    data2.push(Math.ceil(Math.random() * 100));
    data2.push(Math.ceil(Math.random() * 100));

    let data3: Array<number> = [];
    data3.push(Math.ceil(Math.random() * 100));
    data3.push(Math.ceil(Math.random() * 100));
    data3.push(Math.ceil(Math.random() * 100));
    data3.push(Math.ceil(Math.random() * 100));

    let data: Chart.ChartConfiguration = {
      type: 'bar',
      data: {
        labels: ['Week1', 'Week2', 'Week3', 'Week 4'],
        datasets: [{
          label: "Value A",
          type: "bar",
          stack: "Base",
          backgroundColor: "#F24D60",
          barThickness: 8,
          data: data1,
        }, {
          label: "Value B",
          type: "bar",
          stack: "Base",
          backgroundColor: "#6993FF",
          barThickness: 8,
          data: data2,
        }, {
          label: "Value C",
          type: "bar",
          stack: "Base",
          backgroundColor: "#1BC5BD",
          barThickness: 8,
          data: data3,
        }]
      },
      options: {
        legend: {
          position: 'bottom',
          labels: {
            boxWidth: 12,
            fontColor: '#000000',
            fontFamily: 'Caros Bold'
          }
        },
        scales: {
          xAxes: [{
            stacked: true,
            ticks: {
              beginAtZero: true,
              maxRotation: 0,
              minRotation: 0
            },
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            stacked: true,

          }]
        },
      }
    };

    switch (chart) {
      case AdminChart.totalRevenue:
        this.totalRevenueChart = new Chart(this.totalRevenueChartContext, data);
        break;
      case AdminChart.totalUsers:
        this.totalUsersChart = new Chart(this.totalUsersChartContext, data);
        break;
      case AdminChart.activeUsers:
        this.activeUsersChart = new Chart(this.activeUsersChartContext, data);
        break;
      case AdminChart.churnedCustomers:
        this.churnedCustomersChart = new Chart(this.churnedCustomersChartContext, data);
        break;
    }
  }

  private loadTotalUsersChart(
    periodicity: Periodicity
  ): void {

    let data1: Array<number> = [];
    data1.push(Math.ceil(Math.random() * 100));
    data1.push(Math.ceil(Math.random() * 100));
    data1.push(Math.ceil(Math.random() * 100));
    data1.push(Math.ceil(Math.random() * 100));

    let data2: Array<number> = [];
    data2.push(Math.ceil(Math.random() * 100));
    data2.push(Math.ceil(Math.random() * 100));
    data2.push(Math.ceil(Math.random() * 100));
    data2.push(Math.ceil(Math.random() * 100));

    let data3: Array<number> = [];
    data3.push(Math.ceil(Math.random() * 100));
    data3.push(Math.ceil(Math.random() * 100));
    data3.push(Math.ceil(Math.random() * 100));
    data3.push(Math.ceil(Math.random() * 100));

    let data: Chart.ChartConfiguration = {
      type: 'bar',
      data: {
        labels: ['Week1', 'Week2', 'Week3', 'Week 4'],
        datasets: [{
          label: "Trial",
          type: "bar",
          stack: "Base",
          backgroundColor: "#F24D60",
          barThickness: 8,
          data: data1,
        }, {
          label: "Paying",
          type: "bar",
          stack: "Base",
          backgroundColor: "#6993FF",
          barThickness: 8,
          data: data2,
        }, {
          label: "Demo",
          type: "bar",
          stack: "Base",
          backgroundColor: "#1BC5BD",
          barThickness: 8,
          data: data3,
        }]
      },
      options: {
        legend: {
          position: 'bottom',
          labels: {
            boxWidth: 12,
            fontColor: '#000000',
            fontFamily: 'Caros Bold'
          }
        },
        scales: {
          xAxes: [{
            stacked: true,
            ticks: {
              beginAtZero: true,
              maxRotation: 0,
              minRotation: 0
            },
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            stacked: true,

          }]
        },
      }
    };

    this.totalUsersChart = new Chart(this.totalUsersChartContext, data);
  }

  private getInstitutionDetail(institution: InstitutionDto): void {
    this.institutionService
      .getInfo(institution.id)
      .subscribe(data => {
        this.institutionDetail = data;
      })
  }
}
