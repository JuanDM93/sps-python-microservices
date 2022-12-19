import random
import requests
from flask import (
    Blueprint,
    render_template,
)


index_bp = Blueprint('index', __name__, url_prefix='/')


@index_bp.route('/', methods=['GET'])
def index():
    name, img = PokemonHelper().get_pokemon()
    return render_template(
        'index.html',
        poke_name=name.capitalize(),
        poke_img=img
    )


class PokemonHelper:

    def get_pokemon(self):
        """
        Get a random pokemon from pokeapi and save its sprite
        """
        random_id = random.randint(1, 151)
        url = f'https://pokeapi.co/api/v2/pokemon/{random_id}'
        response = requests.get(url)
        response.raise_for_status()
        self.save_sprite(
            random_id=random_id,
            sprite_route=response.json()['sprites']['front_default'],
        )
        return response.json()['name'], f'{random_id}.png'

    def save_sprite(self, random_id, sprite_route):
        """
        Save the sprite of a pokemon in the static folder
        """
        sprite = requests.get(sprite_route)
        with open(f'flaskr/static/{random_id}.png', 'wb') as f:
            f.write(sprite.content)
