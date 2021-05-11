import { Component, OnInit, AfterViewInit, ViewChild, ElementRef, Input, OnChanges, SimpleChanges, DoCheck } from '@angular/core';

import * as Chart from 'chart.js';

@Component({
  selector: 'web-stats-chart',
  templateUrl: './stats-chart.component.html',
  styleUrls: ['./stats-chart.component.scss']
})
export class StatsChartComponent implements OnInit, AfterViewInit, OnChanges {

  @Input() exercisesNumberSelected = false;
  @Input() exercisesNumberData: Chart.ChartDataSets;

  @Input() totalVolumeSelected = false;
  @Input() totalVolumeData: Chart.ChartDataSets;

  @Input() rpeSelected = false;
  @Input() rpeData: Chart.ChartDataSets;

  @Input() preTrainingSurveySelected = false;
  @Input() preTrainingSurveyData: Chart.ChartDataSets;

  @Input() sessionTimeSelected = false;
  @Input() sessionTimeData: Chart.ChartDataSets;

  @ViewChild('chart') chartRef: ElementRef<HTMLCanvasElement>;

  chart: Chart;
  chartContext: CanvasRenderingContext2D;


  private data: Chart.ChartConfiguration;

  private canvas: HTMLCanvasElement;

  exercisesNumberMetadata: any;
  totalVolumeMetadata: any;
  rpeMetadata: any;
  preTrainingSurveyMetadata: any;
  sessionTimeMetadata: any;

  currentCharts: Array<any> = [];

