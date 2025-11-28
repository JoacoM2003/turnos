import React, { useState, useEffect } from 'react';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Loading } from '../../components/common/Loading';
import { Input } from '../../components/common/Input';
import { recursosApi, serviciosApi, proveedorApi } from '../../services/api';
import type { Recurso, Servicio, ReservaDetail } from '../../types';
import { formatDate, formatCurrency, formatTime } from '../../utils/formatters';
import { ESTADOS_RESERVA } from '../../utils/constants';
import { Calendar, Check, X, AlertCircle, DollarSign, CheckCircle, XCircle } from 'lucide-react';

export const ReservasPorRecursoPage: React.FC = () => {
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [recursos, setRecursos] = useState<Recurso[]>([]);
  const [selectedRecurso, setSelectedRecurso] = useState<Recurso | null>(null);
  const [fecha, setFecha] = useState(new Date().toISOString().split('T')[0]);
  const [reservas, setReservas] = useState<ReservaDetail[]>([]);
  const [isLoadingServicios, setIsLoadingServicios] = useState(true);
  const [isLoadingReservas, setIsLoadingReservas] = useState(false);
  
  // Modal confirmación pago
  const [showPagoModal, setShowPagoModal] = useState(false);
  const [reservaSeleccionada, setReservaSeleccionada] = useState<ReservaDetail | null>(null);
  const [pagoConfirmado, setPagoConfirmado] = useState(false);
  const [notasPago, setNotasPago] = useState('');

  useEffect(() => {
    cargarServicios();
  }, []);

  useEffect(() => {
    if (selectedRecurso && fecha) {
      cargarReservas();
    }
  }, [selectedRecurso, fecha]);

  const cargarServicios = async () => {
    try {
      const data = await serviciosApi.getMisServicios();
      setServicios(data);
      
      // Cargar recursos del primer servicio si existe
      if (data.length > 0 && data[0].recursos) {
        setRecursos(data[0].recursos);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoadingServicios(false);
    }
  };

  const handleSelectServicio = async (servicio: Servicio) => {
    try {
      const data = await recursosApi.getByServicio(servicio.id);
      setRecursos(data);
      setSelectedRecurso(null);
      setReservas([]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const cargarReservas = async () => {
    if (!selectedRecurso) return;
    
    setIsLoadingReservas(true);
    try {
      const data = await proveedorApi.getReservasPorRecurso(selectedRecurso.id, fecha);
      setReservas(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoadingReservas(false);
    }
  };

  const handleConfirmarReserva = async (id: number) => {
    try {
      await proveedorApi.confirmarReserva(id);
      cargarReservas();
      alert('Reserva confirmada');
    } catch (error) {
      console.error('Error:', error);
      alert('Error al confirmar reserva');
    }
  };

  const handleCompletarReserva = async (id: number) => {
    try {
      await proveedorApi.completarReserva(id);
      cargarReservas();
      alert('Reserva completada');
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error al completar reserva');
    }
  };

  const handleMarcarNoAsistio = async (id: number) => {
    if (!confirm('¿Marcar que el cliente no asistió?')) return;
    
    try {
      await proveedorApi.marcarNoAsistio(id);
      cargarReservas();
      alert('Marcado como no asistió');
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error');
    }
  };

  const handleAbrirConfirmarPago = (reserva: ReservaDetail) => {
    setReservaSeleccionada(reserva);
    setPagoConfirmado(reserva.pago_confirmado);
    setNotasPago(reserva.notas_pago || '');
    setShowPagoModal(true);
  };

  const handleConfirmarPago = async () => {
    if (!reservaSeleccionada) return;

    try {
      await proveedorApi.confirmarPago(reservaSeleccionada.id, {
        pago_confirmado: pagoConfirmado,
        notas_pago: notasPago || undefined,
      });

      setShowPagoModal(false);
      cargarReservas();
      alert('Estado de pago actualizado');
    } catch (error) {
      console.error('Error:', error);
      alert('Error al actualizar pago');
    }
  };

  if (isLoadingServicios) return <Loading />;

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Reservas por Recurso</h1>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Columna 1: Servicios */}
          <Card>
            <h2 className="font-semibold text-lg mb-4">Mis Servicios</h2>
            <div className="space-y-2">
              {servicios.map((servicio) => (
                <button
                  key={servicio.id}
                  onClick={() => handleSelectServicio(servicio)}
                  className="w-full text-left p-3 rounded-lg border-2 transition-all hover:border-primary-400"
                >
                  <div className="font-medium">{servicio.nombre}</div>
                  <div className="text-sm text-gray-500">
                    {servicio.recursos_count || 0} recursos
                  </div>
                </button>
              ))}
            </div>
          </Card>

          {/* Columna 2: Recursos */}
          <Card>
            <h2 className="font-semibold text-lg mb-4">Recursos</h2>
            {recursos.length === 0 ? (
              <p className="text-gray-500 text-center py-8">
                Selecciona un servicio
              </p>
            ) : (
              <div className="space-y-2">
                {recursos.map((recurso) => (
                  <button
                    key={recurso.id}
                    onClick={() => setSelectedRecurso(recurso)}
                    className={`w-full text-left p-3 rounded-lg border-2 transition-all ${
                      selectedRecurso?.id === recurso.id
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-primary-400'
                    }`}
                  >
                    <div className="font-medium">{recurso.nombre}</div>
                    {recurso.capacidad && (
                      <div className="text-sm text-gray-500">
                        Cap: {recurso.capacidad}
                      </div>
                    )}
                  </button>
                ))}
              </div>
            )}
          </Card>

          {/* Columna 3: Selector de fecha y resumen */}
          <Card>
            <h2 className="font-semibold text-lg mb-4">Fecha</h2>
            {selectedRecurso ? (
              <>
                <Input
                  type="date"
                  value={fecha}
                  onChange={(e) => setFecha(e.target.value)}
                />
                <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                  <div className="text-sm text-gray-600">Recurso seleccionado</div>
                  <div className="font-semibold">{selectedRecurso.nombre}</div>
                  <div className="text-sm text-gray-500 mt-2">
                    {new Date(fecha).toLocaleDateString('es-AR', { 
                      weekday: 'long', 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}
                  </div>
                </div>
              </>
            ) : (
              <p className="text-gray-500 text-center py-8">
                Selecciona un recurso
              </p>
            )}
          </Card>
        </div>

        {/* Reservas del día */}
        {selectedRecurso && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">
              Reservas del {new Date(fecha).toLocaleDateString('es-AR')}
            </h2>

            {isLoadingReservas ? (
              <Loading message="Cargando reservas..." />
            ) : reservas.length === 0 ? (
              <Card>
                <div className="text-center py-12">
                  <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No hay reservas para este día</p>
                </div>
              </Card>
            ) : (
              <div className="space-y-4">
                {reservas.map((reserva) => (
                  <Card key={reserva.id}>
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-lg font-semibold">
                            {formatTime(reserva.fecha_hora_inicio.split('T')[1])} - 
                            {formatTime(reserva.fecha_hora_fin.split('T')[1])}
                          </span>
                          <span
                            className={`px-3 py-1 rounded-full text-sm`}
                            style={{
                              backgroundColor: `var(--${ESTADOS_RESERVA[reserva.estado].color}-100)`,
                              color: `var(--${ESTADOS_RESERVA[reserva.estado].color}-700)`,
                            }}
                          >
                            {ESTADOS_RESERVA[reserva.estado].label}
                          </span>
                        </div>

                        <div className="space-y-1 text-sm">
                          <p><strong>Cliente:</strong> {reserva.cliente_nombre}</p>
                          <p><strong>Precio:</strong> {formatCurrency(reserva.precio_total)}</p>
                        </div>

                        {/* Estado del pago */}
                        <div className="mt-3 space-y-1">
                          {reserva.pago_completo ? (
                            <div className="flex items-center gap-2 text-green-700">
                              <CheckCircle className="w-5 h-5" />
                              <span className="font-medium">Pagado completo</span>
                              {reserva.pago_confirmado ? (
                                <span className="text-xs bg-green-100 px-2 py-1 rounded">
                                  ✓ Confirmado
                                </span>
                              ) : (
                                <button
                                  onClick={() => handleAbrirConfirmarPago(reserva)}
                                  className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded hover:bg-yellow-200"
                                >
                                  Confirmar pago
                                </button>
                              )}
                            </div>
                          ) : (
                            <>
                              {reserva.seña && reserva.seña > 0 ? (
                                <div className="space-y-1">
                                  <div className="flex items-center gap-2 text-blue-700">
                                    <DollarSign className="w-5 h-5" />
                                    <span>Seña: {formatCurrency(reserva.seña)}</span>
                                    {reserva.pago_confirmado ? (
                                      <span className="text-xs bg-blue-100 px-2 py-1 rounded">
                                        ✓ Confirmado
                                      </span>
                                    ) : (
                                      <button
                                        onClick={() => handleAbrirConfirmarPago(reserva)}
                                        className="text-xs bg-yellow-100 text-yellow-700 px-2 py-1 rounded hover:bg-yellow-200"
                                      >
                                        Confirmar
                                      </button>
                                    )}
                                  </div>
                                  <div className="text-orange-700 text-sm">
                                    Saldo: {formatCurrency(reserva.saldo_pendiente || 0)}
                                  </div>
                                </div>
                              ) : (
                                <div className="flex items-center gap-2 text-orange-700">
                                  <AlertCircle className="w-5 h-5" />
                                  <span className="text-sm">Sin pago registrado</span>
                                </div>
                              )}
                            </>
                          )}

                          {reserva.metodo_pago && (
                            <p className="text-xs text-gray-500">
                              Método: {reserva.metodo_pago}
                            </p>
                          )}

                          {reserva.notas_pago && (
                            <div className="p-2 bg-gray-50 rounded text-xs text-gray-700">
                              <strong>Nota:</strong> {reserva.notas_pago}
                            </div>
                          )}
                        </div>

                        {reserva.notas_cliente && (
                          <div className="mt-2 p-2 bg-blue-50 rounded text-sm">
                            <strong>Notas del cliente:</strong> {reserva.notas_cliente}
                          </div>
                        )}
                      </div>

                      {/* Acciones */}
                      <div className="flex flex-col gap-2 ml-4">
                        {reserva.estado === 'pendiente' && (
                          <Button
                            onClick={() => handleConfirmarReserva(reserva.id)}
                            className="whitespace-nowrap"
                          >
                            <Check className="w-4 h-4 mr-1" />
                            Confirmar
                          </Button>
                        )}

                        {reserva.estado === 'confirmada' && (
                          <>
                            <Button
                              onClick={() => handleCompletarReserva(reserva.id)}
                              variant="secondary"
                              className="whitespace-nowrap"
                            >
                              <CheckCircle className="w-4 h-4 mr-1" />
                              Completar
                            </Button>
                            <Button
                              onClick={() => handleMarcarNoAsistio(reserva.id)}
                              variant="danger"
                              className="whitespace-nowrap"
                            >
                              <XCircle className="w-4 h-4 mr-1" />
                              No asistió
                            </Button>
                          </>
                        )}
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Modal Confirmar Pago */}
        {showPagoModal && reservaSeleccionada && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <Card className="max-w-md w-full">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Confirmar Pago</h2>
                <button
                  onClick={() => setShowPagoModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                <p><strong>Cliente:</strong> {reservaSeleccionada.cliente_nombre}</p>
                <p><strong>Monto:</strong> {formatCurrency(reservaSeleccionada.seña || reservaSeleccionada.precio_total)}</p>
                <p><strong>Método:</strong> {reservaSeleccionada.metodo_pago}</p>
              </div>

              <div className="mb-4">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={pagoConfirmado}
                    onChange={(e) => setPagoConfirmado(e.target.checked)}
                    className="w-5 h-5"
                  />
                  <span className="font-medium">Confirmo que recibí el pago</span>
                </label>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notas (opcional)
                </label>
                <textarea
                  value={notasPago}
                  onChange={(e) => setNotasPago(e.target.value)}
                  className="input-field min-h-[80px]"
                  placeholder="Ej: Recibido en efectivo, Transferencia verificada, etc."
                />
              </div>

              <div className="flex gap-2">
                <Button onClick={handleConfirmarPago} className="flex-1">
                  Guardar
                </Button>
                <Button
                  variant="secondary"
                  onClick={() => setShowPagoModal(false)}
                  className="flex-1"
                >
                  Cancelar
                </Button>
              </div>
            </Card>
          </div>
        )}
      </div>
    </Layout>
  );
};