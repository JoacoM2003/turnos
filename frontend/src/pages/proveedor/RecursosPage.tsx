import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Loading } from '../../components/common/Loading';
import { recursosApi, proveedorApi, serviciosApi } from '../../services/api';
import type { Recurso, Servicio } from '../../types';
import { Plus, Settings, ArrowLeft } from 'lucide-react';

export const RecursosPage: React.FC = () => {
  const { servicioId } = useParams();
  const navigate = useNavigate();
  const [servicio, setServicio] = useState<Servicio | null>(null);
  const [recursos, setRecursos] = useState<Recurso[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [recursoData, setRecursoData] = useState({
    nombre: '',
    descripcion: '',
    capacidad: '',
    caracteristicas: '',
  });

  useEffect(() => {
    cargarDatos();
  }, [servicioId]);

  const cargarDatos = async () => {
    try {
      const [servicioData, recursosData] = await Promise.all([
        serviciosApi.getById(Number(servicioId)),
        recursosApi.getByServicio(Number(servicioId)),
      ]);
      setServicio(servicioData);
      setRecursos(recursosData);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCrearRecurso = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await proveedorApi.crearRecurso({
        servicio_id: Number(servicioId),
        nombre: recursoData.nombre,
        descripcion: recursoData.descripcion || undefined,
        capacidad: recursoData.capacidad ? Number(recursoData.capacidad) : undefined,
        caracteristicas: recursoData.caracteristicas || undefined,
      });
      setShowModal(false);
      setRecursoData({ nombre: '', descripcion: '', capacidad: '', caracteristicas: '' });
      cargarDatos();
    } catch (error) {
      console.error('Error:', error);
      alert('Error al crear recurso');
    }
  };

  if (isLoading) return <Loading />;

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <button
          onClick={() => navigate('/proveedor/servicios')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          Volver a servicios
        </button>

        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold">{servicio?.nombre}</h1>
            <p className="text-gray-600">Recursos/Instalaciones</p>
          </div>
          <Button onClick={() => setShowModal(true)}>
            <Plus className="w-5 h-5 mr-2" />
            Nuevo Recurso
          </Button>
        </div>

        {recursos.length === 0 ? (
          <Card>
            <div className="text-center py-12">
              <p className="text-gray-500 mb-4">No tienes recursos creados</p>
              <Button onClick={() => setShowModal(true)}>
                Crear tu primer recurso
              </Button>
            </div>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 gap-6">
            {recursos.map((recurso) => (
              <Card key={recurso.id}>
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold">{recurso.nombre}</h3>
                    {recurso.descripcion && (
                      <p className="text-gray-600 mt-1">{recurso.descripcion}</p>
                    )}
                    {recurso.capacidad && (
                      <p className="text-sm text-gray-500 mt-2">
                        Capacidad: {recurso.capacidad} personas
                      </p>
                    )}
                    {recurso.caracteristicas && (
                      <p className="text-sm text-gray-500">
                        {recurso.caracteristicas}
                      </p>
                    )}
                  </div>
                </div>

                <div className="mt-4">
                  <Button
                    variant="secondary"
                    onClick={() => navigate(`/proveedor/recurso/${recurso.id}/horarios`)}
                    className="w-full"
                  >
                    <Settings className="w-4 h-4 mr-2" />
                    Configurar Horarios
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Modal Crear Recurso */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="max-w-md w-full mx-4">
              <h2 className="text-2xl font-bold mb-4">Nuevo Recurso</h2>
              <form onSubmit={handleCrearRecurso}>
                <Input
                  label="Nombre"
                  value={recursoData.nombre}
                  onChange={(e) => setRecursoData({ ...recursoData, nombre: e.target.value })}
                  required
                  placeholder="Ej: Cancha 1"
                />
                <Input
                  label="Descripción"
                  value={recursoData.descripcion}
                  onChange={(e) => setRecursoData({ ...recursoData, descripcion: e.target.value })}
                  placeholder="Opcional"
                />
                <Input
                  type="number"
                  label="Capacidad"
                  value={recursoData.capacidad}
                  onChange={(e) => setRecursoData({ ...recursoData, capacidad: e.target.value })}
                  placeholder="Cantidad de personas"
                />
                <Input
                  label="Características"
                  value={recursoData.caracteristicas}
                  onChange={(e) => setRecursoData({ ...recursoData, caracteristicas: e.target.value })}
                  placeholder="Ej: Techada, vestuarios, estacionamiento"
                />
                <div className="flex gap-2 mt-6">
                  <Button type="submit" className="flex-1">
                    Crear
                  </Button>
                  <Button
                    type="button"
                    variant="secondary"
                    onClick={() => setShowModal(false)}
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