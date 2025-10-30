"use client";

import React from "react";
import ReactMarkdown from "react-markdown";

interface ResponseProps {
  content: string;
}

const Response: React.FC<ResponseProps> = ({ content }) => {
  // 🧹 Limpa o HTML e textos desnecessários da resposta
  const cleanText = content
    .replace(/<[^>]+>/g, "") // remove tags HTML
    .replace(/\n+/g, " ")
    .replace(/\s{2,}/g, " ")
    .replace(/(Saltar para o conteúdo|Menu principal|Editar código fonte|Ver histórico|Ligações externas|Ferramentas|Discussão|Wikidata)/gi, "")
    .replace(/(\[\d+\])/g, "") // remove referências tipo [1]
    .replace(/(\(.+?Wikipédia.+?\))/gi, "") // remove repetições de "Wikipédia"
    .trim();

  // 🎯 Limita o texto para não ficar gigante
  const shortText = cleanText.length > 1200 ? cleanText.slice(0, 1200) + "..." : cleanText;

  // 🔗 Extrai o primeiro link encontrado (ex: Wikipédia)
  const linkMatch = content.match(/https?:\/\/[^\s"]+/);
  const link = linkMatch ? linkMatch[0] : null;

  return (
    <div className="h-full w-full bg-black/30 text-white p-6 rounded-2xl overflow-y-auto backdrop-blur-md border border-white/10 shadow-lg">
      <h2 className="text-2xl font-semibold text-blue-400 mb-3 flex items-center gap-2">
        🧠 Resultados resumidos
      </h2>
      <div
        className="prose prose-invert max-w-none text-gray-200 leading-relaxed text-base whitespace-pre-line"

      >
        <ReactMarkdown>{shortText}</ReactMarkdown>
      </div>

      {link && (
        <a
          href={link}
          target="_blank"
          rel="noopener noreferrer"
          className="block mt-6 text-blue-400 hover:text-blue-300 font-medium transition-colors"
        >
          📘 Ler matéria completa
        </a>
      )}
    </div>
  );
};

export default Response;
