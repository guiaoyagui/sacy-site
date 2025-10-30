"use client";

import { useState } from "react";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-transparent">
      <nav className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <div className="flex items-center">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
              <span className="text-black font-bold text-xl">S</span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#inicio" className="text-white hover:text-gray-300 transition-colors">
              Início
            </a>
            <a href="#servicos" className="text-white hover:text-gray-300 transition-colors">
              Serviços
            </a>
            <a href="#sobre" className="text-white hover:text-gray-300 transition-colors">
              Sobre
            </a>
          </div>

          {/* Search Button */}
          <div className="hidden md:block">
            <button className="border border-white rounded-full px-6 py-2 text-white hover:bg-white hover:text-black transition-colors duration-300">
              Pesquisar
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-white"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              {isMenuOpen ? (
                <path d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 pb-4 space-y-4">
            <a
              href="#inicio"
              className="block text-white hover:text-gray-300 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Início
            </a>
            <a
              href="#servicos"
              className="block text-white hover:text-gray-300 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Serviços
            </a>
            <a
              href="#sobre"
              className="block text-white hover:text-gray-300 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Sobre
            </a>
            <button className="border border-white rounded-full px-6 py-2 text-white hover:bg-white hover:text-black transition-colors duration-300 w-full">
              Pesquisar
            </button>
          </div>
        )}
      </nav>
    </header>
  );
}