import matplotlib.pyplot as plt
import numpy as np
from game import Game
from ai import AI


def run_game_sequence(use_enhanced_score, max_moves=1000):
    scores = []
    game = Game()

    for _ in range(max_moves):
        if game.game_over():
            break

        ai = AI(game.current_state(), search_depth=3)
        if not use_enhanced_score:
            original_expectimax = ai.expectimax
            ai.expectimax = lambda node=None: (original_expectimax(node)[0], node.state[1] if node.is_terminal() else original_expectimax(node)[1])

        direction = ai.compute_decision()
        game.move_and_place(direction)
        scores.append(game.score)

    return scores


def plot_performance_comparison():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    colors_original = ["#F7CFD8", "#B82132", "#A6F1E0", "#5C7285", "#09122C"]
    ax1.set_title("Original Exp-3 (Game Score Only)", fontsize=10)
    for i in range(5):
        scores = run_game_sequence(use_enhanced_score=False)
        moves = range(len(scores))
        ax1.plot(moves, scores, color=colors_original[i], label=f"Run {i+1}", linewidth=1, alpha=1)
    ax1.set_xlabel("Number of Moves")
    ax1.set_ylabel("Game Score")
    ax1.grid(True, alpha=0.8)
    ax1.legend()

    colors_enhanced = ["#F7CFD8", "#B82132", "#A6F1E0", "#5C7285", "#09122C"]
    ax2.set_title("Enhanced Exp-3 (With Enhanced Evaluation)", fontsize=10)
    for i in range(5):
        scores = run_game_sequence(use_enhanced_score=True)
        moves = range(len(scores))
        ax2.plot(moves, scores, color=colors_enhanced[i], label=f"Run {i+1}", linewidth=1, alpha=1)
    ax2.set_xlabel("Number of Moves")
    ax2.set_ylabel("Game Score")
    ax2.grid(True, alpha=0.8)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("Figs/evaluation-comparison.pdf", format="pdf", dpi=450, bbox_inches="tight", pad_inches=0.05)
    plt.show()


if __name__ == "__main__":
    plot_performance_comparison()
