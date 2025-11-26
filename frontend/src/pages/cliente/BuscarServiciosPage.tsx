import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Input } from '../../components/common/Input';
import { Loading } from '../../components/common/Loading';
import { serviciosApi, recursosApi } from '../../services/api';
import type { Servicio, Recurso } from '../../types';
import { Search, MapPin, Users } from 'lucide-react';

export const BuscarServiciosPage: React.FC = () => {
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [selectedServicio, setSelectedServicio] = useState<Servicio | null>(null);
  const [recursos, setRecursos] = useState<Recurso[]>([]);
  const [busqueda, setBusqueda] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    cargarServicios();
  }, []);

  const cargarServicios = async () => {
    try {
      const data = await serviciosApi.buscar();
      setServicios(data);
    } catch (error) {
      console.error('Error al cargar servicios:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const cargarRecursos = async (servicioId: number) => {
    try {
      const data = await recursosApi.getByServicio(servicioId);
      setRecursos(data);
    } catch (error) {
      console.error('Error al cargar recursos:', error);
    }
  };

  const handleSelectServicio = async (servicio: Servicio) => {
    setSelectedServicio(servicio);
    await cargarRecursos(servicio.id);
  };

  const serviciosFiltrados = servicios.filter((s) =>
    s.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
    s.descripcion?.toLowerCase().includes(busqueda.toLowerCase())
  );

  if (isLoading) {
    return <Loading />;
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Buscar Servicios</h1>

        {/* Buscador */}
        <div className="mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar servicios..."
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
              className="input-field pl-10"
            />
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Lista de servicios */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Servicios Disponibles</h2>
            <div className="space-y-4">
              {serviciosFiltrados.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No se encontraron servicios</p>
              ) : (
                serviciosFiltrados.map((servicio) => (
                  <Card
                    key={servicio.id}
                    onClick={() => handleSelectServicio(servicio)}
                    className={selectedServicio?.id === servicio.id ? 'ring-2 ring-primary-500' : ''}
                  >
                    <h3 className="font-semibold text-lg">{servicio.nombre}</h3>
                    {servicio.descripcion && (
                      <p className="text-gray-600 text-sm mt-1">{servicio.descripcion}</p>
                    )}
                    {servicio.categoria && (
                      <span className="inline-block mt-2 px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                        {servicio.categoria}
                      </span>
                    )}
                  </Card>
                ))
              )}
            </div>
          </div>

          {/* Recursos del servicio seleccionado */}
          <div>
            {selectedServicio ? (
              <>
                <h2 className="text-xl font-semibold mb-4">
                  {selectedServicio.nombre} - Recursos
                </h2>
                <div className="space-y-4">
                  {recursos.length === 0 ? (
                    <Card>
                      <p className="text-gray-500 text-center">No hay recursos disponibles</p>
                    </Card>
                  ) : (
                    recursos.map((recurso) => (
                      <Card key={recurso.id}>
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="font-semibold">{recurso.nombre}</h3>
                            {recurso.descripcion && (
                              <p className="text-gray-600 text-sm mt-1">{recurso.descripcion}</p>
                            )}
                            {recurso.capacidad && (
                              <div className="flex items-center gap-2 mt-2 text-sm text-gray-500">
                                <Users className="w-4 h-4" />
                                <span>Capacidad: {recurso.capacidad} personas</span>
                              </div>
                            )}
                          </div>
                          <button
                            onClick={() => navigate(`/cliente/reservar/${recurso.id}`)}
                            className="btn-primary ml-4"
                          >
                            Reservar
                          </button>
                        </div>
                      </Card>
                    ))
                  )}
                </div>
              </>
            ) : (
              <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                <p className="text-gray-500">Selecciona un servicio para ver recursos</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};
