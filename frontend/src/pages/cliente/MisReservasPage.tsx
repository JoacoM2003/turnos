import React, { useState, useEffect } from 'react';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Loading } from '../../components/common/Loading';
import { Button } from '../../components/common/Button';
import { reservasApi } from '../../services/api';
import type { ReservaDetail } from '../../types';
import { formatDate, formatCurrency } from '../../utils/formatters';
import { ESTADOS_RESERVA } from '../../utils/constants';
import { Calendar } from 'lucide-react';

export const MisReservasPage: React.FC = () => {
  const [reservas, setReservas] = useState<ReservaDetail[]>([]);
  const [isLoading, setIsLoading] = useState(true);

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
                    <div className="mt-2 flex items-center gap-4">
                      <span className="text-lg font-semibold">
                        {formatCurrency(reserva.precio_total)}
                      </span>
                      {!reserva.pago_completo && reserva.saldo_pendiente && (
                        <span className="text-sm text-orange-600">
                          Saldo: {formatCurrency(reserva.saldo_pendiente)}
                        </span>
                      )}
                    </div>
                  </div>
                  
                  {reserva.estado === 'pendiente' && (
                    <Button
                      variant="danger"
                      onClick={() => handleCancelar(reserva.id)}
                    >
                      Cancelar
                    </Button>
                  )}
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};