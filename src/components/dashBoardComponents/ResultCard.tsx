import React from "react";

interface ResultCardProps {
  topic: string;
  title: string;
  summary: string;
  imageUrl: string;
  link: string;
}

const ResultCard: React.FC<ResultCardProps> = ({
  topic,
  title,
  summary,
  imageUrl,
  link,
}) => {
  return (
    <div className="bg-black/40 p-4 rounded-2xl border border-white/10 hover:border-blue-400 transition-all duration-300 shadow-md">
      <h3 className="text-blue-400 text-xl font-semibold mb-1">{title}</h3>
      <p className="text-gray-400 text-sm mb-3">Tópico: {topic}</p>

      <div className="flex flex-col md:flex-row gap-4">
        <img
          src={imageUrl}
          alt={title}
          className="w-full md:w-1/3 rounded-xl object-cover"
        />
        <p className="text-gray-200 text-base leading-relaxed flex-1">
          {summary}
        </p>
      </div>

      <a
        href={link}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block mt-4 text-blue-400 hover:text-blue-300 font-medium transition"
      >
        📘 Ler matéria completa
      </a>
    </div>
  );
};

export default ResultCard;
