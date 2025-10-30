export default function Footer() {
  return (
    <footer className="bg-black text-white rounded-t-[50px] mt-20">
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Logo e Citação */}
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center">
                <span className="text-black font-bold text-2xl">S</span>
              </div>
            </div>
            <p className="text-gray-400 text-sm italic">
              &ldquo;Não procuramos o que existe na Terra, mas criamos o que ela ainda não viu.&rdquo;
            </p>
            <p className="text-gray-500 text-xs">- Lema SACY</p>
          </div>

          {/* Navegação */}
          <div>
            <h4 className="text-lg font-semibold mb-4">NAVEGAÇÃO</h4>
            <ul className="space-y-2">
              <li>
                <a href="#inicio" className="text-gray-400 hover:text-white transition-colors">
                  → Início
                </a>
              </li>
              <li>
                <a href="#servicos" className="text-gray-400 hover:text-white transition-colors">
                  → Serviços
                </a>
              </li>
              <li>
                <a href="#sobre" className="text-gray-400 hover:text-white transition-colors">
                  → Sobre
                </a>
              </li>
              <li>
                <a href="#faq" className="text-gray-400 hover:text-white transition-colors">
                  → FAQ
                </a>
              </li>
            </ul>
          </div>

          {/* Use Pesquisa */}
          <div>
            <h4 className="text-lg font-semibold mb-4">USE PESQUISA</h4>
            <form className="space-y-4">
              <input
                type="email"
                placeholder="Digite seu email"
                className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-white/40 transition-colors"
              />
              <button
                type="submit"
                className="w-full bg-white text-black px-6 py-2 rounded-lg font-medium hover:bg-gray-200 transition-colors"
              >
                Inscrever-se
              </button>
            </form>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-12 pt-8 border-t border-white/10 text-center">
          <p className="text-gray-500 text-sm">
            © 2025 Tecnologias SACY — Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}