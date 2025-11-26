import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { LogOut, User, Calendar } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <Calendar className="w-8 h-8 text-primary-600" />
            <span className="text-xl font-bold text-gray-900">Sistema de Reservas</span>
          </Link>

          {/* Navigation */}
          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <>
                {user?.role === 'cliente' && (
                  <>
                    <Link to="/cliente/buscar" className="text-gray-700 hover:text-primary-600 transition-colors">
                      Buscar Servicios
                    </Link>
                    <Link to="/cliente/mis-reservas" className="text-gray-700 hover:text-primary-600 transition-colors">
                      Mis Reservas
                    </Link>
                  </>
                )}
                
                {user?.role === 'proveedor' && (
                  <>
                    <Link to="/proveedor/servicios" className="text-gray-700 hover:text-primary-600 transition-colors">
                      Mis Servicios
                    </Link>
                    <Link to="/proveedor/reservas" className="text-gray-700 hover:text-primary-600 transition-colors">
                      Reservas
                    </Link>
                  </>
                )}

                <div className="flex items-center gap-2 ml-4 pl-4 border-l border-gray-300">
                  <User className="w-5 h-5 text-gray-600" />
                  <span className="text-sm text-gray-700">{user?.username}</span>
                  <span className="text-xs px-2 py-1 bg-primary-100 text-primary-700 rounded-full">
                    {user?.role}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="ml-2 p-2 text-gray-600 hover:text-red-600 transition-colors"
                    title="Cerrar sesión"
                  >
                    <LogOut className="w-5 h-5" />
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-primary-600 transition-colors">
                  Iniciar Sesión
                </Link>
                <Link
                  to="/register"
                  className="btn-primary"
                >
                  Registrarse
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};