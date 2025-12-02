"use client";

import React, { useState, useEffect, useRef } from "react";
import { useAuth } from "@/context/AuthContext";
import UserProfile from "@/components/dashBoardComponents/UserProfile";

// --- API Gemini ---
const apiKey = "AIzaSyDTuho3L8K7DX0LYsIcLKYlLbRF3EN5gW4";

interface QuizQuestion {
  pergunta: string;
  alternativas: string[];
  correta: number; // ✅ Correto
}


export default function Dashboard() {
  const { user, loading } = useAuth();
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [displayedResult, setDisplayedResult] = useState<string>("");
  const [apiLoading, setApiLoading] = useState(false);
  const resultRef = useRef<HTMLDivElement>(null);

  const [quizQuestions, setQuizQuestions] = useState<QuizQuestion[]>([]);
  const [isGeneratingExtras, setIsGeneratingExtras] = useState(false);
  const [extrasError, setExtrasError] = useState<string | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<{ [key: number]: number }>({});
  const [quizResults, setQuizResults] = useState<{ [key: number]: "correct" | "incorrect" }>({});
  const [quizScore, setQuizScore] = useState<string | null>(null);
  const [isEnemMode, setIsEnemMode] = useState(false);

  // Redireciona se não estiver logado
  useEffect(() => {
    if (!loading && !user) window.location.href = "/login";
  }, [user, loading]);

  // Renderização estável KaTeX
  useEffect(() => {
    if (displayedResult && resultRef.current) {
      import("katex")
        .then((katex) => {
          const elements = resultRef.current!.querySelectorAll("span.math, span.katex, .chem");
          elements.forEach((el) => {
            try {
              katex.render(el.textContent || "", el as HTMLElement, { throwOnError: false });
            } catch (err) {
              console.warn("Erro KaTeX:", err);
            }
          });
        })
        .catch((err) => console.error("Erro KaTeX:", err));
    }
  }, [displayedResult]);

  // Efeito de digitação inteligente (sem bug visual)
  useEffect(() => {
    if (!result) return;

    const hasMath = /\$[^$]+\$|\$\$[^$]+\$\$|\\[a-zA-Z]+/.test(result);
    const clean = result.replace(/<style[\s\S]*?<\/style>/gi, "");

    // Se o texto contém fórmulas, renderiza de uma vez
    if (hasMath) {
      setDisplayedResult(clean);
      return;
    }

    // Caso contrário, anima
    let i = 0;
    setDisplayedResult("");
    const interval = setInterval(() => {
      setDisplayedResult(clean.slice(0, i));
      i++;
      if (i >= clean.length) clearInterval(interval);
    }, 5);
    return () => clearInterval(interval);
  }, [result]);

// Limpa HTML e trata KaTeX (versão final — remove duplicações e artefatos invisíveis)
const cleanHtmlResult = (html: string): string => {
  if (!html) return "";

  // Evita reprocessar se o texto já tiver fórmulas renderizadas
  const alreadyHasMath = html.includes("katex") || html.includes('<span class="math"');

  let cleaned = html
    .replace(/<style[\s\S]*?<\/style>/gi, "") // Remove estilos vindos do backend
    .replace(/background-color:\s*(white|#[0-9a-fA-F]{3,6})/gi, "background-color: transparent")
    .replace(/border:\s*1px\s*solid\s*#ddd/gi, "border: 1px solid #333")
    .replace(/font-family:[^;]+;/gi, "")
    // 🔧 Remove caracteres invisíveis Unicode (ZWSP, ZWNJ, etc.) que causam duplicações tipo FR​=m⋅a
    .replace(/[\u200B-\u200D\uFEFF]/g, "")
    .replace(/\s{2,}/g, " ")
    .trim();

  // Apenas adiciona marcações KaTeX se o texto ainda não tiver sido processado
  if (!alreadyHasMath) {
    cleaned = cleaned
      .replace(/\$\$([^$]+)\$\$/g, '<span class="math">$1</span>')
      .replace(/\$([^$]+)\$/g, '<span class="math">$1</span>');
  }

  return cleaned;
};


  // Busca principal no backend Flask
  const runSearch = async (currentQuery: string) => {
    if (!currentQuery.trim()) return;
    setApiLoading(true);
    setResult(null);
    setDisplayedResult("");
    setQuizQuestions([]);
    setExtrasError(null);
    setSelectedAnswers({});
    setQuizResults({});
    setQuizScore(null);

    const endpoint = isEnemMode ? "/pesquisar-enem" : "/pesquisar";
    const url = `http://127.0.0.1:5000${endpoint}?q=${encodeURIComponent(currentQuery)}`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Erro ${response.statusText}`);
      const data = await response.text();
      setResult(cleanHtmlResult(data));
    } catch (error) {
      console.error("Erro:", error);
      setResult("<p><strong>Erro:</strong> Falha na comunicação com o backend 😔</p>");
    } finally {
      setApiLoading(false);
    }
  };

  const handleFormSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    runSearch(query);
  };

  // Resumo via Gemini
  const handleSimplify = async () => {
    if (!result) return;
    setApiLoading(true);
    try {
      const payload = {
        contents: [{ parts: [{ text: `Simplifique o texto abaixo mantendo formatações matemáticas:\n\n${result}` }] }],
      };
      const res = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`,
        { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }
      );
      const data = await res.json();
      const simplified = data.candidates?.[0]?.content?.parts?.[0]?.text || result;
      setResult(cleanHtmlResult(simplified));
    } catch (err) {
      console.error("Erro Gemini:", err);
    } finally {
      setApiLoading(false);
    }
  };

  // Gerar quiz via Flask
  const handleSuggestQuestions = async () => {
    if (!result) return;
    setIsGeneratingExtras(true);
    setExtrasError(null);
    setQuizQuestions([]);
    setQuizScore(null);
    setQuizResults({});
    setSelectedAnswers({});

    try {
      const response = await fetch("http://127.0.0.1:5000/gerar-quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto: result }),
      });
      const data = await response.json();
      if (data.quiz && Array.isArray(data.quiz)) setQuizQuestions(data.quiz);
      else throw new Error("Retorno inválido do servidor.");
    } catch (e) {
      setExtrasError("⚠️ Não foi possível gerar o quiz. Tente novamente em alguns segundos.");
    } finally {
      setIsGeneratingExtras(false);
    }
  };

  // Quiz interativo
  const handleAnswerSelect = (i: number, j: number) => {
    if (!quizResults[i]) setSelectedAnswers((p) => ({ ...p, [i]: j }));
  };

  const handleSubmitQuiz = () => {
    let r: { [k: number]: "correct" | "incorrect" } = {};
    let acertos = 0;
    quizQuestions.forEach((q, i) => {
      // Garante que selectedAnswers[i] é um número antes de comparar
      const userAnswer = selectedAnswers[i] !== undefined ? selectedAnswers[i] : -1; 
      
      if (userAnswer === q.correta) {
        r[i] = "correct";
        acertos++;
      } else r[i] = "incorrect";
    });
    setQuizResults(r);
    setQuizScore(`✅ Acertou ${acertos} de ${quizQuestions.length}!`);
  };

  const allQuestionsAnswered = Object.keys(selectedAnswers).length === quizQuestions.length;

  if (loading || !user)
    return (
      <div className="min-h-screen flex items-center justify-center bg-black text-white">
        <p>Verificando autenticação...</p>
      </div>
    );

  return (
    <div className="absolute inset-0 flex flex-col md:flex-row w-full h-screen bg-[#0f0f10] text-white overflow-hidden">
      {/* Painel esquerdo */}
      <aside className="md:w-1/3 w-full p-6 border-r border-gray-800 flex flex-col h-full justify-between">
        <h1 className="text-2xl font-semibold mb-4">🤖 Chat com a IA</h1>
        <p className="text-gray-400 text-sm mb-6">
          Envie uma nova pergunta e veja o resultado detalhado.
        </p>

        <form onSubmit={handleFormSubmit} className="flex flex-col gap-3">
          <input
            type="text"
            placeholder="Digite o tema..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full p-3 rounded-xl bg-[#1a1a1b] text-gray-200 focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={apiLoading}
            className="bg-blue-600 hover:bg-blue-700 transition-all text-white py-2 rounded-xl font-medium"
          >
            {apiLoading ? "Buscando..." : "Pesquisar"}
          </button>

<div className="flex items-center justify-center gap-3 mt-3">
  <label
    htmlFor="enem-toggle"
    className={`font-medium ${isEnemMode ? "text-green-400" : "text-gray-500"}`}
  >
    Modo Foco ENEM/Vestibular
  </label>
  <button
    id="enem-toggle"
    role="switch"
    aria-checked={isEnemMode} // ✅ Corrigido: agora envia boolean, não string
    aria-label="Ativar ou desativar modo ENEM/Vestibular"
    onClick={() => setIsEnemMode(!isEnemMode)}
    type="button" // ✅ evita submit acidental
    className={`relative inline-flex items-center h-6 rounded-full w-11 ${
      isEnemMode ? "bg-green-600" : "bg-gray-600"
    }`}
  >
    <span
      className={`inline-block w-4 h-4 transform bg-white rounded-full transition-transform ${
        isEnemMode ? "translate-x-6" : "translate-x-1"
      }`}
    />
  </button>
</div>

        </form>

        <div className="mt-auto">
          <UserProfile />
        </div>
      </aside>

{/* Painel direito */}
<main className="flex-1 p-8 overflow-y-auto h-full">
  <div
    className="
      bg-gradient-to-b from-[#1b1b1e] to-[#121213]
      border border-gray-800/70
      rounded-2xl
      shadow-lg shadow-black/30
      p-8
      transition-all duration-300 ease-in-out
      hover:border-gray-600
      h-full
      flex flex-col
    "
  >
    <h2 className="text-2xl font-semibold flex items-center gap-2 mb-6 text-gray-100">
      🧠 Resultados
    </h2>

    {/* Container fixo para manter layout estável */}
    <div className="flex-1 flex flex-col justify-start">
      {apiLoading ? (
        <div className="flex flex-col items-center justify-center gap-3 flex-1 border border-gray-700/50 bg-gray-900/20 rounded-xl animate-pulse transition-all">
          <p className="text-gray-400 text-sm italic">Processando sua pergunta...</p>
        </div>
      ) : displayedResult ? (
        <div className="w-full space-y-4">
          <div
            ref={resultRef}
            className="
              max-w-none
              bg-[#141416]
              border border-gray-800/80
              rounded-2xl
              shadow-md shadow-black/20
              p-6 sm:p-8 text-gray-100
              leading-relaxed tracking-wide
              transition-all duration-300
              hover:border-gray-600
              overflow-hidden
              prose prose-invert
              [&_h2]:text-gray-100 [&_h2]:font-semibold [&_h2]:text-lg [&_h2]:mt-6 [&_h2]:mb-3
              [&_h3]:text-gray-300 [&_h3]:font-medium [&_h3]:text-base [&_h3]:mt-4 [&_h3]:mb-2
              [&_strong]:text-blue-400 [&_em]:text-gray-400 [&_em]:italic
              [&_code]:bg-[#0f172a] [&_code]:text-blue-300 [&_code]:px-2 [&_code]:py-1 [&_code]:rounded-md
              [&_.math]:block [&_.math]:text-center [&_.math]:my-3 [&_.math]:bg-[#0f172a] [&_.math]:rounded-md [&_.math]:p-3 [&_.math]:text-[1.05rem]
              [&_ul]:list-disc [&_ul]:ml-6 [&_ul]:text-gray-300
              [&_ol]:list-decimal [&_ol]:ml-6 [&_ol]:text-gray-300
              [&_table]:border-collapse [&_table]:w-full [&_table]:my-4
              [&_table_td]:border [&_table_td]:border-gray-700 [&_table_td]:px-3 [&_table_td]:py-2
              [&_table_th]:border [&_table_th]:border-gray-700 [&_table_th]:bg-[#1e293b] [&_table_th]:font-semibold [&_table_th]:px-3 [&_table_th]:py-2
            "
            dangerouslySetInnerHTML={{ __html: displayedResult }}
          />

          <div className="flex flex-wrap items-center justify-center gap-4 mt-6">
            <button
              onClick={handleSimplify}
              className="px-6 py-2.5 rounded-xl font-medium bg-blue-600 hover:bg-blue-700"
            >
              🧩 Resumir Explicação
            </button>
            <button
              onClick={handleSuggestQuestions}
              disabled={isGeneratingExtras}
              className="px-6 py-2.5 rounded-xl font-medium bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50"
            >
              {isGeneratingExtras ? "Gerando Quiz..." : "🎯 Gerar Quiz"}
            </button>
          </div>

          {/* Quiz */}
          {extrasError && <p className="text-red-400 text-center">{extrasError}</p>}
          {quizQuestions.length > 0 && (
            <div className="mt-6 p-4 border border-gray-700 rounded-xl bg-[#1e1e20]">
              <h3 className="text-lg font-semibold mb-3">🧩 Quiz Interativo</h3>
              {quizQuestions.map((q, i) => (
                <div key={i} className="mb-6">
                  <p className="font-medium mb-2">{i + 1}. {q.pergunta}</p>
                  <div className="flex flex-col gap-2">
                    {q.alternativas.map((alt, j) => {
                      const selected = selectedAnswers[i] === j;
                      const resultClass =
                        quizResults[i] === "correct" && j === q.correta
                          ? "bg-green-700"
                          : quizResults[i] === "incorrect" && selected
                          ? "bg-red-700"
                          : selected
                          ? "bg-blue-700"
                          : "bg-gray-700 hover:bg-gray-600";
                      const letter = String.fromCharCode(65 + j);
                      return (
                        <button
                          key={j}
                          onClick={() => handleAnswerSelect(i, j)}
                          disabled={!!quizResults[i]}
                          className={`text-left px-4 py-2 rounded-lg ${resultClass}`}
                        >
                          <span className="font-semibold uppercase">{letter})</span> {alt}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
              {!quizScore && (
                <button
                  onClick={handleSubmitQuiz}
                  disabled={!allQuestionsAnswered}
                  className="mt-4 w-full py-2 bg-blue-600 hover:bg-blue-700 rounded-xl font-medium disabled:opacity-50"
                >
                  Enviar Respostas
                </button>
              )}
              {quizScore && (
                <div className="mt-4 text-center">
                  <p className="font-semibold text-green-400">{quizScore}</p>

                </div>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="flex items-center justify-center flex-1">
          <p className="text-gray-500 mt-4">Pesquise algo para começar 🚀</p>
        </div>
      )}
    </div>
  </div>
</main>
    </div>
  );
}
