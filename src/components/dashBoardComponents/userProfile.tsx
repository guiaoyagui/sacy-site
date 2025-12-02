'use client';

import React, { useState, useRef, useEffect } from 'react';
import { LogOut, User, ChevronDown, ChevronUp } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { signOut } from 'firebase/auth';

const UserProfile: React.FC = () => {
  const { user, auth } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Fecha o dropdown se o usuário clicar fora
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [dropdownRef]);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      // Redireciona para a página de login após o logout
      window.location.href = '/login';
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
      alert('Não foi possível sair da conta. Tente novamente.');
    }
  };

  // Se o usuário não estiver logado, não deve renderizar este componente
  // (Embora a proteção de rota no dashBoard/page.tsx já trate disso)
  if (!user) {
    return null;
  }

  // Obtém o nome de exibição ou usa o e-mail como fallback
  const displayName = user.displayName || user.email || 'Usuário Sacy';
  const displayEmail = user.email || 'Sem e-mail';
  const userInitial = displayName.charAt(0).toUpperCase();

  return (
    <div className="absolute bottom-4 left-4 z-50" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 p-2 rounded-xl bg-[#1e1e1e] hover:bg-[#2a2a2a] transition duration-200 cursor-pointer text-white shadow-lg"
      >
        {/* Avatar */}
        <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-lg font-bold">
          {userInitial}
        </div>
        
        {/* Informações do Usuário */}
        <div className="text-left hidden sm:block">
          <p className="font-medium text-sm truncate max-w-[120px]">{displayName}</p>
          <p className="text-xs text-gray-400">Nível 1</p>
        </div>

        {/* Ícone de Dropdown */}
        <div className="text-gray-400">
          {isOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </div>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute bottom-full mb-2 w-full min-w-[200px] bg-[#1e1e1e] rounded-xl shadow-2xl overflow-hidden">
          {/* Header do Dropdown (opcional, mostra e-mail) */}
          <div className="p-3 border-b border-[#2a2a2a]">
            <p className="text-sm font-semibold text-white truncate">{displayName}</p>
            <p className="text-xs text-gray-400 truncate">{displayEmail}</p>
          </div>

          {/* Opções */}
          <button
            onClick={() => {
              // Lógica para ir para a página de perfil (se existir)
              alert('Funcionalidade de Perfil em desenvolvimento!');
              setIsOpen(false);
            }}
            className="flex items-center w-full p-3 text-sm text-white hover:bg-blue-600/20 transition duration-150"
          >
            <User size={18} className="mr-3 text-blue-400" />
            Ver Perfil
          </button>

          <button
            onClick={handleLogout}
            className="flex items-center w-full p-3 text-sm text-red-400 hover:bg-red-600/20 transition duration-150 border-t border-[#2a2a2a]"
          >
            <LogOut size={18} className="mr-3" />
            Sair da Conta
          </button>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
