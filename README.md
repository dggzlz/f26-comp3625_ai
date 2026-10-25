# COMP 3625 - Artificial Intelligence (Fall 2026)

This repository contains shared code, lab exercises, and assignment guidelines for **COMP 3625**. 

This space is intended for course collaborators and classmates to work together, reference coursework, and keep our lab materials organized.

---

## 📌 Working Guidelines for Labs & Assignments

To keep things smooth and organized for everyone working out of this repo, please follow these simple rules:

### 1. Git Workflow & Branching
To prevent merge conflicts and keep our history clean, **do not push directly to `main`**. Follow this branching workflow:

* **Create a feature branch:** Whenever you start a new lab, assignment, or component, branch off from the latest `main`:
  ```bash
  git checkout main
  git pull origin main
  git checkout -b feature/lab-X-yourname
* Use clear and concise commit messages describing what you changed (e.g., `fix: resolve search algorithm heuristic in lab 2` or `add: solution outline for assignment 1`).

### 2. Code Quality & Formatting
* Keep your code clean, readable, and commented where necessary, especially for complex AI algorithms or search heuristics.
* Test your code locally before opening a pull request or merging code into the main branches.

### 3. Collaboration & Integrity
* Feel free to discuss concepts, logic, and debugging strategies with each other.
* Ensure that any shared code aligns with the course’s academic integrity policies regarding collaborative work vs. individual submissions.

---