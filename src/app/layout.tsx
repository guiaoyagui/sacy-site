import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Script from "next/script"; // ✅ Import necessário para carregar KaTeX de forma segura
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Sacy - Seu assistente de estudos",
  description: "A inteligência artificial que te ajuda a estudar para o ENEM e vestibulares.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <head>
        {/* ✅ KaTeX: estilos e scripts para renderização matemática */}
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css"
          integrity="sha384-n8f+6nR9+v9B0eJ9rQx6HuXsd+OB1zME4j9F4J3L3+Pp6ahv8M27aR4Mu9l8+2A/"
          crossOrigin="anonymous"
        />
      </head>
      <body className={inter.className}>
        {/* ✅ Carrega scripts de forma assíncrona e segura */}
        <Script
          id="katex-core"
          src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"
          strategy="beforeInteractive"
          crossOrigin="anonymous"
        />
        <Script
          id="katex-auto-render"
          src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"
          strategy="beforeInteractive"
          crossOrigin="anonymous"
        />

        {/* Contexto de autenticação + conteúdo */}
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
