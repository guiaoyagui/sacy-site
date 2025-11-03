"use client";

import React, { useState } from "react";
import { LogOut, Settings, User, ChevronDown } from "lucide-react";

interface UserProfileProps {
  isLoggedIn?: boolean;
  userName?: string;
  userInitials?: string;
}

const UserProfile: React.FC<UserProfileProps> = ({
  isLoggedIn = false,
  userName = "Usuário",
  userInitials = "U",
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    setIsMenuOpen(false);
    // Aqui você pode adicionar a lógica de logout
    console.log("Logout");
  };

  const handleSettings = () => {
    setIsMenuOpen(false);
    // Aqui você pode adicionar a lógica de configurações
    console.log("Settings");
  };

  return (
    <div className="mt-auto pt-6 border-t border-gray-700">
      {isLoggedIn ? (
        <div className="relative">
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="w-full flex items-center justify-between p-3 rounded-lg bg-gray-800/50 hover:bg-gray-700 transition-all duration-200"
          >
            <div className="flex items-center gap-3">
              {/* Avatar */}
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-sm font-semibold">
                {userInitials}
              </div>
              {/* Nome do usuário */}
              <div className="text-left">
                <p className="text-sm font-medium text-white">{userName}</p>
                <p className="text-xs text-gray-400">Grátis</p>
              </div>
            </div>
            {/* Ícone de menu */}
            <ChevronDown
              className={`w-4 h-4 text-gray-400 transition-transform duration-200 ${
                isMenuOpen ? "rotate-180" : ""
              }`}
            />
          </button>

          {/* Menu dropdown */}
          {isMenuOpen && (
            <div className="absolute bottom-full left-0 right-0 mb-2 bg-gray-800 rounded-lg border border-gray-700 shadow-lg overflow-hidden z-50">
              <button
                onClick={handleSettings}
                className="w-full flex items-center gap-3 px-4 py-3 text-sm text-gray-300 hover:bg-gray-700 transition-all duration-200"
              >
                <Settings className="w-4 h-4" />
                Configurações
              </button>
              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-3 px-4 py-3 text-sm text-red-400 hover:bg-gray-700 transition-all duration-200 border-t border-gray-700"
              >
                <LogOut className="w-4 h-4" />
                Sair
              </button>
            </div>
          )}
        </div>
      ) : (
        <button className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium transition-all duration-200 shadow-md hover:shadow-lg">
          <User className="w-4 h-4" />
          Fazer Login
        </button>
      )}
    </div>
  );
};

export default UserProfile;
