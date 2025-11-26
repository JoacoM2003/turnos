import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { useAuth } from '../../hooks/useAuth';
import { Calendar, Users, Clock, CheckCircle } from 'lucide-react';
import { Button } from '../../components/common/Button';

export const HomePage: React.FC = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();

  React.useEffect(() => {
    if (isAuthenticated) {
      if (user?.role === 'cliente') {
        navigate('/cliente/buscar');
      } else if (user?.role === 'proveedor') {
        navigate('/proveedor/servicios');
      }
    }
  }, [isAuthenticated, user, navigate]);

  return (
    <Layout>
      <div className="text-center py-20">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Sistema de Reservas
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Gestiona tus reservas de forma simple y eficiente
        </p>

        <div className="flex justify-center gap-4 mb-16">
          <Button onClick={() => navigate('/register')} className="text-lg px-8 py-3">
            Comenzar Ahora
          </Button>
          <Button
            onClick={() => navigate('/login')}
            variant="secondary"
            className="text-lg px-8 py-3"
          >
            Iniciar Sesión
          </Button>
        </div>

        <div className="grid md:grid-cols-4 gap-8 max-w-5xl mx-auto">
          <div className="text-center">
            <Calendar className="w-12 h-12 text-primary-600 mx-auto mb-4" />
            <h3 className="font-semibold text-gray-900 mb-2">Fácil Reserva</h3>
            <p className="text-gray-600 text-sm">Reserva en pocos clicks</p>
          </div>

          <div className="text-center">
            <Users className="w-12 h-12 text-primary-600 mx-auto mb-4" />
            <h3 className="font-semibold text-gray-900 mb-2">Para Proveedores</h3>
            <p className="text-gray-600 text-sm">Gestiona tu negocio</p>
          </div>

          <div className="text-center">
            <Clock className="w-12 h-12 text-primary-600 mx-auto mb-4" />
            <h3 className="font-semibold text-gray-900 mb-2">Tiempo Real</h3>
            <p className="text-gray-600 text-sm">Disponibilidad actualizada</p>
          </div>

          <div className="text-center">
            <CheckCircle className="w-12 h-12 text-primary-600 mx-auto mb-4" />
            <h3 className="font-semibold text-gray-900 mb-2">Confirmación</h3>
            <p className="text-gray-600 text-sm">Notificaciones instantáneas</p>
          </div>
        </div>
      </div>
    </Layout>
  );
};