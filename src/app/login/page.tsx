'use client';

import { useState } from 'react';
import { useAuth, createUserProfile } from '@/context/AuthContext';
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
} from 'firebase/auth';

// Componente de Login/Registro
export default function LoginPage() {
  const { auth } = useAuth();
  const [isLoginView, setIsLoginView] = useState(true); // true = Entrar, false = Registar
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [loading, setLoading] = useState(false);

  const redirect = () => {
    // A especificação pede para usar window.location.href para evitar conflitos de compilação
    window.location.href = '/dashBoard';
  };

  const handleRegister = async () => {
    setErrorMsg('');
    setLoading(true);
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      // Cria o perfil do usuário no Firestore
      await createUserProfile(userCredential.user);
      redirect();
    } catch (error: any) {
      console.error('Erro no registo:', error);
      setErrorMsg(error.message.includes('email-already-in-use') ? 'Este email já está em uso.' : 'Erro ao registar. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    setErrorMsg('');
    setLoading(true);
    try {
      await signInWithEmailAndPassword(auth, email, password);
      redirect();
    } catch (error: any) {
      console.error('Erro no login:', error);
      setErrorMsg(error.message.includes('invalid-credential') ? 'Credenciais inválidas.' : 'Erro ao entrar. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setErrorMsg('');
    setLoading(true);
    try {
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
      // O onAuthStateChanged no AuthContext tratará do resto,
      // mas o redirecionamento é feito aqui para seguir a especificação.
      redirect();
    } catch (error: any) {
      console.error('Erro no Google Sign-in:', error);
      setErrorMsg('Erro ao entrar com o Google. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isLoginView) {
      handleLogin();
    } else {
      handleRegister();
    }
  };

  // Estilos baseados na imagem fornecida (dark mode, card centralizado)
  const cardStyle = "bg-[#1e1e1e] p-8 md:p-12 rounded-xl shadow-2xl w-full max-w-md";
  const inputStyle = "w-full p-3 bg-[#2a2a2a] border border-[#3a3a3a] rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500";
  const buttonPrimaryStyle = "w-full p-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition duration-200";
  const buttonSecondaryStyle = "w-full p-3 bg-[#3a3a3a] hover:bg-[#4a4a4a] text-white font-bold rounded-lg transition duration-200 flex items-center justify-center space-x-2";
  const tabActiveStyle = "bg-blue-600 text-white";
  const tabInactiveStyle = "bg-transparent text-gray-400 hover:bg-[#2a2a2a]";

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white p-4">
      <div className={cardStyle}>
        <h1 className="text-3xl font-bold text-center mb-2">Bem-vindo de volta!</h1>
        <p className="text-center text-gray-400 mb-6">Entre para aceder ao Sacy</p>

        {/* Tabs de Entrar/Registar */}
        <div className="flex mb-6 border border-[#3a3a3a] rounded-lg p-1">
          <button
            className={`flex-1 py-2 rounded-lg font-semibold transition duration-200 ${isLoginView ? tabActiveStyle : tabInactiveStyle}`}
            onClick={() => setIsLoginView(true)}
            disabled={loading}
          >
            Entrar
          </button>
          <button
            className={`flex-1 py-2 rounded-lg font-semibold transition duration-200 ${!isLoginView ? tabActiveStyle : tabInactiveStyle}`}
            onClick={() => setIsLoginView(false)}
            disabled={loading}
          >
            Registar
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Campo Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={inputStyle}
              required
              disabled={loading}
            />
          </div>

          {/* Campo Palavra-passe */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">Palavra-passe</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={inputStyle}
              required
              disabled={loading}
            />
          </div>

          {/* Mensagem de Erro */}
          {errorMsg && (
            <p className="text-red-500 text-sm text-center">{errorMsg}</p>
          )}

          {/* Botão Principal */}
          <button type="submit" className={buttonPrimaryStyle} disabled={loading}>
            {loading ? 'A processar...' : isLoginView ? 'Entrar' : 'Registar'}
          </button>
        </form>

        {/* Separador OU */}
        <div className="flex items-center my-6">
          <div className="flex-grow border-t border-[#3a3a3a]"></div>
          <span className="flex-shrink mx-4 text-gray-500 text-sm">OU</span>
          <div className="flex-grow border-t border-[#3a3a3a]"></div>
        </div>

        {/* Botão Google Sign-in */}
        <button onClick={handleGoogleSignIn} className={buttonSecondaryStyle} disabled={loading}>
          {/* Ícone do Google (simulado com um 'G' para simplicidade, idealmente seria um SVG) */}
          <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.26H12v4.26h6.01c-.26 1.37-1.04 2.54-2.21 3.33v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c3.31 0 6.09-1.08 8.12-2.93l-3.57-2.77c-.98.66-2.23 1.06-3.75 1.06-2.89 0-5.34-1.97-6.22-4.67H2.9v2.89C5.07 20.84 8.35 23 12 23z" fill="#34A853"/>
            <path d="M5.78 14.85c-.24-.66-.37-1.36-.37-2.07s.13-1.41.37-2.07V7.89H2.9C2.15 9.43 1.75 11.16 1.75 13s.4 3.57 1.15 5.11l2.88-2.26z" fill="#FBBC05"/>
            <path d="M12 5.6c1.8 0 3.35.63 4.59 1.74l3.17-3.17C18.09 2.51 15.31 1 12 1 8.35 1 5.07 3.16 2.9 6.89l2.88 2.26c.88-2.7 3.33-4.67 6.22-4.67z" fill="#EA4335"/>
          </svg>
          <span>Entrar com o Google</span>
        </button>
      </div>
    </div>
  );
}
