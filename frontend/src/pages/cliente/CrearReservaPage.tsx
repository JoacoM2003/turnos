import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Loading } from '../../components/common/Loading';
import { recursosApi, horariosApi, reservasApi } from '../../services/api';
import type { Recurso, HorarioDisponible } from '../../types';
import { formatCurrency } from '../../utils/formatters';
import { DIAS_SEMANA } from '../../utils/constants';
import { ArrowLeft, AlertCircle } from 'lucide-react';

export const CrearReservaPage: React.FC = () => {
  const { recursoId } = useParams();
  const navigate = useNavigate();
  const [recurso, setRecurso] = useState<Recurso | null>(null);
  const [horarios, setHorarios] = useState<HorarioDisponible[]>([]);
  const [reservasExistentes, setReservasExistentes] = useState<any[]>([]);
  const [fecha, setFecha] = useState('');
  const [horaSeleccionada, setHoraSeleccionada] = useState('');
  const [precioSeleccionado, setPrecioSeleccionado] = useState(0);
  
  // Nuevo: Pago
  const [mostrarPago, setMostrarPago] = useState(false);
  const [seña, setSeña] = useState('');
  const [metodoPago, setMetodoPago] = useState('efectivo');
  
  const [isLoading, setIsLoading] = useState(false);
  const [loadingRecurso, setLoadingRecurso] = useState(true);

  useEffect(() => {
    cargarRecurso();
    cargarHorarios();
  }, [recursoId]);

  useEffect(() => {
    if (fecha) {
      cargarReservasDelDia();
    }
  }, [fecha]);

  const cargarRecurso = async () => {
    try {
      const data = await recursosApi.getByServicio(1);
      const rec = data.find(r => r.id === Number(recursoId));
      if (rec) setRecurso(rec);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoadingRecurso(false);
    }
  };

  const cargarHorarios = async () => {
    try {
      const data = await horariosApi.getByRecurso(Number(recursoId));
      setHorarios(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const cargarReservasDelDia = async () => {
    try {
      // Aquí deberías tener un endpoint para obtener reservas de un día específico
      // Por ahora simularemos
      setReservasExistentes([]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const getHorariosParaFecha = () => {
    if (!fecha) return [];
    const fechaDate = new Date(fecha + 'T00:00:00');
    const diaSemana = fechaDate.getDay() === 0 ? 6 : fechaDate.getDay() - 1;
    return horarios.filter(h => h.dia_semana === diaSemana);
  };

  const generarSlots = (horario: HorarioDisponible) => {
    const slots = [];
    const [horaInicioH, horaInicioM] = horario.hora_inicio.split(':').map(Number);
    const [horaFinH, horaFinM] = horario.hora_fin.split(':').map(Number);
    
    let minutosActuales = horaInicioH * 60 + horaInicioM;
    const minutosFin = horaFinH * 60 + horaFinM;
    
    while (minutosActuales < minutosFin) {
      const horas = Math.floor(minutosActuales / 60);
      const minutos = minutosActuales % 60;
      const horaStr = `${String(horas).padStart(2, '0')}:${String(minutos).padStart(2, '0')}`;
      
      // Verificar si está ocupado
      const estaOcupado = reservasExistentes.some(r => {
        const inicioReserva = new Date(r.fecha_hora_inicio).getHours() * 60 + 
                              new Date(r.fecha_hora_inicio).getMinutes();
        const finReserva = new Date(r.fecha_hora_fin).getHours() * 60 + 
                          new Date(r.fecha_hora_fin).getMinutes();
        return minutosActuales >= inicioReserva && minutosActuales < finReserva;
      });
      
      slots.push({
        hora: horaStr,
        precio: horario.precio,
        disponible: !estaOcupado
      });
      
      minutosActuales += horario.duracion_minutos;
    }
    
    return slots;
  };

  const handleReservar = async () => {
    if (!fecha || !horaSeleccionada || !recursoId) {
      alert('Selecciona fecha y hora');
      return;
    }

    const señaMonto = parseFloat(seña) || 0;
    if (señaMonto > precioSeleccionado) {
      alert('La seña no puede ser mayor al precio total');
      return;
    }

    setIsLoading(true);
    try {
      const fechaHoraInicio = `${fecha}T${horaSeleccionada}:00`;
      
      await reservasApi.crear({
        recurso_id: Number(recursoId),
        fecha_hora_inicio: fechaHoraInicio,
        duracion_minutos: 60,
        notas_cliente: undefined,
        seña: señaMonto > 0 ? señaMonto : undefined,
        metodo_pago: señaMonto > 0 ? metodoPago : undefined,
      });
      
      alert('¡Reserva creada exitosamente!');
      navigate('/cliente/mis-reservas');
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error al crear reserva');
    } finally {
      setIsLoading(false);
    }
  };

  if (loadingRecurso) return <Loading />;

  const horariosDisponibles = getHorariosParaFecha();
  const todosLosSlots = horariosDisponibles.flatMap(h => generarSlots(h));

  return (
    <Layout>
      <div className="max-w-2xl mx-auto">
        <button
          onClick={() => navigate('/cliente/buscar')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Volver a buscar
        </button>

        <h1 className="text-3xl font-bold mb-2">Crear Reserva</h1>
        {recurso && <p className="text-gray-600 mb-8">{recurso.nombre}</p>}
        
        <Card>
          <Input
            type="date"
            label="Fecha"
            value={fecha}
            onChange={(e) => {
              setFecha(e.target.value);
              setHoraSeleccionada('');
              setPrecioSeleccionado(0);
              setMostrarPago(false);
            }}
            min={new Date().toISOString().split('T')[0]}
          />

          {fecha && (
            <div className="mt-6">
              {horariosDisponibles.length === 0 ? (
                <div className="text-center py-8 bg-gray-50 rounded-lg">
                  <p className="text-gray-500">
                    No hay horarios disponibles para este día
                  </p>
                </div>
              ) : (
                <>
                  <h3 className="font-semibold mb-4">Horarios Disponibles</h3>
                  <div className="grid grid-cols-3 gap-2">
                    {todosLosSlots.map((slot, idx) => (
                      <button
                        key={idx}
                        disabled={!slot.disponible}
                        onClick={() => {
                          if (slot.disponible) {
                            setHoraSeleccionada(slot.hora);
                            setPrecioSeleccionado(slot.precio);
                            setMostrarPago(true);
                          }
                        }}
                        className={`p-3 rounded-lg border-2 transition-all ${
                          !slot.disponible
                            ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                            : horaSeleccionada === slot.hora
                            ? 'border-primary-600 bg-primary-50'
                            : 'border-gray-200 hover:border-primary-400'
                        }`}
                      >
                        <div className="text-sm font-medium">{slot.hora}</div>
                        <div className="text-xs text-gray-600">
                          {slot.disponible ? formatCurrency(slot.precio) : 'Ocupado'}
                        </div>
                      </button>
                    ))}
                  </div>

                  {todosLosSlots.every(s => !s.disponible) && (
                    <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg flex items-start gap-2">
                      <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                      <p className="text-sm text-yellow-800">
                        Todos los horarios están ocupados para este día. Prueba con otra fecha.
                      </p>
                    </div>
                  )}
                </>
              )}
            </div>
          )}

          {mostrarPago && horaSeleccionada && (
            <div className="mt-6 space-y-4">
              <div className="border-t pt-4">
                <h4 className="font-semibold mb-3">Información de Pago (Opcional)</h4>
                
                <div className="grid md:grid-cols-2 gap-4">
                  <Input
                    type="number"
                    label="Seña / Adelanto"
                    value={seña}
                    onChange={(e) => setSeña(e.target.value)}
                    placeholder="0"
                    min="0"
                    max={precioSeleccionado.toString()}
                    step="0.01"
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
                </div>

                {parseFloat(seña) > 0 && (
                  <div className="p-3 bg-blue-50 rounded-lg text-sm text-blue-800">
                    <p>Seña: {formatCurrency(parseFloat(seña))}</p>
                    <p>Saldo restante: {formatCurrency(precioSeleccionado - parseFloat(seña))}</p>
                  </div>
                )}
              </div>

              <div className="p-4 bg-primary-50 rounded-lg">
                <h4 className="font-semibold mb-2">Resumen:</h4>
                <p>Fecha: {new Date(fecha).toLocaleDateString('es-AR')}</p>
                <p>Horario: {horaSeleccionada}</p>
                <p className="text-lg font-bold mt-2">
                  Total: {formatCurrency(precioSeleccionado)}
                </p>
                {parseFloat(seña) > 0 && (
                  <p className="text-sm text-gray-600 mt-1">
                    A pagar ahora: {formatCurrency(parseFloat(seña))}
                  </p>
                )}
                <Button
                  onClick={handleReservar}
                  isLoading={isLoading}
                  className="w-full mt-4"
                >
                  Confirmar Reserva
                </Button>
              </div>
            </div>
          )}
        </Card>
      </div>
    </Layout>
  );
};