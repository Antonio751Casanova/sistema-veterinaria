export interface EspecieData {
  especie: string;
  cantidad: number;
}

export interface Estadisticas {
  clientes: {
    total: number;
    hoy: number;
    semana: number;
    mes: number;
  };
  mascotas: {
    total: number;
    por_especie: EspecieData[];
  };
  citas: {
    total: number;
    pendientes: number;
    hoy: number;
    semana: number;
  };
}

