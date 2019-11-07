from flask import current_app

from application import socketio
from application.models import GameOfLifeGame, GameOfLifeCell, db


def create_new_game(owner, width, height):
    game_cells = list()

    game = GameOfLifeGame(owner=owner)
    db.session.add(game)
    
    dead_cell_color = current_app.config['GAME_OF_LIFE_DEAD_CELL_COLOR']
    
    for y in range(height):
        for x in range(width):
            cell = GameOfLifeCell(
                game=game,
                x=x + 1,
                y=y + 1,
                color=dead_cell_color,
            )
            game_cells.append((cell.x, cell.y, False, dead_cell_color))
            db.session.add(cell)
    db.session.commit()

    broadcast_game_state(game)
    return game


def delete_game(game):
    try:
        cells_to_delete = GameOfLifeCell.query.filter_by(game=game).all()
        for cell in cells_to_delete:
            db.session.delete(cell)
        db.session.delete(game)
        db.session.commit()
    except Exception as E:
        print(E)
        db.session.rollback()


def broadcast_game_state(game=None):
    if game is None:
        game = GameOfLifeGame.query.first()

    game_cells = list()
    cells = GameOfLifeCell.query.filter_by(game=game).all()
    for cell in cells:
        alive = 1 if cell.is_alive else 0
        game_cells.append((cell.x, cell.y, alive, cell.color))

    socketio.emit("gameUpdate", game_cells) 


def update_game_round():
    current_game_state = dict()
    game_cells = list()

    games_exist = GameOfLifeGame.query.scalar()
    if not games_exist:
        return

    game = GameOfLifeGame.query.first()
    cells = GameOfLifeCell.query.filter_by(game=game).all()
    for cell in cells:
        coordinates = (cell.x, cell.y)
        is_alive = cell.is_alive
        color = cell.color
        current_game_state[coordinates] = {"is_alive": is_alive, "color": color}

    for cell in cells:
        cell_state = _get_cell_state(cell, current_game_state)

        alive_next_round, color = _is_alive_next_round(cell_state, current_game_state)
        if alive_next_round is not None:
            cell.is_alive = alive_next_round
            cell.color = color
            db.session.commit()

        alive = 1 if cell.is_alive else 0
        game_cells.append((cell.x, cell.y, alive, cell.color))

    socketio.emit("gameUpdate", game_cells)



def _get_cell_state(cell, current_game_state):
    state = dict()
    neighbours = _get_neighbour_cell_coordinates(cell)
    alive_neighbours, dead_neighbours = _count_live_and_dead_neighbours(neighbours, current_game_state)

    state['cell'] = cell
    state['is_alive'] = cell.is_alive
    state['color'] = cell.color
    state['alive_neighbours'] = alive_neighbours
    state['dead_neighbours'] = dead_neighbours

    return state

def _get_neighbour_cell_coordinates(cell):
    """Returns list of coordinate sets for all neighbours of
    a particular cell"""
    neighbours = list()
    game_width = current_app.config['GAME_OF_LIFE_WIDTH']
    game_height = current_app.config['GAME_OF_LIFE_HEIGHT']

    min_x = cell.x - 1 if (cell.x - 1) > 0 else 1
    max_x = cell.x + 1 if (cell.x + 1 <= game_width) else game_width
    min_y = cell.y - 1 if (cell.y - 1) > 0 else 1
    max_y = cell.y + 1 if (cell.y + 1 <= game_height) else game_height

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if x == cell.x and y == cell.y:
                continue
            neighbours.append((x, y))

    return neighbours


def _count_live_and_dead_neighbours(cell_coord_list, game_state):
    alive_cells = 0
    dead_cells = 0

    for cell_coord in cell_coord_list:
        current_cell_state = game_state[cell_coord]
        is_alive = current_cell_state['is_alive']
        if is_alive:
            alive_cells += 1
        else:
            dead_cells += 1

    return alive_cells, dead_cells


def _is_alive_next_round(current_state, game_state):
    is_alive = current_state['is_alive']
    color = current_state['color']
    cell = current_state['cell']

    alive_neighbours = current_state['alive_neighbours']
    dead_cell_color = current_app.config['GAME_OF_LIFE_DEAD_CELL_COLOR']

    if is_alive and alive_neighbours < 2:
        return False, dead_cell_color
    elif is_alive and alive_neighbours in (2, 3):
        return True, color
    elif is_alive and alive_neighbours > 3:
        return False, dead_cell_color
    elif not is_alive and alive_neighbours == 3:
        new_color = _get_revived_cell_color(cell, game_state)
        return True, new_color
    else:
        return None, dead_cell_color


def _get_revived_cell_color(cell, game_state):
    colors_of_alive_neighbours = list()
    neighbours_coords = _get_neighbour_cell_coordinates(cell)
    for cell_coord in neighbours_coords:
        current_cell_state = game_state[cell_coord]
        is_alive = current_cell_state['is_alive']
        
        if is_alive:
            color = current_cell_state['color']
            colors_of_alive_neighbours.append(color)
    average_color = _calc_average_color(colors_of_alive_neighbours)

    return average_color


def _calc_average_color(list_of_colors):
    no_colors = len(list_of_colors)
    red = 0
    green = 0
    blue = 0

    for color in list_of_colors:
        hex = color.lstrip('#')
        rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        red += rgb[0]
        green += rgb[1]
        blue += rgb[2]
    average_red = int(red / no_colors)
    average_green = int(green / no_colors)
    average_blue = int(blue / no_colors)
    average_color_rgb = (average_red, average_green, average_blue)
    average_color_hex = '#%02x%02x%02x' % average_color_rgb

    return average_color_hex


    