  constructor() { }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['exercisesNumberSelected']) {
      setTimeout(() => {
        this.addRemoveExercisesNumberData();
      }, 0);
    }
    if (changes['totalVolumeSelected']) {
      setTimeout(() => {
        this.addRemoveTotalVolumeData();
      }, 0);
    }
    if (changes['rpeSelected']) {
      setTimeout(() => {
        this.addRemoveRPEData();
      }, 0);
    }
    if (changes['preTrainingSurveySelected']) {
      setTimeout(() => {
        this.addRemovePreTrainingSurveyData();
      }, 0);
    }
    if (changes['sessionTimeSelected']) {
      setTimeout(() => {
        this.addRemoveSessionTimeData();
      }, 0);
    }
  }

  ngAfterViewInit(): void {

    if (!this.chartRef) {
      return;
    }
    this.canvas = this.chartRef.nativeElement;
    this.chartContext = this.canvas.getContext("2d");

    // let tvBackground = this.chartContext.createLinearGradient(0, 0, 0, canvas.height);
    // tvBackground.addColorStop(0, "rgba(247, 193, 65, 0.5)");
    // tvBackground.addColorStop(1, "rgba(247, 193, 65, 0.1)");

    this.data = {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: []
      },
      options: {
        maintainAspectRatio: false,
        elements: {
          // point: {
          //   radius: 0
          // }
        },
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
            ticks: {
              stepSize: 10
            },
            gridLines: {
              color: '#ECEDF4'
            }
          }]
        },
      }
    };

    this.chart = new Chart(this.chartContext, this.data);
  }

  private addRemoveExercisesNumberData(): void {

    if (!this.chart || !this.canvas) {
      return;
    }

    if (this.exercisesNumberSelected) {

      const color = '234, 28, 44';
      let borderColor = `rgb(${color})`;
      let backgroundColor = this.chartContext.createLinearGradient(0, 0, 0, (<any>this.canvas.parentNode).clientHeight);
      backgroundColor.addColorStop(0, `rgba(${color}, 0.5)`);
      backgroundColor.addColorStop(1, `rgba(${color}, 0.05)`);

      this.exercisesNumberData = {
        label: "Number of exercises",
        type: "line",
        borderColor: borderColor,
        backgroundColor: backgroundColor,
        data: this.getDummyData()
      };

      this.data.data.datasets.push(this.exercisesNumberData);

      this.exercisesNumberMetadata = { color: this.getAvailableColor() };
      this.currentCharts.push(this.exercisesNumberMetadata);

      this.chart.update();

    } else {

      let index = this.chart.data.datasets.indexOf(this.exercisesNumberData);
      this.chart.data.datasets.splice(index, 1);

      let metadataIndex = this.currentCharts.indexOf(this.exercisesNumberMetadata);
      this.currentCharts.splice(metadataIndex, 1);

      this.chart.update();
    }
  }

  private addRemoveTotalVolumeData(): void {

    if (!this.chart || !this.canvas) {
      return;
    }

    if (this.totalVolumeSelected) {

      const color = '247,193,65';
      let borderColor = `rgb(${color})`;
      let backgroundColor = this.chartContext.createLinearGradient(0, 0, 0, (<any>this.canvas.parentNode).clientHeight);
      backgroundColor.addColorStop(0, `rgba(${color}, 0.5)`);
      backgroundColor.addColorStop(1, `rgba(${color}, 0.05)`);

      this.totalVolumeData = {
        label: "Total volume",
        type: "line",
        borderColor: borderColor,
        backgroundColor: backgroundColor,
        data: this.getDummyData()
      };

      this.data.data.datasets.push(this.totalVolumeData);

      this.totalVolumeMetadata = { color: this.getAvailableColor() };
      this.currentCharts.push(this.totalVolumeMetadata);

      this.chart.update();

    } else {

      let index = this.chart.data.datasets.indexOf(this.totalVolumeData);
      this.chart.data.datasets.splice(index, 1);

      let metadataIndex = this.currentCharts.indexOf(this.totalVolumeMetadata);
      this.currentCharts.splice(metadataIndex, 1);

      this.chart.update();
    }

  }

  private addRemoveRPEData(): void {

    if (!this.chart || !this.canvas) {
      return;
    }

    if (this.rpeSelected) {

      const color = '49,87,151';
      let borderColor = `rgb(${color})`;
      let backgroundColor = this.chartContext.createLinearGradient(0, 0, 0, (<any>this.canvas.parentNode).clientHeight);
      backgroundColor.addColorStop(0, `rgba(${color}, 0.5)`);
      backgroundColor.addColorStop(1, `rgba(${color}, 0.05)`);

      this.rpeData = {
        label: "RPE",
        type: "line",
        borderColor: borderColor,
        backgroundColor: backgroundColor,
        data: this.getDummyData()
      };

      this.data.data.datasets.push(this.rpeData);

      this.rpeMetadata = { color: this.getAvailableColor() };
      this.currentCharts.push(this.rpeMetadata);

      this.chart.update();

    } else {

      let index = this.chart.data.datasets.indexOf(this.rpeData);
      this.chart.data.datasets.splice(index, 1);

      let metadataIndex = this.currentCharts.indexOf(this.rpeMetadata);
      this.currentCharts.splice(metadataIndex, 1);

      this.chart.update();
    }

  }

  private addRemovePreTrainingSurveyData(): void {

    if (!this.chart || !this.canvas) {
      return;
    }

    if (this.preTrainingSurveySelected) {

      const color = '133,93,189';
      let borderColor = `rgb(${color})`;
      let backgroundColor = this.chartContext.createLinearGradient(0, 0, 0, (<any>this.canvas.parentNode).clientHeight);
      backgroundColor.addColorStop(0, `rgba(${color}, 0.5)`);
      backgroundColor.addColorStop(1, `rgba(${color}, 0.05)`);

      this.preTrainingSurveyData = {
        label: "Pre training survey",
        type: "line",
        borderColor: borderColor,
        backgroundColor: backgroundColor,
        data: this.getDummyData()
      };

      this.data.data.datasets.push(this.preTrainingSurveyData);

      this.preTrainingSurveyMetadata = { color: this.getAvailableColor() };
      this.currentCharts.push(this.preTrainingSurveyMetadata);

      this.chart.update();

    } else {

      let index = this.chart.data.datasets.indexOf(this.preTrainingSurveyData);
      this.chart.data.datasets.splice(index, 1);

      let metadataIndex = this.currentCharts.indexOf(this.preTrainingSurveyMetadata);
      this.currentCharts.splice(metadataIndex, 1);

      this.chart.update();
    }

  }

  private addRemoveSessionTimeData(): void {

    if (!this.chart || !this.canvas) {
      return;
    }

    if (this.sessionTimeSelected) {

      const color = '237,62,127';
      let borderColor = `rgb(${color})`;
      let backgroundColor = this.chartContext.createLinearGradient(0, 0, 0, (<any>this.canvas.parentNode).clientHeight);
      backgroundColor.addColorStop(0, `rgba(${color}, 0.5)`);
      backgroundColor.addColorStop(1, `rgba(${color}, 0.05)`);

      this.sessionTimeData = {
        label: "Session time",
        type: "line",
        borderColor: borderColor,
        backgroundColor: backgroundColor,
        data: this.getDummyData()
      };

      this.data.data.datasets.push(this.sessionTimeData);

      this.sessionTimeMetadata = { color: this.getAvailableColor() };
      this.currentCharts.push(this.sessionTimeMetadata);

      this.chart.update();

    } else {

      let index = this.chart.data.datasets.indexOf(this.sessionTimeData);
      this.chart.data.datasets.splice(index, 1);

      let metadataIndex = this.currentCharts.indexOf(this.sessionTimeMetadata);
      this.currentCharts.splice(metadataIndex, 1);

      this.chart.update();
    }

  }

  private getAvailableColor(): string {
    return this.checkColorUsed() === 'color1' ? 'color2' : 'color1';
  }

  private getAvailableBorderColor(): string {
    let bordercolor = '';
    if (this.checkColorUsed() === 'color1') {
      bordercolor = "#315797";
    } else {
      bordercolor = "#F24D60";
    }
    return bordercolor;
  }

  private getAvailableBackgroundColor(): CanvasGradient {

    let background = this.chartContext.createLinearGradient(0, 0, 0, (<any>this.canvas.parentNode).clientHeight);

    if (this.checkColorUsed() === 'color1') {
      background.addColorStop(0, "rgba(49, 87, 151, 0.5)");
      background.addColorStop(1, "rgba(49, 87, 151, 0.1)");
    } else {
      background.addColorStop(0, "rgba(234, 28, 44, 0.5)");
      background.addColorStop(1, "rgba(234, 28, 44, 0.1)");
    }

    return background;
  }

  private checkColorUsed(): string {
    if (!this.currentCharts.length) {
      return '';
    }
    return this.currentCharts[0].color;
  }

  private getDummyData(): Array<number> {
    return [
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100
    ];
  }
}