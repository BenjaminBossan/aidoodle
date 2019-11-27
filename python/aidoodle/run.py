# type: ignore

import click

from aidoodle.games import tictactoe
from aidoodle.ai.mcts import MctsAgent


AGENTS = ['random', 'mcts']
GAMES = ['tictactoe']


def play_game(*args, n_runs=None, **kwargs):
    n_games = 0
    n_wins_1 = 0
    n_wins_2 = 0
    n_ties = 0

    cont = 't'
    while cont not in {'f', 'q', 'quit'}:
        winner = _play_game(*args, **kwargs)
        if n_runs is None:
            cont = input("(q) to quit playing: ")
        n_games += 1

        if winner == 1:
            n_wins_1 += 1
        elif winner == 2:
            n_wins_2 += 1
        elif winner == -1:
            n_ties += 1
        else:
            raise ValueError

        print(f"games: {n_games} | wins 1: {n_wins_1} | wins 2: {n_wins_2} "
              f"| ties: {n_ties}")

        if n_games >= n_runs:
            break


def _void(*args, **kwargs):
    pass


def _play_game(player1, player2, engine, silent=False):
    sink = _void if silent else print

    game = engine.Game(
        players=(player1, player2),
        board=engine.Board(),
    )

    while not game.winner:
        sink(game.board, flush=True)
        game = engine.make_move(game=game)
    print(game.board)
    sink(f"Winner: {game.winner}")
    return game.winner


@click.command()
@click.option('--start', default=True, type=click.BOOL, help="whether you start")
@click.option('--agent', default='mcts', type=click.Choice(AGENTS), help='which agent')
@click.option('--game', default='tictactoe', type=click.Choice(GAMES), help='which game')
@click.option('--n_iter', default=1000, type=click.INT, help='agent depth')
def run(start, agent, game, n_iter):
    if game == 'tictactoe':
        engine = tictactoe
    else:
        raise ValueError

    player_idx, agent_idx = (1, 2) if start else (2, 1)
    player = engine.Player(player_idx, agent=engine.CliInputAgent())

    if agent == 'random':
        player_agent = engine.Player(agent_idx)
    elif agent == 'mcts':
        player_agent = engine.Player(
            agent_idx, agent=MctsAgent(engine=engine, n_iter=n_iter))
    else:
        raise ValueError

    print(f"Playing against {player_agent.agent}")
    if start:
        play_game(player, player_agent, engine=engine)
    else:
        play_game(player_agent, player, engine=engine)


@click.command()
@click.option('--game', default='tictactoe', type=click.Choice(GAMES), help='which game')
@click.option('--agent1', default='mcts', type=click.Choice(AGENTS), help='choose agent 1')
@click.option('--agent2', default='mcts', type=click.Choice(AGENTS), help='choose agent 2')
@click.option('--n_iter1', default=1000, type=click.INT, help='agent 1 depth')
@click.option('--n_iter2', default=1000, type=click.INT, help='agent 2 depth')
@click.option('--n_runs', default=100, type=click.INT, help='number of simulations')
def simulate(game, agent1, agent2, n_iter1, n_iter2, n_runs):
    if game == 'tictactoe':
        engine = tictactoe
    else:
        raise ValueError

    if agent1 == 'random':
        player1 = engine.Player(1)
    elif agent1 == 'mcts':
        player1 = engine.Player(1, agent=MctsAgent(engine=engine, n_iter=n_iter1))
    else:
        raise ValueError

    if agent2 == 'random':
        player2 = engine.Player(2)
    elif agent2 == 'mcts':
        player2 = engine.Player(2, agent=MctsAgent(engine=engine, n_iter=n_iter2))
    else:
        raise ValueError

    play_game(player1, player2, engine=engine, n_runs=n_runs, silent=False)
