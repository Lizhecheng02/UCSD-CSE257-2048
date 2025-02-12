import matplotlib.pyplot as plt
import numpy as np
from game import Game
from ai import AI


def run_game_sequence(depth, max_moves=1000):
    scores = []
    game = Game()

    for _ in range(max_moves):
        if game.game_over():
            break
        ai = AI(game.current_state(), search_depth=depth)
        direction = ai.compute_decision()
        game.move_and_place(direction)
        scores.append(game.score)

    return scores


def plot_performance_comparison():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    colors_exp1 = ["#F7CFD8", "#B82132", "#A6F1E0", "#5C7285", "#09122C"]
    colors_exp3 = ["#F7CFD8", "#B82132", "#A6F1E0", "#5C7285", "#09122C"]

    ax1.set_title("Performance of Exp-1 (Depth = 1)", fontsize=10)
    for i in range(5):
        scores = run_game_sequence(1)
        moves = range(len(scores))
        ax1.plot(moves, scores, color=colors_exp1[i], label=f"Run {i + 1}", linewidth=1, alpha=1)
    ax1.set_xlabel("Number of Moves")
    ax1.set_ylabel("Game Score")
    ax1.grid(True, alpha=0.8)
    ax1.legend()

    ax2.set_title("Performance of Exp-3 (Depth = 3)", fontsize=10)
    for i in range(5):
        scores = run_game_sequence(3)
        moves = range(len(scores))
        ax2.plot(moves, scores, color=colors_exp3[i], label=f"Run {i + 1}", linewidth=1, alpha=1)
    ax2.set_xlabel("Number of Moves")
    ax2.set_ylabel("Game Score")
    ax2.grid(True, alpha=0.8)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("Figs/depth-comparison.pdf", format="pdf", dpi=450, bbox_inches="tight", pad_inches=0.05)
    plt.show()


if __name__ == "__main__":
    plot_performance_comparison()
