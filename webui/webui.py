from webui import app
from flask import request, render_template
from objects.Game import Game


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/board', methods=['GET', 'POST'])
def board():

    if request.method == 'POST':
        a = 1
        # update player decision
        # make computer decision
    else:
        # first rendering so randomise hands
        game = Game()
        game.flop()

    return render_template('board.html',
                           player_hand=game.players[0].hand.pokerhand,
                           com_hand=game.players[1].hand.pokerhand,
                           community=game.community_cards)

