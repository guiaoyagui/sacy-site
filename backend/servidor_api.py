from flask import Flask, request, jsonify
from flask_cors import CORS
from agent_literatura import AgentLiteratura

app = Flask(__name__)
CORS(app)

agent = AgentLiteratura()

@app.route("/api/processar-consulta", methods=["POST"])
def processar_consulta():
    try:
        data = request.get_json()
        consulta = data.get("consulta", "").strip()

        if not consulta:
            return jsonify({"erro": "Consulta vazia."}), 400

        print(f"📡 Recebendo consulta: {consulta}")

        resultado = agent.buscar_e_resumir(consulta)

        # Retorna o resumo formatado como JSON
        return jsonify({"resumo": resultado})
    
    except Exception as e:
        print(f"❌ Erro interno no servidor: {e}")
        return jsonify({"erro": str(e)}), 500


@app.route("/", methods=["GET"])
def raiz():
    return jsonify({"mensagem": "Servidor do AgentLiteratura está ativo 🚀"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
