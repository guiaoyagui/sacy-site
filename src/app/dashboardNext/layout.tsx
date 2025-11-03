import type { Metadata } from "next";
import "../globals.css";
import { Inter } from "next/font/google";

export const metadata: Metadata = {
  title: "SacyIA",
  description: "ia que ajuda você a encontrar o que precisa",
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
      <body className="relative min-h-screen bg-page">
        <div className="absolute inset-0 bg-black/80 z-0" />

        <main className="relative z-10">{children}</main>
      </body>
    </html>
  );
}
