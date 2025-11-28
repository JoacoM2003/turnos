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
import { ArrowLeft, AlertCircle, DollarSign, CheckCircle } from 'lucide-react';
import api from '../../services/api';

export const CrearReservaPage: React.FC = () => {
  const { recursoId } = useParams();
  const navigate = useNavigate();
  const [recurso, setRecurso] = useState<Recurso | null>(null);
  const [horarios, setHorarios] = useState<HorarioDisponible[]>([]);
  const [horariosOcupados, setHorariosOcupados] = useState<string[]>([]);
  const [fecha, setFecha] = useState('');
  const [horaSeleccionada, setHoraSeleccionada] = useState('');
  const [precioSeleccionado, setPrecioSeleccionado] = useState(0);
  
  // Pago
  const [mostrarPago, setMostrarPago] = useState(false);
  const [tipoPago, setTipoPago] = useState<'completo' | 'seña'>('completo');
  const [montoSeña, setMontoSeña] = useState('');
  const [metodoPago, setMetodoPago] = useState('efectivo');
  
  const [isLoading, setIsLoading] = useState(false);
  const [loadingRecurso, setLoadingRecurso] = useState(true);

  useEffect(() => {
    cargarRecurso();
    cargarHorarios();
  }, [recursoId]);

  useEffect(() => {
    if (fecha) {
      cargarDisponibilidad();
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

  const cargarDisponibilidad = async () => {
    try {
      const response = await api.get(`/reservas/recurso/${recursoId}/disponibilidad`, {
        params: { fecha }
      });
      
      // Extraer las horas ocupadas
      const ocupados = response.data.map((r: any) => r.hora_inicio);
      setHorariosOcupados(ocupados);
    } catch (error) {
      console.error('Error al cargar disponibilidad:', error);
      setHorariosOcupados([]);
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
      
      const estaOcupado = horariosOcupados.includes(horaStr);
      
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

    let señaMonto = 0;
    if (tipoPago === 'seña') {
      señaMonto = parseFloat(montoSeña) || 0;
      if (señaMonto <= 0) {
        alert('Ingresa un monto de seña válido');
        return;
      }
      if (señaMonto > precioSeleccionado) {
        alert('La seña no puede ser mayor al precio total');
        return;
      }
    } else {
      // Pago completo
      señaMonto = precioSeleccionado;
    }

    setIsLoading(true);
    try {
      const fechaHoraInicio = `${fecha}T${horaSeleccionada}:00`;
      
      await reservasApi.crear({
        recurso_id: Number(recursoId),
        fecha_hora_inicio: fechaHoraInicio,
        duracion_minutos: 60,
        notas_cliente: undefined,
        seña: señaMonto,
        metodo_pago: metodoPago,
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
                    No hay horarios disponibles para {DIAS_SEMANA[new Date(fecha + 'T00:00:00').getDay() === 0 ? 6 : new Date(fecha + 'T00:00:00').getDay() - 1]}
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
                            setTipoPago('completo');
                            setMontoSeña('');
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
                <h4 className="font-semibold mb-3 flex items-center gap-2">
                  <DollarSign className="w-5 h-5 text-primary-600" />
                  Información de Pago
                </h4>
                
                {/* Tipo de pago */}
                <div className="grid grid-cols-2 gap-3 mb-4">
                  <button
                    type="button"
                    onClick={() => setTipoPago('completo')}
                    className={`p-4 border-2 rounded-lg transition-all ${
                      tipoPago === 'completo'
                        ? 'border-green-600 bg-green-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <CheckCircle className={`w-6 h-6 mx-auto mb-2 ${
                      tipoPago === 'completo' ? 'text-green-600' : 'text-gray-400'
                    }`} />
                    <div className="font-semibold text-sm">Pago Completo</div>
                    <div className="text-xs text-gray-600 mt-1">
                      {formatCurrency(precioSeleccionado)}
                    </div>
                  </button>

                  <button
                    type="button"
                    onClick={() => setTipoPago('seña')}
                    className={`p-4 border-2 rounded-lg transition-all ${
                      tipoPago === 'seña'
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <DollarSign className={`w-6 h-6 mx-auto mb-2 ${
                      tipoPago === 'seña' ? 'text-primary-600' : 'text-gray-400'
                    }`} />
                    <div className="font-semibold text-sm">Seña / Adelanto</div>
                    <div className="text-xs text-gray-600 mt-1">
                      Pagar el resto después
                    </div>
                  </button>
                </div>

                {tipoPago === 'seña' && (
                  <div className="mb-4">
                    <Input
                      type="number"
                      label="Monto de la seña"
                      value={montoSeña}
                      onChange={(e) => setMontoSeña(e.target.value)}
                      placeholder="0"
                      min="0"
                      max={precioSeleccionado.toString()}
                      step="0.01"
                      required
                    />
                    {parseFloat(montoSeña) > 0 && parseFloat(montoSeña) <= precioSeleccionado && (
                      <div className="mt-2 p-2 bg-blue-50 rounded text-sm text-blue-800">
                        Saldo restante: {formatCurrency(precioSeleccionado - parseFloat(montoSeña))}
                      </div>
                    )}
                  </div>
                )}

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

              <div className="p-4 bg-primary-50 rounded-lg border border-primary-200">
                <h4 className="font-semibold mb-2">Resumen:</h4>
                <div className="space-y-1 text-sm">
                  <p><strong>Fecha:</strong> {new Date(fecha).toLocaleDateString('es-AR')}</p>
                  <p><strong>Horario:</strong> {horaSeleccionada}</p>
                  <p><strong>Precio total:</strong> {formatCurrency(precioSeleccionado)}</p>
                  {tipoPago === 'completo' ? (
                    <p className="text-green-700 font-semibold">
                      ✓ Pago completo: {formatCurrency(precioSeleccionado)}
                    </p>
                  ) : (
                    <>
                      <p><strong>Seña a pagar ahora:</strong> {formatCurrency(parseFloat(montoSeña) || 0)}</p>
                      <p className="text-orange-700">
                        <strong>Saldo pendiente:</strong> {formatCurrency(precioSeleccionado - (parseFloat(montoSeña) || 0))}
                      </p>
                    </>
                  )}
                </div>
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