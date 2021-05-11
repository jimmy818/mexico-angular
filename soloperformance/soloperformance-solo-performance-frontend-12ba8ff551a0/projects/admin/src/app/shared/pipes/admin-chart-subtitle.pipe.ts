import { Pipe, PipeTransform } from '@angular/core';

import { AdminChart } from '@admin/shared/enums/admin-chart.enum';

@Pipe({
  name: 'adminChartSubtitle'
})
export class AdminChartSubtitlePipe implements PipeTransform {

  transform(chart: AdminChart): string {
    switch (chart) {
      case AdminChart.newUsers:
        return 'Monthly evolution of users creation';
      case AdminChart.conversionRate:
        return 'Conversion rate';
      case AdminChart.churnRate:
        return 'Churn rate';
      case AdminChart.averageWeeklyRevenue:
        return 'Average weekly revenue';
      case AdminChart.averageMonthlyRevenue:
        return 'Average monthly revenue';
      case AdminChart.averageYearlyRevenue:
        return 'Average yearly revenue';
      case AdminChart.totalRevenue:
        return 'Total revenue';
      case AdminChart.totalUsers:
        return 'Total users';
      case AdminChart.activeUsers:
        return 'Active users';
      case AdminChart.churnedCustomers:
        return 'Churned customers';
    }
  }

}
