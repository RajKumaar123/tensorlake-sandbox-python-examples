# 🚀 Tensorlake Sandbox Python Examples

> **A production-ready collection of Python examples demonstrating how to build, explore, and deploy AI applications using Tensorlake Sandboxes.**

---

## Overview

Welcome to the **Tensorlake Sandbox Python Examples** repository.

This repository is a practical engineering guide designed to help developers learn Tensorlake Sandboxes through real-world, executable Python examples.

Unlike many tutorials that only demonstrate successful outcomes, this repository follows an **experiment-driven engineering approach** where every feature is explored, verified, documented, and reproduced before it becomes part of the project.

Every example included in this repository is:

- ✅ Executed successfully
- ✅ Verified against actual SDK behavior
- ✅ Documented with explanations
- ✅ Easy to reproduce
- ✅ Designed using engineering best practices

The goal is to create a high-quality open-source resource that helps AI engineers understand how Tensorlake Sandboxes can be used as secure, isolated, and stateful execution environments for modern AI applications.

---

# Why Tensorlake Sandboxes?

Modern AI systems are no longer simple API calls.

Today's AI applications often require the ability to:

- Execute Python code
- Install packages dynamically
- Process files
- Run long-running tasks
- Maintain persistent state
- Resume interrupted work
- Execute browser automation
- Run isolated agent workloads
- Execute untrusted LLM-generated code safely

Traditional serverless platforms and short-lived containers are not always ideal for these scenarios.

Tensorlake Sandboxes provide persistent and isolated execution environments that make these workflows significantly easier to build.

---

# Repository Objectives

This repository has several goals.

## 1. Learn Through Experimentation

Every feature is explored experimentally instead of relying solely on documentation.

The repository documents:

- API exploration
- SDK behavior
- Errors encountered
- Engineering discoveries
- Lessons learned

---

## 2. Build Production-Quality Examples

Every example should demonstrate good engineering practices, including:

- Meaningful comments
- Error handling
- Logging
- Type hints where appropriate
- Clean code
- Reusable structure

---

## 3. Document Everything

Knowledge should never be lost.

Every experiment records:

- Goal
- Code
- Output
- Errors
- Fixes
- Lessons learned
- Best practices

---

## 4. Create Reusable Learning Resources

Readers should be able to clone the repository and immediately begin learning through practical examples.

---

## 5. Support a Medium Article Series

This repository serves as the companion codebase for an in-depth Medium series covering Tensorlake Sandboxes and AI Engineering.

Every article will reference working examples from this repository.

---

## 6. Build an Open Source Reference

The long-term vision is to create a practical reference repository for developers building AI systems on Tensorlake.

---

# Who Is This Repository For?

This project is intended for:

- AI Engineers
- Machine Learning Engineers
- LLM Engineers
- Agent Developers
- Python Developers
- Software Engineers
- Researchers
- Students
- Anyone interested in AI infrastructure

---

# Repository Principles

This repository follows a few simple principles.

- Learn by building.
- Verify every API before using it.
- Never assume SDK behavior.
- Prefer experimentation over speculation.
- Record every discovery.
- Keep examples independent.
- Produce reproducible results.
- Write production-quality code.
- Document engineering decisions.
- Share practical knowledge with the community.

---

# Features

This repository includes:

- Production-ready Python examples
- Hands-on Tensorlake Sandbox exploration
- Engineering notebook documenting discoveries
- Verified terminal outputs
- Screenshots
- Example-specific documentation
- AI assistant guidance (Codex, Copilot, Claude)
- Medium article references
- GitHub-friendly project structure
- Reproducible experiments
- Engineering best practices
- Clean project organization

---

# Repository Structure

```
tensorlake-sandbox-python-examples/
│
├── README.md                 # Project overview and documentation
├── AGENTS.md                 # Instructions for AI coding assistants
├── ROADMAP.md                # Project roadmap and progress tracking
├── notes.md                  # Engineering notebook
├── CONTRIBUTING.md           # Contribution guidelines
├── CHANGELOG.md              # Project changelog
├── LICENSE                   # MIT License
├── .gitignore
├── requirements.txt
├── .env.example
│
├── docs/
│   ├── article_notes/
│   ├── diagrams/
│   ├── outputs/
│   └── screenshots/
│
├── examples/
│   ├── 01_create_sandbox/
│   ├── 02_run_commands/
│   ├── 03_stateful_filesystem/
│   ├── 04_install_packages/
│   ├── 05_native_file_api/
│   ├── 06_snapshots/
│   ├── 07_suspend_resume/
│   ├── 08_process_management/
│   ├── 09_parallel_sandboxes/
│   ├── 10_browser_automation/
│   ├── 11_computer_use/
│   └── 12_ai_agent_demo/
│
├── experiments/
│   ├── check_env.py
│   ├── explore_tensorlake.py
│   ├── inspect_run.py
│   ├── inspect_sandbox.py
│   ├── inspect_url.py
│   ├── sandbox_test.py
│   └── test_tensorlake.py
│
└── utils/
    ├── config.py
    ├── helper.py
    └── logger.py
```

