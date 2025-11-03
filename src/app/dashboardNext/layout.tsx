import type { Metadata } from "next";
import "../globals.css";
import { Inter } from "next/font/google";

export const metadata: Metadata = {
  title: "SacyIA",
  description: "IA que ajuda você a encontrar o que precisa",
  icons: {
    icon: "https://i.imgur.com/J2SO4bJ.png", // ✅ ícone do site
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
        {/* Fallback para navegadores que não interpretam metadata */}
        <link rel="icon" href="https://i.imgur.com/J2SO4bJ.png" type="image/png" />
      </head>
      <body className="relative min-h-screen bg-page">
        {/* Fundo escurecido */}
        <div className="absolute inset-0 bg-black/80 z-0" />

        {/* Conteúdo principal */}
        <main className="relative z-10">{children}</main>
      </body>
    </html>
  );
}
