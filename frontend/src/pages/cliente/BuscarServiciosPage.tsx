import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Input } from '../../components/common/Input';
import { Loading } from '../../components/common/Loading';
import { proveedoresApi, serviciosApi, recursosApi } from '../../services/api';
import type { Proveedor, Servicio, Recurso } from '../../types';
import { Search, Users, ArrowLeft } from 'lucide-react';

export const BuscarServiciosPage: React.FC = () => {
  const [proveedores, setProveedores] = useState<Proveedor[]>([]);
  const [selectedProveedor, setSelectedProveedor] = useState<Proveedor | null>(null);
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [selectedServicio, setSelectedServicio] = useState<Servicio | null>(null);
  const [recursos, setRecursos] = useState<Recurso[]>([]);
  const [busqueda, setBusqueda] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    cargarProveedores();
  }, []);

  const cargarProveedores = async () => {
    try {
      const data = await proveedoresApi.listar();
      setProveedores(data);
    } catch (error) {
      console.error('Error al cargar proveedores:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const cargarServiciosProveedor = async (proveedorId: number) => {
    try {
      const data = await serviciosApi.getByProveedor(proveedorId);
      setServicios(data);
    } catch (error) {
      console.error('Error al cargar servicios:', error);
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

  const handleSelectProveedor = async (proveedor: Proveedor) => {
    setSelectedProveedor(proveedor);
    setSelectedServicio(null);
    setRecursos([]);
    await cargarServiciosProveedor(proveedor.id);
  };

  const handleSelectServicio = async (servicio: Servicio) => {
    setSelectedServicio(servicio);
    await cargarRecursos(servicio.id);
  };

  const handleVolver = () => {
    if (selectedServicio) {
      setSelectedServicio(null);
      setRecursos([]);
    } else if (selectedProveedor) {
      setSelectedProveedor(null);
      setServicios([]);
    }
  };

  const proveedoresFiltrados = proveedores.filter((p) =>
    p.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
    p.especialidad?.toLowerCase().includes(busqueda.toLowerCase())
  );

  if (isLoading) return <Loading />;

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-4 mb-8">
          {(selectedProveedor || selectedServicio) && (
            <button
              onClick={handleVolver}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="w-5 h-5" />
              Volver
            </button>
          )}
          <h1 className="text-3xl font-bold">
            {!selectedProveedor && 'Seleccionar Proveedor'}
            {selectedProveedor && !selectedServicio && `Servicios de ${selectedProveedor.nombre}`}
            {selectedServicio && `Recursos de ${selectedServicio.nombre}`}
          </h1>
        </div>

        {/* PASO 1: Seleccionar Proveedor */}
        {!selectedProveedor && (
          <>
            <div className="mb-8">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Buscar proveedores..."
                  value={busqueda}
                  onChange={(e) => setBusqueda(e.target.value)}
                  className="input-field pl-10"
                />
              </div>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {proveedoresFiltrados.length === 0 ? (
                <p className="text-gray-500 text-center col-span-full py-8">
                  No se encontraron proveedores
                </p>
              ) : (
                proveedoresFiltrados.map((proveedor) => (
                  <Card
                    key={proveedor.id}
                    onClick={() => handleSelectProveedor(proveedor)}
                  >
                    <div className="flex items-start gap-3">
                      <Users className="w-10 h-10 text-primary-600 flex-shrink-0" />
                      <div>
                        <h3 className="font-semibold text-lg">{proveedor.nombre}</h3>
                        <p className="text-sm text-primary-600">{proveedor.especialidad}</p>
                        {proveedor.biografia && (
                          <p className="text-sm text-gray-600 mt-2">{proveedor.biografia}</p>
                        )}
                      </div>
                    </div>
                  </Card>
                ))
              )}
            </div>
          </>
        )}

        {/* PASO 2: Seleccionar Servicio */}
        {selectedProveedor && !selectedServicio && (
          <div className="grid md:grid-cols-2 gap-6">
            {servicios.length === 0 ? (
              <p className="text-gray-500 text-center col-span-full py-8">
                Este proveedor no tiene servicios disponibles
              </p>
            ) : (
              servicios.map((servicio) => (
                <Card
                  key={servicio.id}
                  onClick={() => handleSelectServicio(servicio)}
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
        )}

        {/* PASO 3: Ver Recursos y Reservar */}
        {selectedServicio && (
          <div className="grid md:grid-cols-2 gap-6">
            {recursos.length === 0 ? (
              <p className="text-gray-500 text-center col-span-full py-8">
                No hay recursos disponibles
              </p>
            ) : (
              recursos.map((recurso) => (
                <Card key={recurso.id}>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">{recurso.nombre}</h3>
                      {recurso.descripcion && (
                        <p className="text-gray-600 text-sm mt-1">{recurso.descripcion}</p>
                      )}
                      {recurso.capacidad && (
                        <div className="flex items-center gap-2 mt-2 text-sm text-gray-500">
                          <Users className="w-4 h-4" />
                          <span>Capacidad: {recurso.capacidad} personas</span>
                        </div>
                      )}
                      {recurso.caracteristicas && (
                        <p className="text-sm text-gray-500 mt-1">{recurso.caracteristicas}</p>
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
        )}
      </div>
    </Layout>
  );
};