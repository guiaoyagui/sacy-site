"use client";

import React, { useState } from "react";

export default function DashboardNext() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/processar-consulta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ consulta: query }),
      });

      if (!response.ok) {
        throw new Error("Erro ao buscar dados");
      }

      const data = await response.json();
      setResult(data.resumo || "<p>Nenhum resultado encontrado.</p>");
    } catch (error) {
      console.error("Erro ao processar a consulta:", error);
      setResult("<p style='color:#f87171'>Erro: não foi possível obter o resultado. 😔</p>");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col md:flex-row w-full min-h-screen bg-[#0f0f10] text-white">
      {/* Painel esquerdo - Chat */}
      <aside className="md:w-1/3 w-full p-6 border-r border-gray-800 flex flex-col">
        <h1 className="text-2xl font-semibold mb-4 flex items-center gap-2">🤖 Chat com a IA</h1>
        <p className="text-gray-400 text-sm mb-6">
          Envie uma nova pergunta para a IA e veja o resultado completo no painel ao lado.
        </p>

        <form onSubmit={handleSearch} className="flex flex-col gap-3">
          <input
            type="text"
            placeholder="Digite o tema que deseja pesquisar..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full p-3 rounded-xl bg-[#1a1a1b] text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 transition-all text-white py-2 rounded-xl font-medium"
          >
            {loading ? "Buscando..." : "Pesquisar"}
          </button>
        </form>
      </aside>

      {/* Painel direito - Resultados */}
      <main className="flex-1 p-8 overflow-y-auto">
        <div className="bg-[#161618] p-6 rounded-2xl shadow-lg">
          <h2 className="text-2xl font-semibold flex items-center gap-2 mb-4">
            🧠 Resultados resumidos
          </h2>

          {loading && (
            <p className="text-gray-400 animate-pulse">Carregando resultados...</p>
          )}

          {!loading && result && (
            <div
              className="prose prose-invert max-w-none text-gray-200 leading-relaxed text-base"
              dangerouslySetInnerHTML={{ __html: result }}
            />
          )}

          {!loading && !result && (
            <p className="text-gray-500">Pesquise algo para começar 🚀</p>
          )}
        </div>
      </main>
    </div>
  );
}
