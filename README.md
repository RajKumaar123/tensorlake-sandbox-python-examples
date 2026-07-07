# Tensorlake Sandbox Python Examples

> A production-ready collection of Python examples demonstrating how to build, explore, and document Tensorlake Sandbox workflows.

## Overview

This repository is a practical engineering guide for learning Tensorlake Sandboxes through verified Python examples.

Every example in this repository is:

- Executed successfully
- Verified against actual SDK behavior
- Documented with explanations
- Easy to reproduce
- Built with engineering best practices

The goal is to create a high-quality open-source resource for developers who want to understand Tensorlake Sandboxes as isolated, stateful execution environments for modern AI applications.

## Quick Start

1. Clone the repository.

```bash
git clone https://github.com/<your-username>/tensorlake-sandbox-python-examples.git
cd tensorlake-sandbox-python-examples
```

2. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages.

```bash
pip install tensorlake python-dotenv
```

4. Add your Tensorlake API key to `.env`.

```env
TENSORLAKE_API_KEY=your_api_key
```

5. Run an example.

```bash
cd examples/01_create_sandbox
python main.py
```

## Repository Structure

```
tensorlake-sandbox-python-examples/
|-- README.md
|-- .env.example
|-- .gitignore
|-- docs/
|   |-- AGENTS.md
|   |-- CHANGELOG.md
|   |-- CONTRIBUTING.md
|   |-- example_completion_checklist.md
|   |-- notes.md
|   `-- ROADMAP.md
|-- examples/
|   |-- 01_create_sandbox/
|   |-- 02_run_commands/
|   |-- 03_stateful_filesystem/
|   |-- 04_install_packages/
|   |-- 05_native_file_api/
|   |-- 06_snapshots/
|   |-- 07_suspend_resume/
|   |-- 08_process_management/
|   |-- 09_parallel_sandboxes/
|   |-- 10_browser_automation/
|   |-- 11_computer_use/
|   `-- 12_ai_agent_demo/
|-- experiments/
`-- utils/
    `-- common.py
```

## Learning Roadmap

The repository follows a progressive learning path, starting with the fundamentals and gradually moving toward advanced AI agent workflows.

### Phase 1 - Fundamentals

- Environment Setup
- Creating a Sandbox
- Running Commands
- Understanding the Sandbox Lifecycle
- Stateful Filesystem

### Phase 2 - Working with Sandboxes

- Installing Packages
- Native File Operations
- Uploading Files
- Reading Files
- Managing Directories

### Phase 3 - Advanced Sandbox Features

- Snapshots
- Checkpoints
- Suspend & Resume
- Process Management
- Long-running Applications

### Phase 4 - AI Workloads

- Parallel Sandboxes
- Browser Automation
- Computer Use
- AI Agents
- Multi-Agent Systems

### Phase 5 - Production Patterns

- Secure Code Execution
- Background Workers
- Stateful Agents
- Deployment Patterns
- Best Practices

## Example Index

| Example | Description | Status |
|----------|-------------|--------|
| 01 | Create Your First Sandbox | Completed |
| 02 | Execute Commands | Completed |
| 03 | Stateful Filesystem | Completed |
| 04 | Installing Python Packages | Completed |
| 05 | Native File APIs | Completed |
| 06 | Snapshots & Checkpoints | Completed |
| 07 | Suspend & Resume | Completed |
| 08 | Process Management | Completed |
| 09 | Parallel Sandboxes | Completed |
| 10 | Browser Automation | Completed |
| 11 | Computer Use | Completed |
| 12 | AI Agent Demo | Completed |

## Running Examples

Each example is independent.

Navigate to the example folder:

```bash
cd examples/01_create_sandbox
```

Run the example:

```bash
python main.py
```

Each example folder contains:

```
Example Folder/
|-- main.py
|-- README.md
|-- output.txt
`-- images/
```

- `main.py` - Working source code.
- `README.md` - Explanation of the example.
- `output.txt` - Actual terminal output.
- `images/` - Screenshots and diagrams, where applicable.

## Documentation

This repository contains supporting documents to make learning and contributing easier.

| Document | Description |
|----------|-------------|
| `README.md` | Project overview and getting started guide |
| `docs/AGENTS.md` | Instructions for AI coding assistants |
| `docs/ROADMAP.md` | Project roadmap and progress tracking |
| `docs/notes.md` | Engineering notebook documenting experiments and discoveries |
| `docs/CONTRIBUTING.md` | Contribution guidelines |
| `docs/CHANGELOG.md` | Project release history |
| `docs/example_completion_checklist.md` | Completion checklist used for example reviews |

## Engineering Standards

Every example in this repository follows a common set of engineering standards.

### Code Quality

- Production-quality Python code
- Meaningful variable names
- Modular design
- Comprehensive comments
- Clear docstrings
- Consistent formatting
- PEP 8 compliant

### Verification

Every example must be:

- Executed successfully
- Verified against actual SDK behavior
- Compared with official documentation
- Documented with expected output

Nothing is added based on assumptions.

### Error Handling

Examples should gracefully handle:

- Missing API keys
- Authentication failures
- Invalid commands
- Network issues
- Timeouts
- Unexpected SDK exceptions

Errors are treated as learning opportunities and documented whenever they reveal useful SDK behavior.

### Documentation

Each example includes:

- Objective
- Prerequisites
- Source code
- Execution steps
- Expected output
- Explanation
- Lessons learned
- References, where applicable

## AI Assistant Support

This repository is designed to work well with AI coding assistants, including:

- GitHub Copilot
- OpenAI Codex
- Claude Code
- Cursor

The `docs/AGENTS.md` file contains project-specific instructions that help AI assistants:

- Understand the repository structure
- Continue experiments without repeating work
- Follow project conventions
- Verify APIs before using them
- Update documentation as the project evolves

## Planned Medium Article Series

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

## Contributing

Contributions are welcome.

If you discover:

- SDK improvements
- Better engineering practices
- Bugs
- Documentation improvements
- Additional use cases

please feel free to open an issue or submit a pull request.

Please read `docs/CONTRIBUTING.md` before contributing.

## Acknowledgements

Special thanks to the Tensorlake Engineering Team for providing access to the platform and continuously improving the developer experience.

This repository is based entirely on hands-on experimentation and aims to help the AI engineering community learn Tensorlake through practical, reproducible examples.

## Author

### Raj Kumar

Engineering Manager | AI/ML Engineer | Generative AI Practitioner

Passionate about building practical AI systems, creating educational content, and sharing engineering knowledge with the developer community.

## Connect

- GitHub
- Medium
- LinkedIn

## Support the Project

If you find this repository useful:

- Star the repository
- Fork the repository
- Share it with others
- Provide feedback
- Follow the accompanying Medium article series

## Final Thoughts

The goal of this repository is not simply to demonstrate APIs.

It is to document a real engineering journey, one experiment at a time.

By combining verified examples, engineering notes, and practical articles, this project aims to become a valuable learning resource for developers building modern AI applications with Tensorlake Sandboxes.

Happy Learning!
