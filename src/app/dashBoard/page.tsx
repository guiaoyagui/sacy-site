"use client";

import React, { useState } from "react";
// 1. REMOVIDO O IMPORT DO REACT-MARKDOWN

// API Key para a API Gemini (no frontend, se necessário)
// (Deixe como "" - o ambiente irá fornecê-la)
const apiKey = "AIzaSyDTuho3L8K7DX0LYsIcLKYlLbRF3EN5gW4"; // <-- CORRIGIDO: Removida a chave por segurança

// --- ESTRUTURA DO QUIZ ATUALIZADA ---
interface QuizQuestion {
  pergunta: string;
  alternativas: string[];
  correcta: number; // Índice da resposta correta (0-3)
}

// --- NOVO COMPONENTE: UserProfile (Placeholder) ---
// Adicionado aqui para resolver o erro de importação do "UserProfile"
const UserProfile: React.FC<{ isLoggedIn: boolean }> = ({ isLoggedIn }) => {
  return (
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center text-gray-400">
        ?
      </div>
      <div>
        <p className="font-medium text-gray-300">
          {isLoggedIn ? "Utilizador Logado" : "Visitante"}
        </p>
        <p className="text-xs text-gray-500">
          {isLoggedIn ? "Ver Perfil" : "Nível 1"}
        </p>
      </div>
    </div>
  );
};
// --- FIM DO COMPONENTE UserProfile ---


