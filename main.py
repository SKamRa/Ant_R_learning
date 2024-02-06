from flask import Flask, render_template, request, redirect, flash
import src.ai_renfo


app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    """
    Landing page for the simulation

    Methods : GET
    """
    return render_template('index.html', nb_turn=0, nb_fruits=0, map_size=0, score=0, erromsg="")

@app.route("/generate", methods=['GET', 'POST'])
def generate():
    """
    Call the ai_renfo.py to create the frames

    Methods : GET, POST 

    Return : redirect to the index.html    
    """
    if request.method == 'POST':
        turn_nb = request.form['turn_nb']
        fruits_nb = request.form['fruits_nb']
        size_map = request.form['map_size']
        total_tiles = int(size_map)**2
        if total_tiles < int(fruits_nb):
            redirect('/')
            return render_template('index.html', errormsg="Nombre de fruits ne peux pas être supérieur au nombre de cases!")
        score = ai_renfo.main(turn_nb, fruits_nb, size_map)
        return render_template('index.html', nb_turn=turn_nb, nb_fruits=fruits_nb, map_size=size_map, score=score)

    elif request.method == 'GET':
        return redirect('/')


if __name__ == "__main__":
    app.run(port=8080, debug=True)