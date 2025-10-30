"use client";

import React, { useState } from "react";

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && query.trim() !== "") {
      onSearch(query.trim());
      setQuery(""); // 🔄 limpa o campo depois da pesquisa
    }
  };

  return (
    <div className="w-full flex justify-center">
      <input
        type="text"
        placeholder="Digite um tema para pesquisar..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        className="w-full max-w-md px-4 py-2 rounded-xl bg-zinc-900 text-white border border-white/10 focus:outline-none focus:ring-2 focus:ring-blue-400 placeholder-gray-500"
      />
    </div>
  );
};

export default SearchBar;
