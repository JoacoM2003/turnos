import React, { useState, useEffect } from 'react';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Loading } from '../../components/common/Loading';
import { serviciosApi, recursosApi, proveedorApi } from '../../services/api';
import type { Servicio, Recurso } from '../../types';
import { Plus, Edit, Settings } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const MisServiciosPage: React.FC = () => {
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [servicioData, setServicioData] = useState({
    nombre: '',
    descripcion: '',
    categoria: '',
  });
  const navigate = useNavigate();

  useEffect(() => {
    cargarServicios();
  }, []);

  const cargarServicios = async () => {
    try {
      const data = await serviciosApi.getMisServicios();
      setServicios(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCrearServicio = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await proveedorApi.crearServicio(servicioData);
      setShowModal(false);
      setServicioData({ nombre: '', descripcion: '', categoria: '' });
      cargarServicios();
    } catch (error) {
      console.error('Error:', error);
      alert('Error al crear servicio');
    }
  };

  if (isLoading) return <Loading />;

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Mis Servicios</h1>
          <Button onClick={() => setShowModal(true)}>
            <Plus className="w-5 h-5 mr-2" />
            Nuevo Servicio
          </Button>
        </div>

        {servicios.length === 0 ? (
          <Card>
            <div className="text-center py-12">
              <p className="text-gray-500 mb-4">No tienes servicios creados</p>
              <Button onClick={() => setShowModal(true)}>
                Crear tu primer servicio
              </Button>
            </div>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 gap-6">
            {servicios.map((servicio) => (
              <Card key={servicio.id}>
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold">{servicio.nombre}</h3>
                    {servicio.descripcion && (
                      <p className="text-gray-600 mt-1">{servicio.descripcion}</p>
                    )}
                    {servicio.categoria && (
                      <span className="inline-block mt-2 px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                        {servicio.categoria}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex gap-2 mt-4">
                  <Button
                    variant="secondary"
                    onClick={() => navigate(`/proveedor/servicio/${servicio.id}/recursos`)}
                    className="flex-1"
                  >
                    Ver Recursos ({servicio.recursos_count || 0})
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Modal Crear Servicio */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="max-w-md w-full mx-4">
              <h2 className="text-2xl font-bold mb-4">Nuevo Servicio</h2>
              <form onSubmit={handleCrearServicio}>
                <Input
                  label="Nombre"
                  value={servicioData.nombre}
                  onChange={(e) => setServicioData({ ...servicioData, nombre: e.target.value })}
                  required
                  placeholder="Ej: Fútbol 5"
                />
                <Input
                  label="Descripción"
                  value={servicioData.descripcion}
                  onChange={(e) => setServicioData({ ...servicioData, descripcion: e.target.value })}
                  placeholder="Opcional"
                />
                <Input
                  label="Categoría"
                  value={servicioData.categoria}
                  onChange={(e) => setServicioData({ ...servicioData, categoria: e.target.value })}
                  placeholder="Ej: Deportes"
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