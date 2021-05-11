import { Pipe, PipeTransform } from '@angular/core';

import { AdminChart } from '@admin/shared/enums/admin-chart.enum';

@Pipe({
  name: 'adminChartTitle'
})
export class AdminChartTitlePipe implements PipeTransform {

  transform(chart: AdminChart): string {
    switch (chart) {
      case AdminChart.newUsers:
        return 'New Users';
      case AdminChart.conversionRate:
        return 'Conversion Rate';
      case AdminChart.churnRate:
        return 'Churn Rate';
      case AdminChart.averageWeeklyRevenue:
        return 'Average Weekly Revenue';
      case AdminChart.averageMonthlyRevenue:
        return 'Average Monthly Revenue';
      case AdminChart.averageYearlyRevenue:
        return 'Average Yearly Revenue';
      case AdminChart.totalRevenue:
        return 'Total Revenue';
      case AdminChart.totalUsers:
        return 'Total Users';
      case AdminChart.activeUsers:
        return 'Active Users';
      case AdminChart.churnedCustomers:
        return 'Churned Customers';
    }
  }

}