---

# Learning Roadmap

The repository follows a progressive learning path, starting with the fundamentals and gradually moving toward advanced AI agent workflows.

## Phase 1 — Fundamentals

- Environment Setup
- Creating a Sandbox
- Running Commands
- Understanding the Sandbox Lifecycle
- Stateful Filesystem

---

## Phase 2 — Working with Sandboxes

- Installing Packages
- Native File Operations
- Uploading Files
- Reading Files
- Managing Directories

---

## Phase 3 — Advanced Sandbox Features

- Snapshots
- Checkpoints
- Suspend & Resume
- Process Management
- Long-running Applications

---

## Phase 4 — AI Workloads

- Parallel Sandboxes
- Browser Automation
- Computer Use
- AI Agents
- Multi-Agent Systems

---

## Phase 5 — Production Patterns

- Secure Code Execution
- Background Workers
- Stateful Agents
- Deployment Patterns
- Best Practices

---

# Example Index

| Example | Description | Status |
|----------|-------------|--------|
| 01 | Create Your First Sandbox | ✅ Completed |
| 02 | Execute Commands | ✅ Completed |
| 03 | Stateful Filesystem | ✅ Completed |
| 04 | Installing Python Packages | 🚧 In Progress |
| 05 | Native File APIs | 📅 Planned |
| 06 | Snapshots & Checkpoints | 📅 Planned |
| 07 | Suspend & Resume | 📅 Planned |
| 08 | Process Management | 📅 Planned |
| 09 | Parallel Sandboxes | 📅 Planned |
| 10 | Browser Automation | 📅 Planned |
| 11 | Computer Use | 📅 Planned |
| 12 | AI Agent Demo | 📅 Planned |

---

# Engineering Workflow

Every example in this repository follows the same engineering workflow.

```
Research
      │
      ▼
Explore SDK
      │
      ▼
Inspect APIs
      │
      ▼
Write Code
      │
      ▼
Execute
      │
      ▼
Verify Output
      │
      ▼
Handle Errors
      │
      ▼
Improve Code
      │
      ▼
Document
      │
      ▼
Commit to Git
      │
      ▼
Publish
```

This ensures every example is verified before becoming part of the repository.

---

# Prerequisites

Before using this repository, you should have:

- Python 3.12 or later
- A Tensorlake account
- A Tensorlake API key
- Git
- Visual Studio Code (recommended)
- Basic Python knowledge

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/tensorlake-sandbox-python-examples.git

cd tensorlake-sandbox-python-examples
```

---

Create a virtual environment.

```bash
python -m venv venv
```

---

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

Install the required packages.

```bash
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file in the project root.

```env
TENSORLAKE_API_KEY=your_api_key
```

Never commit your `.env` file to Git.

Instead, use the provided `.env.example` as a template.

---

# Running Examples

Each example is completely independent.

Navigate to the example folder.

Example:

```bash
cd examples/01_create_sandbox
```

Run the example.

```bash
python main.py
```

Each example folder contains:

```
Example Folder/

├── main.py
├── README.md
├── output.txt
└── images/
```

