"use client";

import Link from "next/link";
import { ArrowRight, MessageCircle } from "lucide-react";

export default function Home() {
  return (
    <main className="relative flex flex-col items-center justify-center min-h-screen bg-black text-white px-6 py-12 overflow-hidden">
      {/* Vídeo de Fundo */}
      <video
        autoPlay
        muted
        loop
        playsInline
        className="absolute inset-0 w-full h-full object-cover"
      >
        <source src="/background_video.mp4" type="video/mp4" />
        Seu navegador não suporta o elemento de vídeo.
      </video>

      {/* Overlay escuro para melhorar a legibilidade do texto */}
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />

      {/* Header Minimalista */}
      <header className="absolute top-0 left-0 right-0 p-6 flex justify-center z-10">
        <h1 className="text-2xl font-bold text-white">
          <span className="text-blue-500">Sacy</span> AI
        </h1>
      </header>

      {/* Conteúdo Principal (Hero Section) */}
      <div className="max-w-4xl text-center mt-20 relative z-20">
        {/* TÍTULO */}
        <h2 className="text-6xl md:text-8xl font-extrabold mb-6 leading-tight tracking-tighter">
          <span className="text-white block">Transforme informação</span>
          <span className="text-blue-500 block">em conhecimento</span>
        </h2>

        {/* DESCRIÇÃO */}
        <p className="text-gray-300 text-xl md:text-2xl leading-relaxed mb-12 max-w-2xl mx-auto">
          Use a IA do Sacy para obter resumos, gerar quizzes interativos e
          transformar qualquer tópico complexo em conhecimento prático.
        </p>

        {/* Botão "Chat" */}
        <Link
          href="/dashboardNext"
          className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold rounded-full shadow-2xl transition-all duration-300 ease-in-out
            bg-blue-600 hover:bg-blue-500 text-white
            transform hover:scale-105 hover:shadow-blue-600/50
            ring-4 ring-blue-600/30"
        >
          <MessageCircle className="w-6 h-6 mr-3" />
          Acessar Chat
          <ArrowRight className="w-5 h-5 ml-2" />
        </Link>
      </div>

      {/* Footer Minimalista */}
      <footer className="absolute bottom-6 text-gray-400 text-sm z-10">
        © {new Date().getFullYear()} SACY TECH — Todos os direitos reservados.
      </footer>
    </main>
  );
}