import axios, { AxiosError } from 'axios';
import type {
  LoginRequest,
  RegisterClienteRequest,
  RegisterProveedorRequest,
  AuthResponse,
  Servicio,
  Recurso,
  HorarioDisponible,
  Reserva,
  ReservaDetail,
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token a todas las requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ===== AUTH =====
export const authApi = {
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', data);
    return response.data;
  },

  registerCliente: async (data: RegisterClienteRequest) => {
    const response = await api.post('/auth/register/cliente', data);
    return response.data;
  },

  registerProveedor: async (data: RegisterProveedorRequest) => {
    const response = await api.post('/auth/register/proveedor', data);
    return response.data;
  },

  getProfile: async (role: 'cliente' | 'proveedor') => {
    const response = await api.get(`/auth/me/${role}`);
    return response.data;
  },
};

// ===== SERVICIOS =====
export const serviciosApi = {
  buscar: async (params?: { nombre?: string; categoria?: string }): Promise<Servicio[]> => {
    const response = await api.get<Servicio[]>('/servicios/buscar', { params });
    return response.data;
  },

  crear: async (data: { nombre: string; descripcion?: string; categoria?: string }) => {
    const response = await api.post('/servicios/', data);
    return response.data;
  },

  getMisServicios: async () => {
    const response = await api.get('/servicios/mis-servicios');
    return response.data;
  },

  getById: async (id: number): Promise<Servicio> => {
    const response = await api.get<Servicio>(`/servicios/${id}`);
    return response.data;
  },
};

// ===== RECURSOS =====
export const recursosApi = {
  crear: async (data: {
    servicio_id: number;
    nombre: string;
    descripcion?: string;
    capacidad?: number;
    caracteristicas?: string;
  }) => {
    const response = await api.post('/recursos/', data);
    return response.data;
  },

  getByServicio: async (servicioId: number): Promise<Recurso[]> => {
    const response = await api.get<Recurso[]>(`/recursos/servicio/${servicioId}`);
    return response.data;
  },
};

// ===== HORARIOS =====
export const horariosApi = {
  crear: async (data: {
    recurso_id: number;
    dia_semana: number;
    hora_inicio: string;
    hora_fin: string;
    precio: number;
    duracion_minutos: number;
  }) => {
    const response = await api.post('/horarios/', data);
    return response.data;
  },

  crearBulk: async (data: {
    recurso_id: number;
    dias_semana: number[];
    hora_inicio: string;
    hora_fin: string;
    precio: number;
    duracion_minutos: number;
  }) => {
    const response = await api.post('/horarios/bulk', data);
    return response.data;
  },

  getByRecurso: async (recursoId: number): Promise<HorarioDisponible[]> => {
    const response = await api.get<HorarioDisponible[]>(`/horarios/recurso/${recursoId}`);
    return response.data;
  },

  getDisponibilidad: async (recursoId: number, fecha: string) => {
    const response = await api.get(`/horarios/disponibilidad/${recursoId}/${fecha}`);
    return response.data;
  },
};

// ===== RESERVAS =====
export const reservasApi = {
  crear: async (data: {
    recurso_id: number;
    fecha_hora_inicio: string;
    duracion_minutos: number;
    notas_cliente?: string;
  }): Promise<Reserva> => {
    const response = await api.post<Reserva>('/reservas/', data);
    return response.data;
  },

  getMisReservas: async (estado?: string): Promise<ReservaDetail[]> => {
    const params = estado ? { estado } : {};
    const response = await api.get<ReservaDetail[]>('/reservas/mis-reservas', { params });
    return response.data;
  },

  getById: async (id: number): Promise<ReservaDetail> => {
    const response = await api.get<ReservaDetail>(`/reservas/${id}`);
    return response.data;
  },

  cancelar: async (id: number, motivo?: string) => {
    const response = await api.patch(`/reservas/${id}/cancelar`, { motivo });
    return response.data;
  },

  registrarPago: async (id: number, data: {
    monto: number;
    metodo_pago: 'efectivo' | 'tarjeta' | 'transferencia';
    es_pago_completo: boolean;
  }) => {
    const response = await api.patch(`/reservas/${id}/pago`, data);
    return response.data;
  },
};

export const proveedorApi = {
  // Servicios
  crearServicio: async (data: {
    nombre: string;
    descripcion?: string;
    categoria?: string;
  }) => {
    const response = await api.post('/servicios/', data);
    return response.data;
  },

  actualizarServicio: async (id: number, data: {
    nombre?: string;
    descripcion?: string;
    categoria?: string;
  }) => {
    const response = await api.patch(`/servicios/${id}`, data);
    return response.data;
  },

  // Recursos
  crearRecurso: async (data: {
    servicio_id: number;
    nombre: string;
    descripcion?: string;
    capacidad?: number;
    caracteristicas?: string;
  }) => {
    const response = await api.post('/recursos/', data);
    return response.data;
  },

  actualizarRecurso: async (id: number, data: {
    nombre?: string;
    descripcion?: string;
    capacidad?: number;
    caracteristicas?: string;
  }) => {
    const response = await api.patch(`/recursos/${id}`, data);
    return response.data;
  },

  // Horarios
  crearHorariosBulk: async (data: {
    recurso_id: number;
    dias_semana: number[];
    hora_inicio: string;
    hora_fin: string;
    precio: number;
    duracion_minutos: number;
  }) => {
    const response = await api.post('/horarios/bulk', data);
    return response.data;
  },

  // Reservas
  getReservasProveedor: async (estado?: string) => {
    const params = estado ? { estado } : {};
    const response = await api.get('/reservas/proveedor/todas', { params });
    return response.data;
  },

  confirmarReserva: async (id: number) => {
    const response = await api.patch(`/reservas/proveedor/${id}/confirmar`);
    return response.data;
  },

  completarReserva: async (id: number) => {
    const response = await api.patch(`/reservas/proveedor/${id}/completar`);
    return response.data;
  },
};


export default api;