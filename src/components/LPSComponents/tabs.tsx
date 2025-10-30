"use client";

import { useState } from "react";

interface TabContent {
  id: string;
  label: string;
  title: string;
  description: string;
}

const tabsData: TabContent[] = [
  {
    id: "exploratoria",
    label: "EXPLORATÓRIA",
    title: "Pesquisa Exploratória",
    description:
      "O usuário é apresentado a uma lista de tópicos relacionados ao tema pesquisado. Cada tópico contém links para fontes relevantes, permitindo uma exploração ampla e diversificada do assunto de interesse.",
  },
  {
    id: "objetivas",
    label: "OBJETIVAS",
    title: "Pesquisa Objetivas",
    description:
      "Ideal para perguntas diretas que exigem respostas rápidas e precisas. O sistema fornece informações concisas e relevantes, otimizando o tempo do usuário e facilitando a tomada de decisões.",
  },
  {
    id: "aprofundamento",
    label: "APROFUNDAMENTO",
    title: "Pesquisa Explicativa",
    description:
      "Voltada para análises detalhadas e compreensão profunda de tópicos complexos. O sistema oferece explicações elaboradas, contexto histórico e conexões entre conceitos para um entendimento completo.",
  },
];

export default function Tabs() {
  const [activeTab, setActiveTab] = useState("exploratoria");

  const activeContent = tabsData.find((tab) => tab.id === activeTab);

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Tab Buttons */}
      <div className="flex flex-wrap justify-center gap-4 mb-8">
        {tabsData.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-6 py-3 rounded-full font-medium transition-all duration-300 ${
              activeTab === tab.id
                ? "bg-white text-black"
                : "border border-white text-white hover:bg-white/10"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="bg-black/40 backdrop-blur-sm border border-white/20 rounded-xl p-8 min-h-[200px]">
        {activeContent && (
          <div className="animate-fadeIn">
            <h3 className="text-2xl font-semibold text-white mb-4">
              {activeContent.title}
            </h3>
            <p className="text-gray-300 leading-relaxed">
              {activeContent.description}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}