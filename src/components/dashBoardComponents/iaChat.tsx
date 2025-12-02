"use client";

import React, { useState } from "react";
// import SearchBar from "./searchBar"; // Removido para corrigir o erro de compilação
import { Loader2 } from "lucide-react";
// import Response from "./response"; // Removido para corrigir o erro de compilação

// --- Adicionei esta interface para clareza (opcional mas boa prática) ---
// Embora o seu servidor envie HTML, o seu componente Response.tsx
// pode ser mais complexo. Se ele espera JSON, teríamos que mudar mais coisas.
// Mas, por agora, vamos assumir que ele espera HTML (texto).


// --- INÍCIO DA CORREÇÃO DE COMPILAÇÃO ---
// Para resolver o erro "Could not resolve", os componentes 
// SearchBar e Response foram movidos para este ficheiro.

/**
 * Componente SearchBar local para evitar erros de importação.
 */
interface SearchBarProps {
  onSearch: (query: string) => void;
  loading: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, loading }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Pesquise um tema..."
        className="flex-1 p-2 border rounded-md text-black bg-white" // Assegura a legibilidade
        disabled={loading}
      />
      <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded-md" disabled={loading}>
        {loading ? "Aguarde..." : "Enviar"}
      </button>
    </form>
  );
};

/**
 * Componente Response local para evitar erros de importação.
 * Renderiza o conteúdo HTML recebido do backend.
 */
interface ResponseProps {
  content: string;
}

const Response: React.FC<ResponseProps> = ({ content }) => {
  return (
    <div
      className="prose prose-invert max-w-none text-white"
      dangerouslySetInnerHTML={{ __html: content }}
    />
  );
};
// --- FIM DA CORREÇÃO DE COMPILAÇÃO ---


/**
 * Componente Principal do Chat
 */
const IaChat: React.FC = () => {
  const [response, setResponse] = useState<string>("");
  const [loading, setLoading] = useState(false);
  // --- Adicionei um estado de erro para feedback do utilizador ---
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    setResponse(""); // limpa resultado anterior
    setError(null);   // limpa erro anterior
    setLoading(true);

    try {
      // --- CORREÇÃO AQUI ---
      // A rota no servidor_api.py é /pesquisar, não /consulta
      const res = await fetch(`http://127.0.0.1:5000/pesquisar?q=${encodeURIComponent(query)}`);
      
      if (!res.ok) {
        // Captura erros do servidor (como 500, 404)
        throw new Error(`Erro de rede: ${res.statusText}`);
      }

      const data = await res.text();
      setResponse(data);

    } catch (error) {
      console.error("Erro ao buscar:", error);
      const errorMessage = (error instanceof Error) ? error.message : "Ocorreu um erro desconhecido.";
      // --- Define a mensagem de erro para mostrar ao utilizador ---
      setError(`❌ Ocorreu um erro ao buscar os resultados. (${errorMessage})`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 p-6 text-white h-full overflow-y-auto">
      <SearchBar onSearch={handleSearch} loading={loading} />

      {loading ? (
        <div className="flex justify-center items-center h-20">
          <div className="relative w-12 h-12">
            <Loader2 className="w-12 h-12 text-blue-400 animate-spin" />
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400/0 via-blue-400/20 to-blue-400/0 rounded-full animate-pulse" />
          </div>
        </div>
      ) : error ? (
        // --- Mostra a mensagem de erro ---
        <p className="text-center text-red-400">{error}</p>
      ) : response ? (
        <Response content={response} />
      ) : (
        <p className="text-center text-gray-400">🔍 Pesquise um tema para começar...</p>
      )}
    </div>
  );
};

export default IaChat;
