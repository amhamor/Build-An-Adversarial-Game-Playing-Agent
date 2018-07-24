import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages

custom_heuristic_agent_win_rate_dictionary = {}
baseline_heuristic_agent_win_rate_dictionary = {}

figsize = (17, 13)
figure, [axis1, axis2, axis3] = plt.subplots(3, 1, figsize=figsize)

def get_win_rate_dictionaries(match_results_file_name):
	with open(match_results_file_name, 'r') as input_file_object:
		lines = input_file_object.readlines()
		for line in lines:
			if "Your agent won " in line:
				line_words_list = line.split(' ')
				heuristic_type = line_words_list[-1][:-2]
				#print("heuristic_type: " + str(heuristic_type))
				
				agent_type_start_index = line_words_list.index("against") + 1
				agent_type_end_index = agent_type_start_index + 1
				agent_type = ' '.join(line_words_list[agent_type_start_index:agent_type_end_index+1])
				#print("agent_type: " + str(agent_type))

				for word in line_words_list:
					if '%' in word:
						win_rate = int(float(word[:word.index('%')]))
						#print("win_rate: " + str(win_rate))
				
				if heuristic_type == "custom":	
					custom_heuristic_agent_win_rate_dictionary[agent_type] = win_rate
				elif heuristic_type == "baseline":
					baseline_heuristic_agent_win_rate_dictionary[agent_type] = win_rate

	return custom_heuristic_agent_win_rate_dictionary, baseline_heuristic_agent_win_rate_dictionary

def plot_bar_graph(axis, axis_title, custom_heuristic_agent_win_rate_dictionary, baseline_heuristic_agent_win_rate_dictionary):
	X = list(custom_heuristic_agent_win_rate_dictionary.keys())
	numerical_X = np.arange(len(X))

	custom_heuristic_Y = list(custom_heuristic_agent_win_rate_dictionary.values())
	baseline_heuristic_Y = list(baseline_heuristic_agent_win_rate_dictionary.values())

	axis.bar(numerical_X-0.15, custom_heuristic_Y, width=0.30, align="center")
	axis.bar(numerical_X+0.15, baseline_heuristic_Y, width=0.30, align="center")

	blue_patch = mpatches.Patch(color="blue", label="Custom Heuristic")
	orange_patch = mpatches.Patch(color="orange", label="Baseline Heuristic")

	axis.legend(handles=[blue_patch, orange_patch])

	axis.set_xticks(numerical_X)
	axis.set_xticklabels(X)

	axis.set_xlabel("Agent Type")
	axis.set_ylabel("Win Rate Percentage")

	axis.set_title(axis_title)

with PdfPages("report.pdf") as pdf:
	plot_bar_graph(axis1, "Minimax With Greedy First Choice Move", *get_win_rate_dictionaries("match_results.txt"))
	plot_bar_graph(axis2, "Minimax With Random First Choice Move", *get_win_rate_dictionaries("random_initial_move_match_results.txt"))

	axis3.axis("off")
	axis3_caption_text = """
    Above are two bar graphs showing my custom agents' win rate percentage using my custom heuristic (colored blue) and a baseline heuristic (colored orange) after 400 games with fair matches against Random Agent, Greedy Agent, Minimax Agent, and Custom TestAgent. These two heuristics can be described with two explanations:
    + My custom heuristic calculated the distance of the current player from the center square then returned this distance as a negative value. This simulated choosing the move that minimizes the distance from the player's current location to the center square as much as possible.
    + The baseline heuristic used Udacity's #my_moves - #opponent_moves calculation which simulated achieving a maximum amount of moves more than the opponent.
    
    My custom agents involved in the top graph used a greedy heuristic to choose the first move while my custom agents in the bottom graph randomly chose the first move. Both agents then utilized the minimax search algorithm up through the fourth level of the search tree. If more search is required to find the optimal move after the fourth level of the search tree, the agent then used the heuristic calculation to choose a move from the current player's position.

    I simulated two different ways for the agent to make a first move to see what kind of effect the first move might have on the agent's performance. Using a greedy first move resulted in nearly identical results to using a randomly chosen first move with one exception. When using the baseline heuristic against the Greedy Agent with a greedy first move, the agent loses all of the first 200 games then wins 50% of the last 200 games (i.e. the fair-match games), resulting with a 25% overall win rate. Without this exception, the above graphs show that the baseline heuristic performs the same as or slightly better than my custom heuristic."""
	axis3.text(0.0, 0.05, axis3_caption_text, wrap=True)

	plt.suptitle("400 Games With Fair Matches", fontsize=16)
	plt.tight_layout(rect=[0, 0.03, 1, 0.95])

	figure.subplots_adjust(hspace=0.30)

	pdf.savefig()

	figure2 = plt.figure(figsize=figsize)
	plt.axis("off")
	plt.title("Advanced Heuristic Analysis", fontsize=16)
	figure2_caption_text = """
What features of the game does your heuristic incorporate, and why do you think those features matter in evaluating states during search?

    My custom heuristic incorporates choosing locations that are closest to the center square. Being close to the center square is important because a knight chess piece generally has more locations to move to when in the middle of the board and therefore indirectly incorporates the number of liberties feature at each state. The number of liberties at each state is important because at least one liberty is required to remain in the game and having more liberties than the opponent can increase the chance to win.

Analyze the search depth your agent achieves using your custom heuristic. Does search speed matter more or less than accuracy to the performance of your heuristic?

    My agent achieves a search depth of four. Any search depth greater than four has a chance to take longer than the default time constraint placed on each move. Any search depth less than four causes the agent to guess an optimal move that could have been found otherwise. Because a search agent with infinite time to make a move can search more than 13 levels of nodes (which is more than three times more levels and exponentially more nodes) on an 11 by 9 Isolation board, heuristic accuracy is more important than search speed when under the default time constraints for making a move. As the search space becomes smaller, the agent is able to find a higher percentage of optimal moves relative to the total amount of optimal moves possible and thus search speed becomes more important than heuristic accuracy (because the relevance of the heuristic goes to zero as the search space approaches zero)."""

	figure2.text(0.0, 0.65, figure2_caption_text, wrap=True)

	pdf.savefig()

	plt.show()
