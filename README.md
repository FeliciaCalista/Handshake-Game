# Handshakes Game

This project is a Python-based simulation and solver for a two-player Sokoban-style handshake puzzle. Two players must navigate a maze, moving their “hands” through obstacles and interacting with game mechanics until they meet and perform a handshake.

---

## Objective

Use **Breadth-First Search (BFS)** to simulate all possible hand movements between two pawns until a valid handshake occurs under specific constraints:
- Limited hand movement range per player
- Barriers, movable boxes, severed hands, and buttons in the maze
- Game state updated based on interaction rules

---

## Game Mechanics

- **Pawns**: Two characters with separate arms and limited moves
- **Maze Elements**:
  - `#`: Wall
  - `/`: Barrier
  - `*`: Movable box
  - `G`, `P`: Green and purple buttons
  - `$`: Severed hand
  - `%`: Successful handshake
- **ASCII-based Movement**:
  - Pawn A hands: `→`, `←`, `↑`, `↓`
  - Pawn B hands: `⇒`, `⇐`, `⇑`, `⇓`

---

## License

This project is licensed under the MIT License – you are free to use, modify, and distribute this project with attribution.
