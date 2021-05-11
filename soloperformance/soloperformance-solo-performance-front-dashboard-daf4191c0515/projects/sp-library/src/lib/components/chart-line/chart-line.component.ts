import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, Input } from '@angular/core';
import * as Chart from 'chart.js';

@Component({
  selector: 'sp-chart-line',
  templateUrl: './chart-line.component.html',
  styleUrls: ['./chart-line.component.scss']
})
export class ChartLineComponent implements OnInit, AfterViewInit {

  @Input() data: Array<any> = [];

  @ViewChild('chart') chartRef: ElementRef<HTMLCanvasElement>;

  chart: any = [];
  chartContext: CanvasRenderingContext2D;

  constructor() { }

  ngOnInit(): void {

  }

  ngAfterViewInit(): void {
    const canvasR4 = <any>this.chartRef.nativeElement;
    this.chartContext = canvasR4.getContext("2d");

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
      type: 'line',
      data: {
        labels: ['', '', '', ''],
        datasets: [{
          label: "Number of exercises",
          type: "line",
          borderColor: "#F24D60",
          fill: false,
          data: data1,
        }, {
          label: "Total volume",
          type: "line",
          borderColor: "#F7C141",
          fill: false,
          data: data2,
        }, {
          label: "RPE",
          type: "line",
          borderColor: "#315797",
          fill: false,
          data: data3,
        }]
      },
      options: {
        maintainAspectRatio: false,
        elements: {
          point: {
            radius: 0
          }
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
            //stacked: true,
            ticks: {
              stepSize: 10
            }
          }]
        },
      }
    };

    this.chart = new Chart(this.chartContext, data);
  }

}
