import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/auth/ProtectedRoute';

// Pages
import { HomePage } from './pages/public/HomePage';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';

// Cliente
import { BuscarServiciosPage } from './pages/cliente/BuscarServiciosPage';
import { MisReservasPage } from './pages/cliente/MisReservasPage';
import { CrearReservaPage } from './pages/cliente/CrearReservaPage';

// Proveedor
import { MisServiciosPage } from './pages/proveedor/MisServiciosPage';
import { RecursosPage } from './pages/proveedor/RecursosPage';
import { ConfigurarHorariosPage } from './pages/proveedor/ConfigurarHorariosPage';
import { ReservasProveedorPage } from './pages/proveedor/ReservasProveedorPage';
import { ReservasPorRecursoPage } from './pages/proveedor/ReservasPorRecursoPage';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Cliente Routes */}
          <Route
            path="/cliente/buscar"
            element={
              <ProtectedRoute requiredRole="cliente">
                <BuscarServiciosPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/cliente/mis-reservas"
            element={
              <ProtectedRoute requiredRole="cliente">
                <MisReservasPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/cliente/reservar/:recursoId"
            element={
              <ProtectedRoute requiredRole="cliente">
                <CrearReservaPage />
              </ProtectedRoute>
            }
          />

          {/* Proveedor Routes */}
          <Route
            path="/proveedor/servicios"
            element={
              <ProtectedRoute requiredRole="proveedor">
                <MisServiciosPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/proveedor/servicio/:servicioId/recursos"
            element={
              <ProtectedRoute requiredRole="proveedor">
                <RecursosPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/proveedor/recurso/:recursoId/horarios"
            element={
              <ProtectedRoute requiredRole="proveedor">
                <ConfigurarHorariosPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/proveedor/reservas"
            element={
              <ProtectedRoute requiredRole="proveedor">
                <ReservasProveedorPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/proveedor/reservas-por-recurso"
            element={
              <ProtectedRoute requiredRole="proveedor">
                <ReservasPorRecursoPage />
              </ProtectedRoute>
            }
          />

          {/* 404 */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;