- **main.py** – Working source code.
- **README.md** – Explanation of the example.
- **output.txt** – Actual terminal output.
- **images/** – Screenshots and diagrams, where applicable.

---

# Documentation

This repository contains several supporting documents to make learning and contributing easier.

| Document | Description |
|----------|-------------|
| **README.md** | Project overview and getting started guide |
| **AGENTS.md** | Instructions for AI coding assistants (Codex, Copilot, Claude, Cursor) |
| **ROADMAP.md** | Project roadmap and progress tracking |
| **notes.md** | Engineering notebook documenting experiments and discoveries |
| **CONTRIBUTING.md** | Contribution guidelines |
| **CHANGELOG.md** | Project release history |

---

# Engineering Standards

Every example in this repository follows a common set of engineering standards.

## Code Quality

- Production-quality Python code
- Meaningful variable names
- Modular design
- Comprehensive comments
- Clear docstrings
- Consistent formatting
- PEP 8 compliant

---

## Verification

Every example must be:

- Executed successfully
- Verified against actual SDK behavior
- Compared with official documentation
- Documented with expected output

Nothing is added based on assumptions.

---

## Error Handling

Examples should gracefully handle:

- Missing API keys
- Authentication failures
- Invalid commands
- Network issues
- Timeouts
- Unexpected SDK exceptions

Errors are treated as learning opportunities and documented whenever they reveal useful SDK behavior.

---

## Documentation

Each example includes:

- Objective
- Prerequisites
- Source code
- Execution steps
- Expected output
- Explanation
- Lessons learned
- References (where applicable)

---

# AI Assistant Support

This repository is designed to work well with AI coding assistants, including:

- GitHub Copilot
- OpenAI Codex
- Claude Code
- Cursor

The **AGENTS.md** file contains project-specific instructions that help AI assistants:

- Understand the repository structure
- Continue experiments without repeating work
- Follow project conventions
- Verify APIs before using them
- Update documentation as the project evolves

---

# Engineering Philosophy

This project follows a simple philosophy:

> **Research → Build → Verify → Document → Share**

The emphasis is on understanding how Tensorlake works through experimentation rather than relying solely on documentation.

Every discovery, limitation, and best practice is recorded so future readers can learn from real engineering experiences.

---

# Repository Roadmap

The long-term vision for this repository includes:

## Phase 1 — Foundations

- Environment setup
- Sandbox creation
- Command execution
- Stateful filesystem

## Phase 2 — Sandbox Capabilities

- Package installation
- Native file operations
- File management
- Process management

## Phase 3 — Advanced Features

- Snapshots
- Checkpoints
- Suspend and resume
- Long-running processes
- Parallel execution

## Phase 4 — AI Workloads

- Browser automation
- Computer-use agents
- AI agent architectures
- Multi-agent systems

## Phase 5 — Production Patterns

- Secure code execution
- Background workers
- Deployment strategies
- Best practices

---

# Planned Medium Article Series

This repository will support a technical article series covering topics such as:

1. Building Your First Tensorlake Sandbox
2. Running Python Inside Tensorlake Sandboxes
3. Understanding Stateful Execution
4. Installing Packages and Managing Dependencies
5. Working with Native File APIs
6. Snapshots, Checkpoints, and Recovery
7. Suspend and Resume Workflows
8. Long-Running AI Applications
9. Parallel Sandbox Architectures
10. Browser Automation with Tensorlake
11. Building Stateful AI Agents
12. Production AI Execution Patterns

Each article will reference the corresponding example folder from this repository.

---

# Contributing

Contributions are welcome.

If you discover:

- SDK improvements
- Better engineering practices
- Bugs
- Documentation improvements
- Additional use cases

please feel free to open an issue or submit a pull request.

Please read **CONTRIBUTING.md** before contributing.

---

# License

This project is licensed under the **MIT License**.

See the **LICENSE** file for more information.

---

# Acknowledgements

Special thanks to the **Tensorlake Engineering Team** for providing access to the platform and continuously improving the developer experience.

This repository is based entirely on hands-on experimentation and aims to help the AI engineering community learn Tensorlake through practical, reproducible examples.

---

# Author

## Raj Kumar

Engineering Manager | AI/ML Engineer | Generative AI Practitioner

Passionate about building practical AI systems, creating educational content, and sharing engineering knowledge with the developer community.

---

# Connect

- GitHub *(Coming Soon)*
- Medium *(Article series coming soon)*
- LinkedIn *(Profile link to be added)*

---

# Support the Project

If you find this repository useful:

- ⭐ Star the repository
- 🍴 Fork the repository
- 📝 Share it with others
- 💬 Provide feedback
- 🚀 Follow the accompanying Medium article series

Your support helps improve the project and encourages the creation of more practical AI engineering content.

---

## Final Thoughts

The goal of this repository is not simply to demonstrate APIs.

It is to document a real engineering journey—one experiment at a time.

By combining verified examples, engineering notes, and practical articles, this project aims to become a valuable learning resource for developers building modern AI applications with Tensorlake Sandboxes.

Happy Learning! 🚀