import React from 'react';
import { Layout } from '../../components/layout/Layout';
import { LoginForm } from '../../components/auth/LoginForm';
import { Card } from '../../components/common/Card';

export const LoginPage: React.FC = () => {
  return (
    <Layout>
      <div className="max-w-md mx-auto mt-12">
        <Card>
          <h1 className="text-2xl font-bold text-center mb-6">Iniciar Sesión</h1>
          <LoginForm />
        </Card>
      </div>
    </Layout>
  );
};