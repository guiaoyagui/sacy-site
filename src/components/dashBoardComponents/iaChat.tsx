"use client";

import React, { useState } from "react";
import SearchBar from "./searchBar";
import Response from "./response";

const IaChat: React.FC = () => {
  const [response, setResponse] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async (query: string) => {
    setResponse(""); // limpa resultado anterior
    setLoading(true);

    try {
      const res = await fetch(`http://127.0.0.1:5000/consulta?q=${encodeURIComponent(query)}`);
      const data = await res.text();
      setResponse(data);
    } catch (error) {
      console.error("Erro ao buscar:", error);
      setResponse("❌ Ocorreu um erro ao buscar os resultados.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 p-6 text-white">
      <SearchBar onSearch={handleSearch} />

      {loading ? (
        <p className="text-center text-gray-400 animate-pulse">⏳ Buscando resultados...</p>
      ) : response ? (
        <Response content={response} />
      ) : (
        <p className="text-center text-gray-400">🔍 Pesquise um tema para começar...</p>
      )}
    </div>
  );
};

export default IaChat;
