from flask import Flask, jsonify, request
from flask_cors import CORS
from animeflv import AnimeFLV

app = Flask(__name__)
CORS(app)

@app.route('/buscar', methods=['GET'])
def search_anime():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "se requiere un parámetro de busqueda"}), 400
    try:
        with AnimeFLV() as api:
            results = api.search(query)
            return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getinfo', methods=['GET'])
def get_anime():
    anime_id = request.args.get('id')
    if not anime_id:
        return jsonify({"error": "Se requiere un ID"}), 400
    try:
        with AnimeFLV() as api:
            anime = api.get_anime_info(anime_id)
            return jsonify(anime)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/listarserver', methods=['GET'])
def get_episodes():
    anime_id = request.args.get('id')
    id_episode = request.args.get('episodio')
    if not anime_id or not id_episode:
        return jsonify({"error": "El ID del anime y el numero del episodio son requeridos"}), 400
    try:
        with AnimeFLV() as api:
            episodes = api.get_video_servers(anime_id, int(id_episode))
            return jsonify(episodes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/listar', methods=['GET'])
def get_episodes_list():
    try:
        with AnimeFLV() as api:
            episodes = api.list()
            return jsonify(episodes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
