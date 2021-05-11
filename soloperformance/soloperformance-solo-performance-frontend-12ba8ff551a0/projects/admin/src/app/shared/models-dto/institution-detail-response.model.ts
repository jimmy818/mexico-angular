import { InstitutionDetailCoachResponse } from './institution-detail-coach-response.model';
import { InstitutionDetailEconomicResponse } from './institution-detail-economic-response.model';
import { InstitutionDetailManagerResponse } from './institution-detail-manager-response.model';
import { InstitutionDetailRevenueResponse } from './institution-detail-revenue-response.model';
import { InstitutionDetailStatsResponse } from './institution-detail-stats-response.model';

export interface InstitutionDetailResponse {
    institution_managers: Array<InstitutionDetailManagerResponse>;
    strength_coaches: Array<InstitutionDetailCoachResponse>;
    institution_stats: InstitutionDetailStatsResponse;
    revenue: InstitutionDetailRevenueResponse;
    economic: InstitutionDetailEconomicResponse;
}