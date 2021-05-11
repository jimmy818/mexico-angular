import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UtilitiesService {

  constructor() { }

  /**
   * Obtiene el valor indicado en formato DbName
   * @param value Valor a convertir en formato DbName
   * @param prefix Prefijo a agregar al texto
   */
  static getDbName(value: string, prefix?: string): string {

    if (!value) return '';

    return `${prefix ? prefix : 'spf_'}${value
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')  // Elimina acentos.
      .replace(/[^a-zA-Z0-9]/g, '')     // Elimina todos los caracteres que no sean letras o números
      .toLowerCase()
      }`;
  }
}
