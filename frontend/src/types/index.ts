export interface User {
  id: number;
  email: string;
  username: string;
  role: 'cliente' | 'proveedor' | 'admin';
  is_active: boolean;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterClienteRequest {
  email: string;
  password: string;
  username: string;
  nombre: string;
  apellido: string;
  telefono?: string;
  dni?: string;
}

export interface RegisterProveedorRequest extends RegisterClienteRequest {
  especialidad: string;
  matricula?: string;
  biografia?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Servicio {
  id: number;
  proveedor_id: number;
  nombre: string;
  descripcion?: string;
  categoria?: string;
  is_active: boolean;
}

export interface Recurso {
  id: number;
  servicio_id: number;
  nombre: string;
  descripcion?: string;
  capacidad?: number;
  imagen_url?: string;
  caracteristicas?: string;
  is_active: boolean;
  orden: number;
}

export interface HorarioDisponible {
  id: number;
  recurso_id: number;
  dia_semana: number;
  hora_inicio: string;
  hora_fin: string;
  precio: number;
  duracion_minutos: number;
  is_active: boolean;
}

export interface Reserva {
  id: number;
  cliente_id: number;
  recurso_id: number;
  fecha_hora_inicio: string;
  fecha_hora_fin: string;
  duracion_minutos: number;
  estado: 'pendiente' | 'confirmada' | 'cancelada' | 'completada' | 'no_asistio';
  precio_total: number;
  seña?: number;
  saldo_pendiente?: number;
  pago_completo: boolean;
  pago_confirmado: boolean;  // NUEVO
  notas_cliente?: string;
  notas_pago?: string;  // NUEVO
  created_at: string;
}

export interface ReservaDetail extends Reserva {
  recurso_nombre: string;
  servicio_nombre: string;
  cliente_nombre: string;
}