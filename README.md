# Tensorlake Sandbox Python Examples

This repository contains hands-on Python examples accompanying a progressive engineering series on Tensorlake Sandboxes. The examples move from isolated workload fundamentals to dynamic network security and then to persistent, versioned workflow state with Cloud Volumes.

Each article folder contains implementation-oriented examples and the relevant setup guidance. The examples are validated against the SDK versions documented for their respective article; they are not all pinned to one global SDK version.

## Series Overview

| Part | Focus | Core question | Implementation |
| --- | --- | --- | --- |
| 1 | Sandbox Fundamentals | How do I create and operate an isolated AI workload? | [`examples/`](examples/) |
| 2 | Network Security | How can outbound access change without replacing the workload? | [`02-secure-agent-execution/`](02-secure-agent-execution/) |
| 3 | Persistent State | How can compute be replaceable while workflow state survives independently? | [`03-stateful-agent-cloud-volumes/`](03-stateful-agent-cloud-volumes/) |

## 1. Sandbox Fundamentals

### Getting Started with Tensorlake Sandboxes: Build, Run, and Manage Your First Isolated AI Workload with Python

The foundation examples cover creating sandboxes, executing commands, stateful filesystem behavior, installing Python dependencies such as `pandas`, native file APIs, and Sandbox snapshot/checkpoint lifecycle.

- Implementation: [`examples/`](examples/)
- Article: [Getting Started with Tensorlake Sandboxes](https://pub.towardsai.net/getting-started-with-tensorlake-sandboxes-build-run-and-manage-your-first-isolated-ai-workload-41715d797305)

## 2. Secure Agent Execution

### Secure AI Agents with Tensorlake Dynamic Network Policies

Article 2 explores dynamic outbound network policies for AI agent execution.

**Core principle:** Change the privilege, not the workload.

The validated workflow updates a running sandbox policy without replacing the worker. Existing connections are not interrupted by the update; new outbound connections are evaluated against the updated policy.

- Implementation: [`02-secure-agent-execution/`](02-secure-agent-execution/)
- SDK validation: `tensorlake==0.5.103`
- Article: [Secure AI Agents with Tensorlake Dynamic Network Policies](https://medium.com/towards-artificial-intelligence/secure-ai-agents-with-tensorlake-dynamic-network-policies-3149b7a11e16)

## 3. Persistent Agent State

### Persistent State for AI Agents with Tensorlake Cloud Volumes: Versioning, Recovery, and Sharing Across Sandboxes

Article 3 separates ephemeral compute from durable workflow filesystem state.

**Core principle:** Replace the compute, preserve the workflow state.

The five validated experiments are:

1. Persistent Workspace
2. Replace the Compute
3. Version and Recover
4. Immutable Consumer
5. Shared State Across Workers

The progression is persist state, replace compute, version and recover, consume known-good state read-only, and share state across workers.

- Implementation: [`03-stateful-agent-cloud-volumes/`](03-stateful-agent-cloud-volumes/)
- SDK validation: `tensorlake==0.5.123`, Python `3.12.2`

Implementation complete; all five experiments were validated successfully. The evidence supports replaceable compute, versioned historical reads, fork-based recovery, snapshot-pinned read-only consumption, and disjoint-path sharing. It does not establish instant durability, synchronous replication, transactional multi-writer behavior, conflict-free same-path writes, in-place rollback, runtime/process inheritance between sandboxes, or that Cloud Volumes are Tensorlake's only state-preservation mechanism. Experiment 5 uses separate worker-owned paths; Cloud Volumes are not a transactional database, distributed lock system, or Git conflict-resolution system, so same-path competing writes require application-level coordination.

## Architecture Progression

```text
Sandbox Fundamentals
        |
        v
Network-Constrained Agent Execution
        |
        v
Persistent and Versioned Workflow State
```

The series moves from execution isolation, to execution security, and finally to separating the compute lifecycle from the workflow-state lifecycle.

## Repository Structure

```text
tensorlake-sandbox-python-examples/
├── README.md
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
├── 02-secure-agent-execution/
│   ├── README.md
│   └── experiments/
└── 03-stateful-agent-cloud-volumes/
    ├── README.md
    └── experiments/
        ├── 01-persistent-workspace/
        │   ├── main.py
        │   ├── output.txt
        │   └── result.json
        ├── 02-replace-the-compute/
        │   ├── main.py
        │   ├── output.txt
        │   └── result.json
        ├── 03-version-and-recover/
        │   ├── main.py
        │   ├── output.txt
        │   └── result.json
        ├── 04-immutable-consumer/
        │   ├── main.py
        │   ├── output.txt
        │   └── result.json
        └── 05-shared-state-across-workers/
            ├── main.py
            ├── output.txt
            └── result.json
```

## Reproducibility and SDK Versions

Examples were validated at different points against the SDK versions associated with their article implementation:

- Article 2: `tensorlake==0.5.103`
- Article 3: `tensorlake==0.5.123`, Python `3.12.2`

Article 1 may reflect its historical environment. Read the relevant project README and source before running an example; do not assume that one SDK version applies to the entire repository.

## Getting Started

1. Clone the repository.
2. Choose an article or example folder.
3. Read its README and setup instructions.
4. Create an isolated virtual environment appropriate for that implementation.
5. Configure `TENSORLAKE_API_KEY` through environment configuration without committing the value.
6. Run the relevant example or experiment.

Use a safe placeholder when configuring credentials:

```text
TENSORLAKE_API_KEY=your_tensorlake_api_key
```

Individual projects may use different SDK versions. Follow their documented setup rather than upgrading the repository globally.

## Evidence and Reproducibility

The repository favors executable examples and captured evidence over architecture claims alone. Article 3 preserves `output.txt` and `result.json` for each validated experiment. Other projects may use different evidence-file structures.

## Important Notes

- Tensorlake APIs can evolve; examples reflect the versions against which they were validated.
- Running examples may create or mutate Tensorlake cloud resources.
- Review resource lifecycle and cleanup requirements in the relevant project README before execution.
- Permanent snapshots may remain until explicitly deleted and should be managed intentionally.
- Never commit API keys or other credentials.

A Sandbox Snapshot preserves or recreates execution-environment state. A Cloud Volume provides workflow filesystem state that can be reused across execution environments. Neither mechanism is universally better; they address different lifecycle needs.

## Articles

- [Getting Started with Tensorlake Sandboxes: Build, Run, and Manage Your First Isolated AI Workload with Python](https://pub.towardsai.net/getting-started-with-tensorlake-sandboxes-build-run-and-manage-your-first-isolated-ai-workload-41715d797305)
- [Secure AI Agents with Tensorlake Dynamic Network Policies](https://medium.com/towards-artificial-intelligence/secure-ai-agents-with-tensorlake-dynamic-network-policies-3149b7a11e16)
- Persistent State for AI Agents with Tensorlake Cloud Volumes: Versioning, Recovery, and Sharing Across Sandboxes
