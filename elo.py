from data_types import User

def adjust_elo_record(player1: User, player2: User, result: int):
    elo1 = player1.elo
    elo2 = player2.elo
    expected1 = 1 / (1 + 10 ** ((elo2 - elo1) / 400))
    expected2 = 1 / (1 + 10 ** ((elo1 - elo2) / 400))
    player1.elo = elo1 + 32 * (result - expected1)
    player2.elo = elo2 + 32 * ((1 - result) - expected2)
    player1.games.append(player2.name)
    player2.games.append(player1.name)
    if result == 1:
        player1.wins += 1
        player2.losses += 1
    elif result == 0:
        player2.wins += 1
        player1.losses += 1
    return None