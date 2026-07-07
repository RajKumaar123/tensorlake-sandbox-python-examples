# Insight Forge

## Project Overview

Insight Forge is a production-quality AI engineering project for researching, organizing, and synthesizing information inside Tensorlake Sandboxes.

The project is designed as a real application rather than a tutorial example. It will eventually support structured research workflows, persistent memory, safe execution, and agent orchestration.

## Business Problem

Teams often need to research a topic, collect evidence, keep context across sessions, and turn that work into a reliable deliverable.

Today that process is usually fragmented across browser tabs, notes, spreadsheets, and ad hoc scripts.

This project aims to provide a structured, repeatable workspace for that workflow.

## Vision

The long-term vision is to create a flagship Tensorlake application that can:

- Coordinate research tasks
- Preserve execution state
- Reuse prior work safely
- Produce repeatable outputs
- Demonstrate real sandbox-powered AI workflows

## Why Tensorlake

Tensorlake Sandboxes are a strong fit because this project needs:

- Isolated execution
- Stateful filesystem behavior
- Safe package installation
- Long-running workflows
- Snapshots and resume
- Parallel work streams
- Reproducible environments

## Architecture Overview

The project will follow a modular architecture with distinct layers for:

- Project configuration
- Sandbox lifecycle management
- Orchestration
- Agents
- Tools
- Memory
- Workflows
- Outputs

Only the foundation is created in this milestone. Business logic will be added in later milestones.

## Planned Features

- Sandbox lifecycle management
- Stateful execution
- Persistent filesystem
- Native file operations
- Snapshot support
- Resume support
- Parallel execution
- Browser automation
- Computer use
- Agent memory
- Tool calling
- Workflow orchestration
- Logging
- Error recovery

## Development Roadmap

1. Project foundation
2. Sandbox manager
3. Research workflow
4. Memory layer
5. Browser automation
6. Parallel execution
7. Snapshots
8. Multi-agent orchestration
9. Production hardening
10. Documentation and release

## Folder Structure

```text
projects/01-insight-forge/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── docs/
├── diagrams/
├── screenshots/
├── outputs/
├── src/
│   └── insight_forge/
├── agents/
├── tools/
├── memory/
├── workflows/
├── prompts/
├── tests/
└── examples/
```

## Getting Started

1. Review the project documentation in `docs/`.
2. Create a virtual environment.
3. Install dependencies from `requirements.txt`.
4. Copy `.env.example` to `.env` and provide required keys.
5. Begin with Milestone 2 after the foundation is approved.

## Package Layout

The Python source code will live under `src/insight_forge/` to support a standard package layout and avoid a flat source directory.

## Current Status

Status: Project foundation only

Implemented:

- Repository scaffold
- Starter documentation
- Project layout

Not yet implemented:

- Agents
- Workflows
- Memory
- Browser automation
- Tensorlake integration
