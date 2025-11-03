import type { Metadata } from "next";
import "../globals.css";
import { Inter } from "next/font/google";

export const metadata: Metadata = {
  title: "SacyIA",
  description: "Seu assistente de estudos para o ENEM",
  icons: {
    icon: "https://i.imgur.com/J2SO4bJ.png", // ✅ ícone direto do Imgur
    shortcut: "https://i.imgur.com/J2SO4bJ.png",
    apple: "https://i.imgur.com/J2SO4bJ.png",
  },
};

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className={inter.variable}>
      <head>
        {/* Fallback para navegadores que não interpretam o metadata */}
        <link rel="icon" href="https://i.imgur.com/J2SO4bJ.png" type="image/png" />
      </head>
      <body className="relative min-h-screen bg-page text-gray-900 dark:text-gray-100 font-sans">
        {/* Fundo com leve efeito */}
        <div className="absolute inset-0 backdrop-blur-sm bg-gradient-to-b from-white/30 to-gray-200/20 dark:from-gray-900/50 dark:to-black/50 z-0" />

        {/* Conteúdo principal */}
        <main className="relative z-10">{children}</main>
      </body>
    </html>
  );
}
