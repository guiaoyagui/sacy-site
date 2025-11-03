"use client";

import React, { useState } from "react";
import { Send, Loader2 } from "lucide-react"; // Importar ícones

interface SearchBarProps {
  onSearch: (query: string) => void;
  loading: boolean; // Adicionar prop de carregamento
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, loading }) => {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    if (query.trim() !== "" && !loading) {
      onSearch(query.trim());
      setQuery(""); // 🔄 limpa o campo depois da pesquisa
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="w-full flex justify-center">
      <div className="relative w-full max-w-md">
        <input
          type="text"
          placeholder="Digite sua mensagem..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          className="w-full px-4 py-3 pr-12 rounded-xl bg-zinc-800 text-white border border-white/10 focus:outline-none focus:ring-2 focus:ring-blue-400 placeholder-gray-500 transition-all duration-300 shadow-lg"
          disabled={loading}
        />
        <button
          onClick={handleSearch}
          disabled={query.trim() === "" || loading}
          className={`absolute right-2 top-1/2 transform -translate-y-1/2 p-2 rounded-full transition-all duration-300
            ${query.trim() !== "" && !loading
              ? "bg-blue-500 hover:bg-blue-600 text-white shadow-md hover:shadow-lg hover:scale-110"
              : "bg-zinc-700 text-gray-400 cursor-not-allowed"
            }
          `}
        >
          {loading ? (
            <div className="relative w-5 h-5">
              {/* Animação de carregamento com gradiente */}
              <Loader2 className="w-5 h-5 animate-spin text-blue-400" />
            </div>
          ) : (
            <Send className="w-5 h-5 transition-transform duration-200 group-hover:translate-x-1" /> // Ícone de envio
          )}
        </button>
      </div>
    </div>
  );
};

export default SearchBar;
