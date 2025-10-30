"use client";

import Link from "next/link";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-[#0f0f10] text-white px-6">
      <div className="max-w-2xl text-center">
        <h1 className="text-5xl font-extrabold mb-6">
          Bem-vindo à <span className="text-blue-500">SACY TECH</span>
        </h1>
        <p className="text-gray-400 text-lg leading-relaxed mb-10">
          Explore o poder da inteligência artificial para gerar resumos, imagens e respostas personalizadas.
          <br />
          Clique abaixo para acessar o painel de pesquisa e conversar com a IA.
        </p>

        <Link
          href="/dashboardNext"
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-8 rounded-xl shadow-lg transition-all"
        >
          Acessar Painel
        </Link>
      </div>

      <footer className="absolute bottom-6 text-gray-600 text-sm">
        © {new Date().getFullYear()} SACY TECH — Todos os direitos reservados.
      </footer>
    </main>
  );
}
