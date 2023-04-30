import io
import chess
import chess.engine
import requests
from aiogram import Bot, Dispatcher
from chess.pgn import Game
import config as cfg
import re


def get_best_move(url):
    """
    Returns the best move may be found in position imported by url to lichess.

    url: str - link to the game.

    return: str - best move and current score on the board.
    """

    # Getting game id by url
    game_id = url.split("/")[-1]
    game_id = game_id[:8]
    # print(game_id)

    # Getting PGN-data using API Lichess
    # https://lichess.org/game/export/ielMM7Ep?evals=0&clocks=0 - example of url
    response = requests.get(cfg.LICHESS_URL_FIRST_PART + f"{game_id}" + cfg.LICHESS_URL_SECOND_PART)

    if response.status_code != cfg.GOOD_QUERY:
        print(cfg.LICHESS_URL_FIRST_PART + f"{game_id}" + cfg.LICHESS_URL_SECOND_PART)
        return f"Error while getting data. Response status code: {response.status_code}"

    # Creating the game object using PGN-data
    pgn_data = response.content.decode()
    game = chess.pgn.read_game(io.StringIO(pgn_data))

    # Analyzing current position using Stockfish
    engine = chess.engine.SimpleEngine.popen_uci(cfg.STOCKFISH_PATH)  # Путь к исполняемому файлу Stockfish
    board = game.board()
    for move in game.mainline_moves():
        board.push(chess.Move.from_uci(move.uci()))

    # print(game.mainline())
    # print(board)
    # Getting best move and current score on the board
    result = engine.analyse(board, chess.engine.Limit(time=cfg.TIME_FOR_THINKING))
    best_move = result["pv"][0].uci()
    score = result["score"]
    reg = float(re.findall(r'(\d+)', str(score.white()))[0])
    if (reg > 0):
        reg = '+' + str(reg / 100)
    else:
        reg = str(reg / 100)

    engine.quit()

    return f"The best move: {best_move} ({reg})"
