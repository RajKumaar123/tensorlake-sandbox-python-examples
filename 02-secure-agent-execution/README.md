# Secure AI Agent Execution with Dynamic Network Policies in Tensorlake Sandboxes

AI agents and autonomous workloads often need different network privileges at
different execution phases. A worker may need access to one trusted source
during setup, another approved service during a tool call, and no outbound
network access while running generated or untrusted local code.

This project demonstrates how a running Tensorlake Sandbox can dynamically
change its outbound network policy while preserving execution state and a
long-running worker process. It is a controlled technical demonstration, not a
complete autonomous agent framework.

## What This Project Demonstrates

- Dynamic egress policy changes on a running sandbox
- Hostname allowlisting with `NetworkConfig`
- Runtime policy transitions with `Sandbox.update(network=...)`
- Block-all network isolation with `allow_internet_access=False`
- State persistence across network-policy changes
- Persistent process continuity across policy changes
- Local execution while outbound networking is blocked
- Controlled recovery with `CLEAR_NETWORK_POLICY`
- Cleanup of worker processes and sandboxes

## Security Model

```text
Grant only the network privilege required by the current execution phase.
```

The execution lifecycle and privilege lifecycle do not have to be identical. A
long-running worker can remain alive for the whole workflow while the host-side
controller changes which destinations are reachable at each phase.

## Architecture

```text
Host Orchestrator
       |
       | Sandbox.update(network=...)
       v
+---------------------------------------+
|         Tensorlake Sandbox            |
|                                       |
|   Persistent Worker                   |
|      |                                |
|      +--> State / heartbeat           |
|      |                                |
|      +--> Local computation           |
|                                       |
|   Dynamic Egress Boundary             |
+-------------------+-------------------+
                    |
          phase-specific access
                    |
       +------------+-------------+
       |                          |
buildaisystem.com          www.tensorlake.ai
```

The worker does not decide its own network permissions. The host-side
orchestrator changes the sandbox network boundary.

## Experiment Progression

### Experiment 01 - Inspect Network Policy

Inspects the installed Tensorlake SDK surface and records the networking APIs
available in `tensorlake==0.5.103`, including `NetworkConfig`,
`Sandbox.update(network=...)`, hostname rules, IP/CIDR rules, and
`CLEAR_NETWORK_POLICY`.

### Experiment 02 - Runtime Policy Transition

Validates that one running sandbox can move through baseline connectivity,
hostname allowlisting, switched allowlisting, block-all isolation, and policy
clearing without recreating the sandbox.

### Experiment 03 - Phase-Based Secure Tool Access

Models phase-specific least privilege. It verifies controlled external access,
state persistence, local-only execution while networking is blocked, and
recovery afterward.

### Experiment 04 - Long-Running Worker Policy Control

Adds process continuity. A managed worker process keeps the same PID and an
advancing heartbeat while the sandbox network policy changes around it.

### Experiment 05 - Secure Agent Execution Workflow

Integrates the validated primitives into a production-style secure execution
workflow. It simulates trusted context access, approved platform/tool access,
network-isolated local execution, recovery, state verification, worker cleanup,
and sandbox cleanup.

## Final Workflow

```text
Phase 1
Trusted context access
Allowed: buildaisystem.com

        |
        v

Phase 2
Approved platform/tool access
Allowed: www.tensorlake.ai

        |
        v

Phase 3
Network-isolated execution
Outbound access: blocked
Worker: running
State: preserved
Local computation: allowed

        |
        v

Phase 4
Controlled recovery
Network policy: cleared
Connectivity: restored
```

## Verified Final Result

Experiment 05 produced this successful summary:

```text
worker continuity            : PASS
phase-based access control   : PASS
trusted context access       : PASS
tool access transition       : PASS
network isolation            : PASS
state persistence            : PASS
local isolated execution     : PASS
network recovery             : PASS
final result                 : secure-agent-execution-complete
```

These results demonstrate the behavior of these experiments in the validated
environment. They are not a universal security proof.

## Project Structure

```text
02-secure-agent-execution/
  README.md
  experiments/
    01_inspect_network_policy/
      main.py
      output.txt
    02_runtime_policy_transition/
      main.py
      output.txt
    03_phase_based_secure_tool_access/
      main.py
      output.txt
    04_long_running_worker_policy_control/
      main.py
      output.txt
    05_secure_agent_execution_workflow/
      main.py
      output.txt
  utils/
    __init__.py
    output_logger.py
```

## Prerequisites

- Python
- Tensorlake account
- Tensorlake API key
- Tensorlake Python SDK
- `python-dotenv`

These experiments were validated against:

```text
tensorlake==0.5.103
```

Other SDK versions may expose different signatures or behavior.

## Setup

From the repository root, store credentials in the root `.env` file:

```env
TENSORLAKE_API_KEY=your_tensorlake_api_key_here
```

Do not hardcode API keys in experiment files.

On Windows PowerShell, activate the existing virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Then run commands from the repository root.

## Running the Experiments

```powershell
python .\02-secure-agent-execution\experiments\01_inspect_network_policy\main.py
```

```powershell
python .\02-secure-agent-execution\experiments\02_runtime_policy_transition\main.py
```

```powershell
python .\02-secure-agent-execution\experiments\03_phase_based_secure_tool_access\main.py
```

```powershell
python .\02-secure-agent-execution\experiments\04_long_running_worker_policy_control\main.py
```

```powershell
python .\02-secure-agent-execution\experiments\05_secure_agent_execution_workflow\main.py
```

You can also call the repository virtual environment interpreter directly:

```powershell
& .\venv\Scripts\python.exe .\02-secure-agent-execution\experiments\05_secure_agent_execution_workflow\main.py
```

## Understanding output.txt

Each experiment writes its console evidence to an `output.txt` file beside its
`main.py`. These files are intentionally kept as debugging and publication
evidence.

The project-local `OutputLogger(__file__)` resolves the current experiment
directory and overwrites that experiment's `output.txt` on each run.

## Security Notes

- Never hardcode API keys.
- Keep network allowlists narrowly scoped to the active workload phase.
- Outbound blocking does not replace application-level authorization.
- Production destinations should be selected from actual workload requirements.
- Credentials should not be written into experiment output.
- Public destination availability can affect connectivity tests.

## Important Limitations

- This is a controlled demonstration, not a complete AI agent implementation.
- It does not test every possible DNS or network edge case.
- Public website reachability can change.
- Successful isolation tests are not a formal security audit.
- Production systems still need authentication, authorization, observability,
  secret management, policy governance, and operational monitoring.

## Why This Matters for AI Agents

Tool-using agents often require temporary access to external services. Generated
or untrusted code may benefit from stricter isolation. This project shows how a
controller can keep a worker alive while changing the sandbox network boundary
around each execution phase.

## License / Repository Context

This folder is part of the broader `tensorlake-sandbox-python-examples`
repository. No license is declared in this folder.
