from app.models import GameOfLifeGame, GameOfLifeCell, db


def create_new_game(owner, width, height):
    game = GameOfLifeGame(owner=owner)
    db.session.add(game)
    
    for y in range(height):
        for x in range(width):
            cell = GameOfLifeCell(
                game=game,
                x=x + 1,
                y=y + 1,
            )
            db.session.add(cell)
    db.session.commit()

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


def update_game_round():
    current_game_state = dict()

    games_exist = GameOfLifeGame.query.scalar()
    if not games_exist:
        return

    game = GameOfLifeGame.query.first()
    cells = GameOfLifeCell.query.filter_by(game=game).all()
    for cell in cells:
        coordinates = (cell.x, cell.y)
        is_alive = cell.is_alive
        current_game_state[coordinates] = is_alive

    for cell in cells:
        cell_state = _get_cell_state(cell, current_game_state)
        alive_next_round = _is_alive_next_round(cell_state)
        if alive_next_round is not None:
            cell.is_alive = alive_next_round
            db.session.commit()


def _get_cell_state(cell, current_game_state):
    state = dict()
    neighbours = _get_neighbour_cell_coordinates(cell)
    alive_neighbours, dead_neighbours = _count_live_and_dead_neighbours(neighbours, current_game_state)

    state['is_alive'] = cell.is_alive
    state['alive_neighbours'] = alive_neighbours
    state['dead_neighbours'] = dead_neighbours

    return state

def _get_neighbour_cell_coordinates(cell):
    """Returns list of coordinate sets for all neighbours of
    a particular cell"""
    neighbours = list()

    min_x = cell.x - 1 if (cell.x - 1) > 0 else 1
    min_y = cell.y - 1 if (cell.y - 1) > 0 else 1
    max_x = cell.x + 1 if (cell.x + 1 <= 10) else 10
    max_y = cell.y + 1 if (cell.y + 1 <= 10) else 10

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
        is_alive = game_state[cell_coord]
        if is_alive:
            alive_cells += 1
        else:
            dead_cells += 1

    return alive_cells, dead_cells


def _is_alive_next_round(current_state):
    is_alive = current_state['is_alive']
    alive_neighbours = current_state['alive_neighbours']

    if is_alive and alive_neighbours < 2:
        return False
    elif is_alive and alive_neighbours in (2, 3):
        return True
    elif is_alive and alive_neighbours > 3:
        return False
    elif not is_alive and alive_neighbours == 3:
        return True
    else:
        return None