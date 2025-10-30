"use client";

import { useState } from "react";

export default function ImageSearch() {
  const [query, setQuery] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSearch(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setImageUrl(""); // limpa imagem anterior

    try {
      // 👉 Aqui vai a lógica para gerar imagem.
      // Substitua por sua API real (exemplo abaixo)
      const response = await fetch(
        `https://api.example.com/generate?prompt=${encodeURIComponent(query)}`
      );
      const data = await response.json();

      setImageUrl(data.imageUrl);
    } catch (err) {
      console.error("Erro ao gerar imagem:", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-950 text-white p-6">
      <h1 className="text-2xl font-bold mb-4">Gerador de Imagens</h1>

      <form
        onSubmit={handleSearch}
        className="w-full max-w-md flex flex-col items-center"
      >
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Digite algo e pressione Enter..."
          className="w-full p-3 rounded-xl bg-gray-800 text-white placeholder-gray-400 outline-none focus:ring-2 focus:ring-blue-500"
        />
      </form>

      <div className="mt-6 w-full max-w-md h-[400px] flex items-center justify-center bg-gray-900 rounded-xl overflow-hidden">
        {loading ? (
          <p className="animate-pulse text-gray-400">Gerando imagem...</p>
        ) : imageUrl ? (
          <img
            src={imageUrl}
            alt={query}
            className="w-full h-full object-cover transition-opacity duration-500"
          />
        ) : (
          <p className="text-gray-500">Digite um tema e pressione Enter</p>
        )}
      </div>
    </div>
  );
}