export default function Dashboard() { // <-- CORRIGIDO: Nome do componente
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // --- Estados Gemini Atualizados ---
  const [quizQuestions, setQuizQuestions] = useState<QuizQuestion[]>([]);
  const [isGeneratingExtras, setIsGeneratingExtras] = useState(false);
  const [extrasError, setExtrasError] = useState<string | null>(null);

  // --- NOVOS ESTADOS PARA O QUIZ INTERATIVO ---
  const [selectedAnswers, setSelectedAnswers] = useState<{ [key: number]: number }>({});
  const [quizResults, setQuizResults] = useState<{ [key: number]: "correct" | "incorrect" }>({});
  const [quizScore, setQuizScore] = useState<string | null>(null);

  // --- NOVO ESTADO: MODO FOCO ENEM ---
  const [isEnemMode, setIsEnemMode] = useState(false);


  // --- NOVO HELPER PARA LIMPAR HTML (MAIS ROBUSTO) ---
  const cleanHtmlResult = (html: string): string => {
    if (!html) return "";
    
    // Remove qualquer background-color hexadecimal (ex: #ffffff, #f9f9f9)
    let cleaned = html.replace(/background-color:\s*#[0-9a-fA-F]{3,6}/gi, 'background-color: transparent');
    cleaned = cleaned.replace(/background-color:\s*white/gi, 'background-color: transparent');
    cleaned = cleaned.replace(/border:\s*1px\s*solid\s*#ddd/gi, 'border: 1px solid #333');
    cleaned = cleaned.replace(/padding:\s*(15px|20px)/gi, 'padding: 0');
    cleaned = cleaned.replace(/font-family:\s*Arial,\s*sans-serif;/gi, ''); 
    
    return cleaned;
  };


  /**
   * Função principal para executar a pesquisa no backend.
   * AGORA ATUALIZADA PARA O MODO ENEM.
   */
  const runSearch = async (currentQuery: string) => {
    if (!currentQuery.trim()) return;

    setLoading(true);
    setResult(null);
    setQuizQuestions([]);
    setExtrasError(null);
    setSelectedAnswers({});
    setQuizResults({});
    setQuizScore(null);

    // --- LÓGICA DO MODO ENEM ---
    // 1. Escolhe o endpoint correto
    const endpoint = isEnemMode ? "/pesquisar-enem" : "/pesquisar";
    const url = `http://127.0.0.1:5000${endpoint}?q=${encodeURIComponent(currentQuery)}`;
    
    console.log(`Modo ENEM: ${isEnemMode ? 'LIGADO' : 'DESLIGADO'}`);
    console.log(`Chamando URL: ${url}`);
    // --- FIM DA LÓGICA ---

    try {
      // 2. Passar a 'consulta' como um parâmetro query (?q=)
      // 3. Usar o método GET (implícito ou explícito)
      const response = await fetch(
         url,
         {
           method: "GET", // Especificar GET para clareza
         }
      );

      if (!response.ok) {
        throw new Error(`Erro na resposta do servidor: ${response.statusText}`);
      }

      // O backend sempre envia HTML, seja do modo normal ou ENEM
      const data = await response.text(); 
      const rawHtml = data || "<p><em>Nenhum resultado encontrado.</em></p>";
      setResult(cleanHtmlResult(rawHtml));

    } catch (error: any) {
      console.error("Erro ao processar a consulta:", error);

      let errorMessage =
        "<p><strong>Erro: Falha na Comunicação</strong></p><p>Não foi possível obter o resultado do servidor. Por favor, tente novamente. 😔</p>";

      if (error instanceof TypeError && error.message.includes("Failed to fetch")) {
        errorMessage =
          "<p><strong>Erro: Não foi possível ligar ao backend</strong></p>" +
          "<p>Verifique se o seu servidor Python (Flask) está em execução no endereço <code>http://127.0.0.1:5000</code>.</p>" +
          "<p><strong>Nota:</strong> Se esta aplicação estiver a correr em <code>https</code>, o seu browser pode estar a bloquear pedidos para <code>http</code> (Mixed Content).</p>";
      }
      
      setResult(cleanHtmlResult(errorMessage));

    } finally {
      setLoading(false);
    }
  };

  /**
   * Lida com a submissão do formulário principal.
   */
  const handleFormSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    runSearch(query);
  };

  /**
   * Lida com o clique numa pergunta sugerida (agora pergunta do quiz).
   */
  const handleSuggestedQuestionClick = (question: string) => {
    const cleanQuestion = question.replace(/^\d+\.\s*/, "");
    setQuery(cleanQuestion);
    runSearch(cleanQuestion);
  };

  // --- Funções da API Gemini ---

  /**
   * Função genérica para chamar a API Gemini (gemini-2.5-flash)
   */
  const callGeminiAPI = async (
    prompt: string,
    systemInstruction?: string,
    jsonMode: boolean = false,
    schema?: any 
  ) => {
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;

    const payload: any = {
      contents: [{ parts: [{ text: prompt }] }],
    };

    if (systemInstruction) {
      payload.systemInstruction = {
        parts: [{ text: systemInstruction }],
      };
    }

    if (jsonMode) {
      payload.generationConfig = {
        responseMimeType: "application/json",
        responseSchema: schema || {
          type: "OBJECT",
          properties: {
            placeholder: { type: "STRING" }, 
          },
        },
      };
    }

    let retries = 3;
    let delay = 1000;

    while (retries > 0) {
      try {
        const response = await fetch(apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (
          result.candidates &&
          result.candidates[0].content?.parts?.[0]?.text
        ) {
          return result.candidates[0].content.parts[0].text;
        } else {
          throw new Error("Resposta da API inválida.");
        }
      } catch (error) {
        console.error(
          `Erro na API Gemini (tentativas restantes: ${retries - 1}):`,
          error
        );
        retries--;
        if (retries === 0) {
          throw error;
        }
        await new Promise((resolve) => setTimeout(resolve, delay));
        delay *= 2;
      }
    }
    throw new Error("Falha ao chamar a API Gemini após várias tentativas.");
  };

  /**
   * ✨ GEMINI FEATURE 1: Simplificar o resumo
   */
  const handleSimplify = async () => {
    if (!result) return;

    setLoading(true);
    setQuizQuestions([]);
    setExtrasError(null);
    setSelectedAnswers({});
    setQuizResults({});
    setQuizScore(null);
    const currentResult = result;

    try {
      const systemPrompt =
        "És um assistente de IA especializado em simplificar texto para iniciantes. Responde em português.\n" +
        "**Instruções de Formatação OBRIGATÓRIAS:**\n" +
        "- Deves formatar a tua resposta em **HTML**. Não uses Markdown.\n" +
        "- Usa emojis (como 💡, 🎯, 📚) para tornar o texto mais amigável.\n" +
        "- Usa `<strong>` para destacar pontos-chave.\n" +
        "- Usa `<ul>` e `<li>` para listas e tópicos.\n" +
        "- Usa `<p>` para parágrafos e `<h3>` para subtítulos se necessário.\n" +
        "- **Exemplo:** `<p>💡 A <strong>Fórmula de Bhaskara</strong> é uma ferramenta...</p><ul><li>🎯 Serve para encontrar soluções...</li></ul>`";

      const userPrompt = `Simplifique o seguinte texto para um iniciante (lembre-se de formatar em HTML):\n\n---\n\n${currentResult}`;

      const simplifiedText = await callGeminiAPI(userPrompt, systemPrompt);
      setResult(cleanHtmlResult(simplifiedText)); 

    } catch (error: any) {
      console.error("Erro ao simplificar:", error);

      let errorMsg =
        "<p><strong>Erro ao Simplificar</strong></p><p>Ocorreu um erro ao tentar simplificar o texto. O resumo original é apresentado abaixo.</p><hr>";
      if (error.message && error.message.includes("403")) {
        errorMsg =
          "<p><strong>Erro na API Gemini (403 - Proibido)</strong></p><p>A chave da API pode estar em falta ou ser inválida. Não é possível contactar a IA.</p><hr>";
      }
      setResult(cleanHtmlResult(errorMsg + currentResult)); 
    } finally {
      setLoading(false);
    }
  };

  /**
   * ✨ GEMINI FEATURE 2: Gerar Quiz (com alternativas e resposta correta)
   */
  const handleSuggestQuestions = async () => {
    if (!result) return;

    setIsGeneratingExtras(true);
    setExtrasError(null);
    setQuizQuestions([]);
    setSelectedAnswers({});
    setQuizResults({});
    setQuizScore(null);

    try {
      const systemPrompt =
        "És um assistente de IA com o papel de um professor. A tua tarefa é criar 3 perguntas de prova (em português) com base no texto fornecido, para simular um quiz. Cada pergunta deve ter 4 alternativas (a, b, c, d). Deves também indicar o **índice** da resposta correta (0, 1, 2, ou 3). Devolve a tua resposta como um objeto JSON.";
      
      const userPrompt = `Com base no seguinte texto, gera 3 perguntas de prova (quiz) que um aluno deveria ser capaz de responder após ler o texto:\n\n---\n\n${result}`;

      const quizSchema = {
        type: "OBJECT",
        properties: {
          quiz: {
            type: "ARRAY",
            items: {
              type: "OBJECT",
              properties: {
                pergunta: { type: "STRING" },
                alternativas: {
                  type: "ARRAY",
                  items: { type: "STRING" },
                },
                correcta: { 
                  type: "NUMBER",
                  description: "O índice (0-3) da alternativa correta"
                },
              },
              required: ["pergunta", "alternativas", "correcta"]
            },
          },
        },
      };

      const jsonResponse = await callGeminiAPI(
        userPrompt,
        systemPrompt,
        true,
        quizSchema
      );
      const parsed = JSON.parse(jsonResponse);

      if (parsed.quiz && Array.isArray(parsed.quiz)) {
        setQuizQuestions(parsed.quiz); 
      } else {
        throw new Error("Formato JSON inesperado.");
      }
    } catch (error: any) {
      console.error("Erro ao sugerir perguntas:", error);

      let errorMsg = `Houve um erro ao sugerir perguntas. (${
        error.message || "Tente novamente."
      })`;
      if (error.message && error.message.includes("403")) {
        errorMsg =
          "Erro na API Gemini (403 - Proibido): A chave da API pode estar em falta ou ser inválida.";
      }
      setExtrasError(errorMsg);
    } finally {
      setIsGeneratingExtras(false);
    }
  };

  // --- NOVAS FUNÇÕES PARA QUIZ INTERATIVO ---

  const handleAnswerSelect = (questionIndex: number, alternativeIndex: number) => {
    if (Object.keys(quizResults).length === 0) {
      setSelectedAnswers(prev => ({
        ...prev,
        [questionIndex]: alternativeIndex
      }));
    }
  };

  const handleSubmitQuiz = () => {
    let results: { [key: number]: "correct" | "incorrect" } = {};
    let correctCount = 0;

    quizQuestions.forEach((q, index) => {
      if (selectedAnswers[index] === q.correcta) {
        results[index] = "correct";
        correctCount++;
      } else {
        results[index] = "incorrect";
      }
    });

    setQuizResults(results);
    setQuizScore(`Acertou ${correctCount} de ${quizQuestions.length}!`);
  };

  const allQuestionsAnswered = Object.keys(selectedAnswers).length === quizQuestions.length;


  // --- JSX Atualizado ---

  return (
    <div className="absolute inset-0 flex flex-col md:flex-row w-full h-screen bg-[#0f0f10] text-white overflow-hidden">
      {/* Painel esquerdo - Chat */}
      <aside className="md:w-1/3 w-full p-6 border-r border-gray-800 flex flex-col h-full justify-between">
        <h1 className="text-2xl font-semibold mb-4 flex items-center gap-2">
          🤖 Chat com a IA
        </h1>
        <p className="text-gray-400 text-sm mb-6">
          Envie uma nova pergunta para a IA e veja o resultado completo no
          painel ao lado.
        </p>

        <form onSubmit={handleFormSubmit} className="flex flex-col gap-3">
          <input
            type="text"
            placeholder="Digite o tema que deseja pesquisar..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full p-3 rounded-xl bg-[#1a1a1b] text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          />

          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 transition-all text-white py-2 rounded-xl font-medium flex items-center justify-center gap-2"
          >
            {loading ? (
              <svg
                className="animate-spin h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
            ) : null}
            {loading ? "Buscando..." : "Pesquisar"}
          </button>
          
          {/* --- NOVO: BOTÃO MODO ENEM --- */}
          <div className="flex items-center justify-center gap-3 mt-3">
            <label 
              htmlFor="enem-toggle" 
              className={`font-medium transition-all ${isEnemMode ? 'text-green-400' : 'text-gray-500'}`}
            >
              Modo Foco ENEM/Vestibular
            </label>
            <button
              id="enem-toggle"
              role="switch"
              aria-checked={isEnemMode ? "true" : "false"}
              onClick={() => setIsEnemMode(!isEnemMode)}
              className={`relative inline-flex items-center h-6 rounded-full w-11 transition-all ${isEnemMode ? 'bg-green-600' : 'bg-gray-600'}`}
            >
              <span
                className={`inline-block w-4 h-4 transform bg-white rounded-full transition-transform ${isEnemMode ? 'translate-x-6' : 'translate-x-1'}`}
              />
            </button>
          </div>
          {/* --- FIM DO BOTÃO --- */}
          
        </form>
        <div className="mt-auto">
          <UserProfile isLoggedIn={false} />
        </div>
      </aside>

      {/* Painel direito - Resultados */}
      <main className="flex-1 p-8 overflow-y-auto h-full">
        <div className="bg-[#161618] p-6 rounded-2xl shadow-lg min-h-[200px] h-full">
          <h2 className="text-2xl font-semibold flex items-center gap-2 mb-4">
            🧠 Resultados resumidos
          </h2>

          {/* Skeleton Loader */}
          {loading && (
            <div className="space-y-5 animate-pulse">
              <div className="h-6 bg-gray-700 rounded w-1OS/3"></div>
              <div className="space-y-3">
                <div className="h-4 bg-gray-700 rounded w-full"></div>
                <div className="h-4 bg-gray-700 rounded w-full"></div>
                <div className="h-4 bg-gray-700 rounded w-5/6"></div>
                <div className="h-4 bg-gray-700 rounded w-3/4"></div>
              </div>
            </div>
          )}

          {/* Resultado */}
          {!loading && result && (
            <div
              className="max-w-none text-gray-200 leading-relaxed text-base"
              dangerouslySetInnerHTML={{ __html: result }}
            />
          )}

          {/* --- NOVOS BOTÕES GEMINI --- */}
          {!loading && result && (
            <div className="mt-8 pt-6 border-t border-gray-700 flex flex-wrap gap-3">
              <button
                onClick={handleSimplify}
                disabled={isGeneratingExtras || loading}
                className="bg-teal-600 hover:bg-teal-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all"
              >
                ✨ Simplificar Resumo
              </button>

              {/* --- Botão "Gerar Quiz" --- */}
              <button
                onClick={handleSuggestQuestions}
                disabled={isGeneratingExtras || loading}
                className="bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all"
              >
                {isGeneratingExtras ? (
                  <svg
                    className="animate-spin h-4 w-4 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                ) : (
                  "📚"
                )}
                {isGeneratingExtras ? "A Gerar..." : "Gerar Quiz"}
              </button>
            </div>
          )}

          {/* --- ÁREA PARA ERROS SECUNDÁRIOS --- */}
          {extrasError && (
            <div className="mt-4 text-sm text-red-400 bg-red-900/20 p-3 rounded-lg">
              {extrasError}
            </div>
          )}

          {/* --- NOVO QUIZ INTERATIVO --- */}
          {!loading && quizQuestions.length > 0 && (
            <div className="mt-6">
              <h4 className="text-xl font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">
                Quiz Rápido
              </h4>
              <div className="flex flex-col gap-4">
                {quizQuestions.map((q, index) => {
                  const isSubmitted = !!quizResults[index];
                  return (
                    <div key={index} className="bg-gray-800/50 p-4 rounded-lg">
                      {/* Pergunta Clicável */}
                      <button
                        onClick={() => handleSuggestedQuestionClick(q.pergunta)}
                        className="text-left text-lg text-teal-300 hover:text-teal-200 hover:underline transition-all font-medium disabled:no-underline disabled:text-teal-300 disabled:cursor-default"
                        title="Clique para pesquisar a resposta"
                        disabled={isSubmitted} // Desativa o clique após submeter
                      >
                        {index + 1}. {q.pergunta}
                      </button>
                      
                      {/* Alternativas como Rádio Buttons */}
                      <fieldset className="list-none pl-5 mt-3 space-y-2">
                        <legend className="sr-only">Alternativas para a pergunta {index + 1}</legend>
                        {q.alternativas.map((alt, altIndex) => {
                          const isSelected = selectedAnswers[index] === altIndex;
                          const isCorrect = q.correcta === altIndex;
                          
                          let stateClass = "";
                          if (isSubmitted) {
                            if (isCorrect) {
                              stateClass = "border-green-500 bg-green-900/50 text-green-200";
                            } else if (isSelected) {
                              stateClass = "border-red-500 bg-red-900/50 text-red-300 opacity-70";
                            } else {
                              stateClass = "border-gray-700 opacity-40";
                            }
                          } else if (isSelected) {
                            stateClass = "border-blue-500 bg-blue-900/50 text-white";
                          } else {
                            stateClass = "border-gray-700 hover:bg-gray-700/50 cursor-pointer";
                          }

                          return (
                            <label key={altIndex} className={`flex items-center w-full text-left p-3 rounded-lg border transition-all duration-150 ${stateClass}`}>
                              <input
                                type="radio"
                                name={`question-${index}`}
                                value={altIndex}
                                checked={isSelected}
                                onChange={() => handleAnswerSelect(index, altIndex)}
                                disabled={isSubmitted}
                                className="w-4 h-4 mr-3 text-teal-400 bg-gray-600 border-gray-500 focus:ring-teal-500 focus:ring-2"
                              />
                              <span className="text-gray-500 mr-2">{String.fromCharCode(97 + altIndex)})</span>
                              {alt}
                            </label>
                          );
                        })}
                      </fieldset>
                    </div>
                  );
                })}

                {/* --- Botão de Submissão e Pontuação --- */}
                <div className="mt-4 flex flex-col items-center gap-4">
                  <button
                    onClick={handleSubmitQuiz}
                    disabled={!allQuestionsAnswered || !!quizScore} // Desativa se não respondeu tudo ou se já submeteu
                    className="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg text-base font-medium transition-all"
                  >
                    {quizScore ? "Quiz Corrigido!" : "Corrigido!"}
                  </button>

                  {quizScore && (
                    <p className="text-lg font-semibold text-yellow-300">
                      {quizScore}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Mensagem Inicial (como antes) */}
          {!loading && !result && (
            <p className="text-gray-500">Pesquise algo para começar 🚀</p>
          )}
        </div>
      </main>
    </div>
  );
}

