import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Layout } from '../../components/layout/Layout';
import { Card } from '../../components/common/Card';
import { Input } from '../../components/common/Input';
import { Button } from '../../components/common/Button';
import { authApi } from '../../services/api';
import { Users, Briefcase } from 'lucide-react';

type UserType = 'cliente' | 'proveedor';

export const RegisterPage: React.FC = () => {
  const [userType, setUserType] = useState<UserType>('cliente');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Campos comunes
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [telefono, setTelefono] = useState('');

  // Campos específicos de cliente
  const [dni, setDni] = useState('');

  // Campos específicos de proveedor
  const [especialidad, setEspecialidad] = useState('');
  const [matricula, setMatricula] = useState('');
  const [biografia, setBiografia] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      if (userType === 'cliente') {
        await authApi.registerCliente({
          email,
          password,
          username,
          nombre,
          apellido,
          telefono: telefono || undefined,
          dni: dni || undefined,
        });
      } else {
        if (!especialidad) {
          setError('La especialidad es requerida para proveedores');
          setIsLoading(false);
          return;
        }

        await authApi.registerProveedor({
          email,
          password,
          username,
          nombre,
          apellido,
          telefono: telefono || undefined,
          especialidad,
          matricula: matricula || undefined,
          biografia: biografia || undefined,
        });
      }

      // Registro exitoso, redirigir a login
      navigate('/login', {
        state: { message: 'Registro exitoso. Por favor inicia sesión.' },
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al registrarse');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto mt-8">
        <Card>
          <h1 className="text-2xl font-bold text-center mb-6">Crear Cuenta</h1>

          {/* Selector de tipo de usuario */}
          <div className="grid grid-cols-2 gap-4 mb-8">
            <button
              type="button"
              onClick={() => setUserType('cliente')}
              className={`p-6 border-2 rounded-lg transition-all ${
                userType === 'cliente'
                  ? 'border-primary-600 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <Users className={`w-12 h-12 mx-auto mb-2 ${
                userType === 'cliente' ? 'text-primary-600' : 'text-gray-400'
              }`} />
              <h3 className="font-semibold">Soy Cliente</h3>
              <p className="text-sm text-gray-600 mt-1">Quiero reservar servicios</p>
            </button>

            <button
              type="button"
              onClick={() => setUserType('proveedor')}
              className={`p-6 border-2 rounded-lg transition-all ${
                userType === 'proveedor'
                  ? 'border-primary-600 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <Briefcase className={`w-12 h-12 mx-auto mb-2 ${
                userType === 'proveedor' ? 'text-primary-600' : 'text-gray-400'
              }`} />
              <h3 className="font-semibold">Soy Proveedor</h3>
              <p className="text-sm text-gray-600 mt-1">Ofrezco servicios</p>
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Campos comunes */}
            <div className="grid md:grid-cols-2 gap-4">
              <Input
                type="email"
                label="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />

              <Input
                type="text"
                label="Nombre de usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />

              <Input
                type="password"
                label="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
              />

              <Input
                type="tel"
                label="Teléfono"
                value={telefono}
                onChange={(e) => setTelefono(e.target.value)}
                placeholder="Opcional"
              />

              <Input
                type="text"
                label="Nombre"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
              />

              <Input
                type="text"
                label="Apellido"
                value={apellido}
                onChange={(e) => setApellido(e.target.value)}
                required
              />
            </div>

            {/* Campos específicos de cliente */}
            {userType === 'cliente' && (
              <div className="mt-4">
                <Input
                  type="text"
                  label="DNI"
                  value={dni}
                  onChange={(e) => setDni(e.target.value)}
                  placeholder="Opcional - puedes completarlo después"
                />
              </div>
            )}

            {/* Campos específicos de proveedor */}
            {userType === 'proveedor' && (
              <div className="mt-4 space-y-4">
                <Input
                  type="text"
                  label="Especialidad"
                  value={especialidad}
                  onChange={(e) => setEspecialidad(e.target.value)}
                  required
                  placeholder="Ej: Fútbol 5, Tenis, Peluquería"
                />

                <Input
                  type="text"
                  label="Matrícula Profesional"
                  value={matricula}
                  onChange={(e) => setMatricula(e.target.value)}
                  placeholder="Opcional"
                />

                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Biografía
                  </label>
                  <textarea
                    value={biografia}
                    onChange={(e) => setBiografia(e.target.value)}
                    className="input-field min-h-[100px]"
                    placeholder="Cuéntanos sobre tu experiencia..."
                  />
                </div>
              </div>
            )}

            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                {error}
              </div>
            )}

            <Button type="submit" isLoading={isLoading} className="w-full mt-6">
              Registrarse
            </Button>

            <p className="text-center text-sm text-gray-600 mt-4">
              ¿Ya tienes cuenta?{' '}
              <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
                Inicia sesión aquí
              </Link>
            </p>
          </form>
        </Card>
      </div>
    </Layout>
  );
};
