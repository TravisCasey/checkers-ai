# Checkers AI

This project is an agent learning to play checkers using deep reinforcement learning. Within this project is the custom checkers package written to handle the logic and flow of playing a match of checkers. Included in the package are other agents that play using tree search algorithms for the AI agent to be validated against. The goal is for the AI agent to play at the level of a tree search agent in a fraction of the computing time.

This project is a work in progress. The checkers package is fully useable; its documentation is within its __init__.py file. The agents included use pure tree search and are somewhat slow, but this is intended to be improved upon in the future. In particular, a Monte Carlo tree search agent would be more effective than a pure and naive tree search. Adding a graphical interface would improve clarity and playability as well.

The current state of the model is used a feedforward network using fully connected layers. While this design does learn initially, it fails to improve signficantly against the other agents. This seems to vary little with different hyperparameters and architectures. The next steps are to instead implement a convolutional neural network (CNN) instead, as it more accurately represents the checkers board. Also, using the network to instead assess on a Monte Carlo tree rather than simply choosing the best move. This will allow the network continue to improve with self-play.

Currently, checkers may be played using the checkers package by running the build.py module in the checkers package. The model can be customized and trained by running the model.py file in the repository.
