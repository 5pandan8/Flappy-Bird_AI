# 🐦 Flappy Bird AI

A simple **Flappy Bird clone** built using [Pygame](https://www.pygame.org/news) and enhanced with an **AI agent trained using [NEAT-Python](https://neat-python.readthedocs.io/en/latest/)** to play the game automatically.

The project demonstrates how evolutionary algorithms can be applied to train agents in reinforcement-learning-like environments.

---

## 🚀 Features

* Classic Flappy Bird gameplay implemented with **Pygame**.
* AI agent learns to play the game using the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm.
* Visualization of AI training and evolution across generations.
* Easy-to-understand code structure for learning purposes.

---

## 🛠 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Flappy-Bird_AI.git
   cd Flappy-Bird_AI
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   **Requirements:**

   * Python 3.x
   * Pygame
   * NEAT-Python

---

## ▶️ Usage

### Run the game manually

```bash
python flappy_bird.py
```

### Train and run the AI

```bash
python flappy_bird_ai.py
```

* The AI will start training using NEAT and evolve over multiple generations.
* You can tweak parameters inside `config-feedforward.txt` to experiment with different training settings.

---

## 📂 Project Structure

```
Flappy-Bird_AI/
│── flappy_bird.py        # Play Flappy Bird manually
│── flappy_bird_ai.py     # AI-controlled Flappy Bird using NEAT
│── config-feedforward.txt # NEAT configuration file
│── assets/               # Game sprites (bird, pipes, background, etc.)
│── requirements.txt
│── README.md
```

---

## 📖 Learning Outcomes

This project is great for:

* Understanding how **neuroevolution** works.
* Learning **Pygame basics** for game development.
* Exploring the integration of AI with games.

---

## 📚 References

* [NEAT-Python Documentation](https://neat-python.readthedocs.io/en/latest/)
* [Pygame Documentation](https://www.pygame.org/docs/)


