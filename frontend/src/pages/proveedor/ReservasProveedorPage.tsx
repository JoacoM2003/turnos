import React, { useState, useEffect } from 'react';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Loading } from '../../components/common/Loading';
import { proveedorApi } from '../../services/api';
import type { ReservaDetail } from '../../types';
import { formatDate, formatCurrency } from '../../utils/formatters';
import { ESTADOS_RESERVA } from '../../utils/constants';
import { Check, X, Calendar } from 'lucide-react';

export const ReservasProveedorPage: React.FC = () => {
  const [reservas, setReservas] = useState<ReservaDetail[]>([]);
  const [filtroEstado, setFiltroEstado] = useState<string>('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    cargarReservas();
  }, [filtroEstado]);

  const cargarReservas = async () => {
    try {
      const data = await proveedorApi.getReservasProveedor(filtroEstado || undefined);
      setReservas(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleConfirmar = async (id: number) => {
    try {
      await proveedorApi.confirmarReserva(id);
      cargarReservas();
    } catch (error) {
      console.error('Error:', error);
      alert('Error al confirmar reserva');
    }
  };

  const handleCompletar = async (id: number) => {
    try {
      await proveedorApi.completarReserva(id);
      cargarReservas();
    } catch (error) {
      console.error('Error:', error);
      alert('Error al completar reserva');
    }
  };

  if (isLoading) return <Loading />;

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Reservas</h1>

        {/* Filtros */}
        <div className="mb-6 flex gap-2 flex-wrap">
          <button
            onClick={() => setFiltroEstado('')}
            className={`px-4 py-2 rounded-lg ${
              filtroEstado === ''
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Todas
          </button>
          {Object.entries(ESTADOS_RESERVA).map(([key, { label, color }]) => (
            <button
              key={key}
              onClick={() => setFiltroEstado(key)}
              className={`px-4 py-2 rounded-lg ${
                filtroEstado === key
                  ? `bg-${color}-600 text-white`
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {reservas.length === 0 ? (
          <Card>
            <div className="text-center py-12">
              <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">No hay reservas {filtroEstado && `en estado "${ESTADOS_RESERVA[filtroEstado as keyof typeof ESTADOS_RESERVA].label}"`}</p>
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
                      <span className={`px-3 py-1 rounded-full text-sm bg-${ESTADOS_RESERVA[reserva.estado].color}-100 text-${ESTADOS_RESERVA[reserva.estado].color}-700`}>
                        {ESTADOS_RESERVA[reserva.estado].label}
                      </span>
                    </div>
                    
                    <p className="text-gray-600">{reserva.recurso_nombre}</p>
                    <p className="text-sm text-gray-500 mt-1">
                      Cliente: {reserva.cliente_nombre}
                    </p>
                    <p className="text-sm text-gray-500">
                      {formatDate(reserva.fecha_hora_inicio)}
                    </p>
                    
                    {reserva.notas_cliente && (
                      <div className="mt-2 p-2 bg-gray-50 rounded text-sm">
                        <strong>Notas:</strong> {reserva.notas_cliente}
                      </div>
                    )}

                    <div className="mt-3 flex items-center gap-4">
                      <span className="font-semibold text-lg">
                        {formatCurrency(reserva.precio_total)}
                      </span>
                      {!reserva.pago_completo && (
                        <span className="text-sm text-orange-600">
                          Saldo pendiente: {formatCurrency(reserva.saldo_pendiente || 0)}
                        </span>
                      )}
                      {reserva.pago_completo && (
                        <span className="text-sm text-green-600">✓ Pagado</span>
                      )}
                    </div>
                  </div>

                  <div className="flex flex-col gap-2 ml-4">
                    {reserva.estado === 'pendiente' && (
                      <Button
                        onClick={() => handleConfirmar(reserva.id)}
                        className="whitespace-nowrap"
                      >
                        <Check className="w-4 h-4 mr-1" />
                        Confirmar
                      </Button>
                    )}
                    
                    {reserva.estado === 'confirmada' && (
                      <Button
                        onClick={() => handleCompletar(reserva.id)}
                        variant="secondary"
                        className="whitespace-nowrap"
                      >
                        <Check className="w-4 h-4 mr-1" />
                        Completar
                      </Button>
                    )}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};