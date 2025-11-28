import React, { useState, useEffect } from 'react';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Loading } from '../../components/common/Loading';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { reservasApi } from '../../services/api';
import type { ReservaDetail } from '../../types';
import { formatDate, formatCurrency } from '../../utils/formatters';
import { ESTADOS_RESERVA } from '../../utils/constants';
import { Calendar, DollarSign, CheckCircle, AlertCircle, X } from 'lucide-react';

export const MisReservasPage: React.FC = () => {
  const [reservas, setReservas] = useState<ReservaDetail[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Modal de pago
  const [showPagoModal, setShowPagoModal] = useState(false);
  const [reservaSeleccionada, setReservaSeleccionada] = useState<ReservaDetail | null>(null);
  const [montoPago, setMontoPago] = useState('');
  const [metodoPago, setMetodoPago] = useState('efectivo');
  const [isPagando, setIsPagando] = useState(false);

  useEffect(() => {
    cargarReservas();
  }, []);

  const cargarReservas = async () => {
    try {
      const data = await reservasApi.getMisReservas();
      setReservas(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelar = async (id: number) => {
    if (!confirm('¿Seguro que quieres cancelar esta reserva?')) return;
    
    try {
      await reservasApi.cancelar(id);
      cargarReservas();
    } catch (error) {
      console.error('Error:', error);
      alert('Error al cancelar reserva');
    }
  };

  const handleAbrirPago = (reserva: ReservaDetail) => {
    setReservaSeleccionada(reserva);
    setMontoPago(reserva.saldo_pendiente?.toString() || '');
    setMetodoPago(reserva.metodo_pago || 'efectivo');
    setShowPagoModal(true);
  };

  const handlePagar = async () => {
    if (!reservaSeleccionada) return;
    
    const monto = parseFloat(montoPago);
    if (!monto || monto <= 0) {
      alert('Ingresa un monto válido');
      return;
    }

    if (monto > (reservaSeleccionada.saldo_pendiente || 0)) {
      alert('El monto no puede ser mayor al saldo pendiente');
      return;
    }

    setIsPagando(true);
    try {
      await reservasApi.registrarPago(reservaSeleccionada.id, {
        monto,
        metodo_pago: metodoPago as any,
        es_pago_completo: monto === reservaSeleccionada.saldo_pendiente,
      });

      alert('Pago registrado exitosamente');
      setShowPagoModal(false);
      cargarReservas();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error al registrar pago');
    } finally {
      setIsPagando(false);
    }
  };

  if (isLoading) return <Loading />;

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Mis Reservas</h1>
        
        {reservas.length === 0 ? (
          <Card>
            <div className="text-center py-12">
              <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500 mb-4">No tienes reservas</p>
              <Button onClick={() => window.location.href = '/cliente/buscar'}>
                Buscar Servicios
              </Button>
            </div>
          </Card>
        ) : (
          <div className="space-y-4">
            {reservas.map((reserva) => (
              <Card key={reserva.id}>
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-lg">{reserva.servicio_nombre}</h3>
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
                    <p className="text-gray-600">{reserva.recurso_nombre}</p>
                    <p className="text-sm text-gray-500 mt-2">
                      {formatDate(reserva.fecha_hora_inicio)}
                    </p>

                    {/* Estado del pago */}
                    <div className="mt-3 space-y-2">
                      <div className="flex items-center gap-4">
                        <span className="text-lg font-semibold">
                          {formatCurrency(reserva.precio_total)}
                        </span>
                      </div>

                      {reserva.pago_completo ? (
                        <div className="flex items-center gap-2 text-green-700">
                          <CheckCircle className="w-5 h-5" />
                          <span className="font-medium">Pagado completo</span>
                          {reserva.pago_confirmado && (
                            <span className="text-xs bg-green-100 px-2 py-1 rounded">
                              ✓ Confirmado por proveedor
                            </span>
                          )}
                        </div>
                      ) : (
                        <>
                          {reserva.seña && reserva.seña > 0 ? (
                            <div className="space-y-1">
                              <div className="flex items-center gap-2 text-blue-700">
                                <DollarSign className="w-5 h-5" />
                                <span>Seña pagada: {formatCurrency(reserva.seña)}</span>
                                {reserva.pago_confirmado && (
                                  <span className="text-xs bg-blue-100 px-2 py-1 rounded">
                                    ✓ Confirmado
                                  </span>
                                )}
                              </div>
                              <div className="flex items-center gap-2 text-orange-700">
                                <AlertCircle className="w-5 h-5" />
                                <span className="font-medium">
                                  Saldo pendiente: {formatCurrency(reserva.saldo_pendiente || 0)}
                                </span>
                              </div>
                            </div>
                          ) : (
                            <div className="flex items-center gap-2 text-orange-700">
                              <AlertCircle className="w-5 h-5" />
                              <span>Sin pago registrado</span>
                            </div>
                          )}
                        </>
                      )}

                      {reserva.notas_pago && (
                        <div className="p-2 bg-gray-50 rounded text-sm text-gray-700">
                          <strong>Nota del proveedor:</strong> {reserva.notas_pago}
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex flex-col gap-2 ml-4">
                    {/* Botón de pagar */}
                    {!reserva.pago_completo && 
                     (reserva.estado === 'pendiente' || reserva.estado === 'confirmada') && (
                      <Button
                        onClick={() => handleAbrirPago(reserva)}
                        variant="secondary"
                      >
                        <DollarSign className="w-4 h-4 mr-1" />
                        Pagar
                      </Button>
                    )}

                    {/* Botón de cancelar */}
                    {reserva.estado === 'pendiente' && (
                      <Button
                        variant="danger"
                        onClick={() => handleCancelar(reserva.id)}
                      >
                        Cancelar
                      </Button>
                    )}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Modal de Pago */}
        {showPagoModal && reservaSeleccionada && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <Card className="max-w-md w-full">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Registrar Pago</h2>
                <button
                  onClick={() => setShowPagoModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600">Reserva</p>
                <p className="font-semibold">{reservaSeleccionada.servicio_nombre}</p>
                <p className="text-sm">{reservaSeleccionada.recurso_nombre}</p>
              </div>

              <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                <div className="flex justify-between">
                  <span className="text-sm">Precio total:</span>
                  <span className="font-semibold">{formatCurrency(reservaSeleccionada.precio_total)}</span>
                </div>
                {reservaSeleccionada.seña && reservaSeleccionada.seña > 0 && (
                  <div className="flex justify-between text-green-700">
                    <span className="text-sm">Ya pagado:</span>
                    <span className="font-semibold">{formatCurrency(reservaSeleccionada.seña)}</span>
                  </div>
                )}
                <div className="flex justify-between border-t mt-2 pt-2">
                  <span className="font-semibold">Saldo pendiente:</span>
                  <span className="font-bold text-lg text-orange-700">
                    {formatCurrency(reservaSeleccionada.saldo_pendiente || 0)}
                  </span>
                </div>
              </div>

              <Input
                type="number"
                label="Monto a pagar"
                value={montoPago}
                onChange={(e) => setMontoPago(e.target.value)}
                min="0"
                max={reservaSeleccionada.saldo_pendiente?.toString()}
                step="0.01"
                required
              />

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Método de pago
                </label>
                <select
                  value={metodoPago}
                  onChange={(e) => setMetodoPago(e.target.value)}
                  className="input-field"
                >
                  <option value="efectivo">Efectivo</option>
                  <option value="tarjeta">Tarjeta</option>
                  <option value="transferencia">Transferencia</option>
                </select>
              </div>

              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg mb-4 text-sm text-yellow-800">
                El proveedor deberá confirmar que recibió el pago.
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={handlePagar}
                  isLoading={isPagando}
                  className="flex-1"
                >
                  Confirmar Pago
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