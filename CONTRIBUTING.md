# Contributing to PulseTag

Thank you for your interest in contributing to PulseTag! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- OpenRouter API key (free at https://openrouter.ai/keys)

### Setting Up Your Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pulse-tag.git
   cd pulse-tag
   ```

3. Set up the development environment:
   ```bash
   # Copy environment file
   cp backend/.env.example backend/.env
   
   # Add your OpenRouter API key to backend/.env
   # Start the services
   docker-compose up --build
   ```

## How to Contribute

### Reporting Bugs

- Use the GitHub issue tracker
- Provide a clear description of the bug
- Include steps to reproduce the issue
- Add screenshots if applicable

### Suggesting Features

- Open an issue with the "enhancement" label
- Describe the feature and why it would be useful
- Consider if it fits the project's goals

### Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards below

3. Test your changes thoroughly

4. Commit your changes:
   ```bash
   git commit -m "feat: add your feature description"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a pull request

## Coding Standards

### Frontend (React/TypeScript)

- Use TypeScript for all new code
- Follow React best practices
- Use functional components with hooks
- Keep components small and focused
- Use Tailwind CSS for styling

### Backend (Python)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write clear, descriptive docstrings
- Keep functions small and focused
- Handle errors gracefully

### General Guidelines

- Write clear, descriptive commit messages
- Use conventional commit format (feat:, fix:, docs:, etc.)
- Update documentation as needed
- Add tests for new features
- Keep the codebase clean and organized

## Pull Request Process

1. Ensure your PR description clearly describes the changes
2. Link any relevant issues in the PR description
3. Ensure all checks pass
4. Request code review from maintainers
5. Make requested changes if any

## Areas Where We Need Help

- [ ] Adding support for more social media platforms
- [ ] Improving the UI/UX
- [ ] Adding more AI models
- [ ] Writing tests
- [ ] Documentation improvements
- [ ] Performance optimizations

## Code of Conduct

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions with the project.

## Questions?

Feel free to open an issue or reach out to the maintainers if you have any questions about contributing.

---

Thank you for contributing to PulseTag! 🚀
