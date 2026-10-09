# Project 2 Report: Adversarial Search & Tic-Tac-Toe AI

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Primary AI Algorithm:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information
- **Name:**Kay
- **MMDT ID:**MMDT051

---

## Section 1: AI Agent Configuration
- **Primary AI Algorithm:** Minimax with Alpha-Beta Pruning
- **Pruning Technique:** Alpha-Beta Pruning with terminal-depth heuristic evaluation
- **Heuristic Strategy:** Win > Block > Center > Corners > Edges

---

## Section 2: Complexity & Search Tree Analysis
- **Maximum Search Depth (Empty 3x3 Board):** 9
- **Total Possible Board States:** 5478
- **Unbeatable Minimax Guarantee:** Yes — a perfect-play minimax agent can force at least a draw and never lose on Tic-Tac-Toe.

---

## Section 3: Local Verification & Agent Checklist
*Check the algorithms, agents, and features you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Minimax Search Algorithm with Depth Penalty
- [x] Alpha-Beta Pruning Optimization
- [x] Rule-Based Heuristic Agent
- [x] Uniform Random Baseline Agent
- [x] Interactive Web Visualizer with Move Matrix & Metrics
- [x] Bot vs Bot Simulation Benchmark

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://dashboard.render.com/project/prj-db4b0jijnfac73aqjd60
- **Video Presentation Link:**https://drive.google.com/drive/folders/1uaPMZveDRk3ZznSX0SZNF4Tt3Xf-gz3t?usp=drive_link

---

## Section 5: Discussion
*Provide your written analysis for each point by replacing the bracket placeholders below:*
- **Explain how Alpha-Beta pruning reduces the number of evaluated game tree nodes without changing the minimax decision.**
    Alpha-Beta pruning keeps track of the best score already found for the maximizing and minimizing players and stops exploring branches when a partial score cannot improve the current best option. Because it prunes only branches that cannot affect the final minimax result, the chosen move stays identical while many redundant game states are skipped. This reduces the effective branching factor and makes deeper search feasible in games like Tic-Tac-Toe.
- **Compare classical Adversarial Search (Minimax / Alpha-Beta) with modern Tree Search approaches in Generative AI (e.g., Monte Carlo Tree Search, Tree of Thoughts, or Process Reward Models).**
    Classical adversarial search uses a fully deterministic game tree with exact utility values and complete state evaluation, while modern Generative AI methods such as Monte Carlo Tree Search, Tree of Thoughts, and Process Reward Models approximate decisions under uncertainty and partial observability. Minimax and Alpha-Beta are exact and efficient for zero-sum games with known rules, whereas generative search uses sampling, value estimates, and self-evaluation to explore broader reasoning paths. Both approaches rely on selecting promising branches, but generative systems often trade perfect optimality for scalability and adaptability in open-ended tasks.
