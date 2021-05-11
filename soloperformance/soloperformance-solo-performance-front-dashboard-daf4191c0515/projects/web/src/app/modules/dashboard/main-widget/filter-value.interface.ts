export interface Filter {
    name: string;
    text: string;
    selected: boolean;
    isIndividual: boolean;
    selectedMax?: number;
    selectedOrder?: number;
}