import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Loading } from '../../components/common/Loading';
import { recursosApi, horariosApi, proveedorApi } from '../../services/api';
import type { Recurso, HorarioDisponible } from '../../types';
import { ArrowLeft, Plus, Edit2, Trash2, X } from 'lucide-react';
import { DIAS_SEMANA } from '../../utils/constants';
import { formatTime, formatCurrency } from '../../utils/formatters';

export const ConfigurarHorariosPage: React.FC = () => {
  const { recursoId } = useParams();
  const navigate = useNavigate();
  const [recurso, setRecurso] = useState<Recurso | null>(null);
  const [horarios, setHorarios] = useState<HorarioDisponible[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editingHorario, setEditingHorario] = useState<HorarioDisponible | null>(null);
  
  const [horarioData, setHorarioData] = useState({
    dias_semana: [] as number[],
    hora_inicio: '09:00',
    hora_fin: '22:00',
    precio: '',
    duracion_minutos: '60',
  });

  useEffect(() => {
    cargarDatos();
  }, [recursoId]);

  const cargarDatos = async () => {
    try {
      const [recursoData, horariosData] = await Promise.all([
        recursosApi.getByServicio(1).then(recursos => recursos.find(r => r.id === Number(recursoId))),
        horariosApi.getByRecurso(Number(recursoId)),
      ]);
      if (recursoData) setRecurso(recursoData);
      setHorarios(horariosData);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setHorarioData({
      dias_semana: [],
      hora_inicio: '09:00',
      hora_fin: '22:00',
      precio: '',
      duracion_minutos: '60',
    });
    setIsEditing(false);
    setEditingHorario(null);
  };

  const toggleDia = (dia: number) => {
    setHorarioData(prev => ({
      ...prev,
      dias_semana: prev.dias_semana.includes(dia)
        ? prev.dias_semana.filter(d => d !== dia)
        : [...prev.dias_semana, dia]
    }));
  };

  const handleCrearHorarios = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (horarioData.dias_semana.length === 0) {
      alert('Selecciona al menos un día');
      return;
    }

    try {
      await proveedorApi.crearHorariosBulk({
        recurso_id: Number(recursoId),
        dias_semana: horarioData.dias_semana,
        hora_inicio: horarioData.hora_inicio + ':00',
        hora_fin: horarioData.hora_fin + ':00',
        precio: Number(horarioData.precio),
        duracion_minutos: Number(horarioData.duracion_minutos),
      });
      
      setShowModal(false);
      resetForm();
      cargarDatos();
      alert('Horarios creados exitosamente');
    } catch (error: any) {
      console.error('Error:', error);
      alert(error.response?.data?.detail || 'Error al crear horarios');
    }
  };

  const handleEditarHorario = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!editingHorario) return;

    try {
      await horariosApi.actualizar(editingHorario.id, {
        recurso_id: Number(recursoId),
        dia_semana: horarioData.dias_semana[0],
        hora_inicio: horarioData.hora_inicio + ':00',
        hora_fin: horarioData.hora_fin + ':00',
        precio: Number(horarioData.precio),
        duracion_minutos: Number(horarioData.duracion_minutos),
      });
      
      setShowModal(false);
      resetForm();
      cargarDatos();
      alert('Horario actualizado exitosamente');
    } catch (error: any) {
      console.error('Error:', error);
      alert(error.response?.data?.detail || 'Error al actualizar horario');
    }
  };

  const handleAbrirEditar = (horario: HorarioDisponible) => {
    setIsEditing(true);
    setEditingHorario(horario);
    setHorarioData({
      dias_semana: [horario.dia_semana],
      hora_inicio: horario.hora_inicio.substring(0, 5),
      hora_fin: horario.hora_fin.substring(0, 5),
      precio: horario.precio.toString(),
      duracion_minutos: horario.duracion_minutos.toString(),
    });
    setShowModal(true);
  };

  const handleEliminar = async (id: number) => {
    if (!confirm('¿Seguro que quieres eliminar este horario?')) return;

    try {
      await horariosApi.eliminar(id);
      cargarDatos();
      alert('Horario eliminado');
    } catch (error) {
      console.error('Error:', error);
      alert('Error al eliminar horario');
    }
  };

  // Agrupar horarios por día
  const horariosPorDia = horarios.reduce((acc, horario) => {
    if (!acc[horario.dia_semana]) {
      acc[horario.dia_semana] = [];
    }
    acc[horario.dia_semana].push(horario);
    return acc;
  }, {} as Record<number, HorarioDisponible[]>);

  if (isLoading) return <Loading />;

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Volver
        </button>

        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold">{recurso?.nombre}</h1>
            <p className="text-gray-600">Configuración de Horarios y Precios</p>
          </div>
          <Button onClick={() => { resetForm(); setShowModal(true); }}>
            <Plus className="w-5 h-5 mr-2" />
            Agregar Horarios
          </Button>
        </div>

        {Object.keys(horariosPorDia).length === 0 ? (
          <Card>
            <div className="text-center py-12">
              <p className="text-gray-500 mb-4">No hay horarios configurados</p>
              <p className="text-sm text-gray-400 mb-4">
                Los clientes necesitan horarios disponibles para poder hacer reservas
              </p>
              <Button onClick={() => setShowModal(true)}>
                Configurar horarios
              </Button>
            </div>
          </Card>
        ) : (
          <div className="space-y-4">
            {Object.entries(horariosPorDia).map(([dia, horariosDelDia]) => (
              <Card key={dia}>
                <h3 className="font-semibold text-lg mb-3">
                  {DIAS_SEMANA[Number(dia)]}
                </h3>
                <div className="space-y-2">
                  {horariosDelDia.map((horario) => (
                    <div key={horario.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <div>
                        <span className="font-medium">
                          {formatTime(horario.hora_inicio)} - {formatTime(horario.hora_fin)}
                        </span>
                        <span className="text-gray-600 ml-4">
                          {horario.duracion_minutos} min
                        </span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="font-semibold text-primary-600">
                          {formatCurrency(horario.precio)}
                        </span>
                        <button
                          onClick={() => handleAbrirEditar(horario)}
                          className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                          title="Editar"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleEliminar(horario.id)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                          title="Eliminar"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Modal Crear/Editar Horarios */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <Card className="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">
                  {isEditing ? 'Editar Horario' : 'Configurar Horarios'}
                </h2>
                <button
                  onClick={() => { setShowModal(false); resetForm(); }}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <form onSubmit={isEditing ? handleEditarHorario : handleCrearHorarios}>
                {/* Selector de días */}
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {isEditing ? 'Día de la semana' : 'Días de la semana'} <span className="text-red-500">*</span>
                  </label>
                  {isEditing ? (
                    <div className="p-3 bg-gray-100 rounded-lg font-medium">
                      {DIAS_SEMANA[horarioData.dias_semana[0]]}
                    </div>
                  ) : (
                    <div className="grid grid-cols-7 gap-2">
                      {DIAS_SEMANA.map((dia, index) => (
                        <button
                          key={index}
                          type="button"
                          onClick={() => toggleDia(index)}
                          className={`p-2 text-sm rounded-lg border-2 transition-all ${
                            horarioData.dias_semana.includes(index)
                              ? 'border-primary-600 bg-primary-50 text-primary-700'
                              : 'border-gray-300 hover:border-gray-400'
                          }`}
                        >
                          {dia.slice(0, 3)}
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <Input
                    type="time"
                    label="Hora inicio"
                    value={horarioData.hora_inicio}
                    onChange={(e) => setHorarioData({ ...horarioData, hora_inicio: e.target.value })}
                    required
                  />
                  <Input
                    type="time"
                    label="Hora fin"
                    value={horarioData.hora_fin}
                    onChange={(e) => setHorarioData({ ...horarioData, hora_fin: e.target.value })}
                    required
                  />
                  <Input
                    type="number"
                    label="Precio por turno"
                    value={horarioData.precio}
                    onChange={(e) => setHorarioData({ ...horarioData, precio: e.target.value })}
                    required
                    min="0"
                    step="0.01"
                  />
                  <Input
                    type="number"
                    label="Duración (minutos)"
                    value={horarioData.duracion_minutos}
                    onChange={(e) => setHorarioData({ ...horarioData, duracion_minutos: e.target.value })}
                    required
                    min="15"
                    step="15"
                  />
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
                  <p className="text-sm text-blue-800">
                    <strong>Ejemplo:</strong> Si configuras de 10:00 a 22:00 con duración de 60 minutos,
                    se generarán slots de 10:00-11:00, 11:00-12:00, etc.
                  </p>
                </div>

                <div className="flex gap-2 mt-6">
                  <Button type="submit" className="flex-1">
                    {isEditing ? 'Actualizar' : 'Crear Horarios'}
                  </Button>
                  <Button
                    type="button"
                    variant="secondary"
                    onClick={() => { setShowModal(false); resetForm(); }}
                    className="flex-1"
                  >
                    Cancelar
                  </Button>
                </div>
              </form>
            </Card>
          </div>
        )}
      </div>
    </Layout>
  );
};