def calculate_battle_score(level: int, force: int) -> int:
    if level < 0 or force < 0:
        raise ValueError("Nível e força devem ser maiores ou iguais a zero")
    return level * force


def determine_winner(
    first_level: int,
    first_force: int,
    second_level: int,
    second_force: int,
) -> dict:
    first_score = calculate_battle_score(first_level, first_force)
    second_score = calculate_battle_score(second_level, second_force)
    if first_score > second_score:
        winner = "first"
    elif second_score > first_score:
        winner = "second"
    else:
        winner = "draw"
    return {
        "winner": winner,
        "first_score": first_score,
        "second_score": second_score,
    }
