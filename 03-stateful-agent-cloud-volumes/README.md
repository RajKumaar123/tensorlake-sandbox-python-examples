# Persistent State for AI Agents with Tensorlake Cloud Volumes

Article 3 demonstrates how ephemeral sandbox compute can be replaced while workflow filesystem state remains reusable, versioned, recoverable, and shareable across Tensorlake sandboxes.

## Status

Implementation complete. All five experiments were validated successfully with the evidence preserved in this directory.

## Environment

- Python 3.12.2
- `tensorlake==0.5.123`
- Isolated environment: `03-stateful-agent-cloud-volumes/.venv`

Do not use the repository root `venv`; earlier articles depend on it.

## Setup

From the repository root in Windows PowerShell:

```powershell
cd 03-stateful-agent-cloud-volumes
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install tensorlake==0.5.123
```

The experiments load `TENSORLAKE_API_KEY` from the existing repository-root `.env`. Do not copy the real value into this directory, print it, or commit it. The root `.env` is ignored by Git. A safe example is:

```text
TENSORLAKE_API_KEY=your_tensorlake_api_key
```

## Experiment Order

The experiments are intentionally incremental and share Cloud Volume state. Run them in this order from the Article 3 directory:

```powershell
python experiments/01-persistent-workspace/main.py
python experiments/02-replace-the-compute/main.py
python experiments/03-version-and-recover/main.py
python experiments/04-immutable-consumer/main.py
python experiments/05-shared-state-across-workers/main.py
```

### 1. Persistent Workspace

Sandbox A writes workflow state to a mounted Cloud Volume. The host verifies the published file through `Filesystem.read_file()` with matching bytes and hash.

### 2. Replace the Compute

After Sandbox A terminates, Sandbox B mounts the same Cloud Volume, reads Stage 1, and continues the workflow by writing Stage 2.

### 3. Version and Recover

A permanent known-good snapshot is created, current state is modified, historical state is read, and a separate recovery filesystem is forked from the snapshot. This validates recovery; it is not in-place rollback.

### 4. Immutable Consumer

A new sandbox mounts the permanent snapshot with `read_only=True` and `snapshot_id`. It reads the known-good state and verifies that mutation is rejected with the observed read-only filesystem behavior.

### 5. Shared State Across Workers

Two sandboxes mount the same writable Cloud Volume and write separate worker-owned subtrees. Host-side reads and cross-worker reads verify the resulting shared state. This demonstrates disjoint-path ownership, not transactional coordination.

## Evidence

Each experiment preserves `output.txt` and `result.json` as committed reproducibility evidence. Hashes, byte counts, IDs, timing observations, and PASS/FAIL results reflect the actual validated runs.

## Resource Lifecycle

Running these experiments creates and mutates Tensorlake cloud resources, including sandboxes, Cloud Volumes/filesystems, permanent snapshots, and recovery filesystem state. Cleanup is not universal or automatic. Some resources were intentionally retained after validation so article evidence and screenshots could be preserved.

Inspect your Tensorlake resources after running the experiments and delete anything you no longer need according to your retention requirements. Permanent snapshots may remain until explicitly deleted and should be managed intentionally. Do not use destructive cleanup commands unless their targets and behavior have been independently verified.

## Technical Boundaries

Do not infer instant durability, synchronous replication, transactional multi-writer behavior, conflict-free same-path writes, in-place rollback, runtime/process inheritance between sandboxes, or that Cloud Volumes are Tensorlake's only state-preservation mechanism.

Experiment 5 assigns separate worker-owned paths. Cloud Volumes are not a transactional database, distributed lock system, or Git conflict-resolution system. Competing writes to the same path require application-level coordination.

A Sandbox snapshot preserves or recreates execution-environment state. A Cloud Volume provides workflow filesystem state that can be reused across execution environments. Neither mechanism is universally better; they address different lifecycle needs.

## Repository Structure

The local `.venv`, Python caches, and bytecode are excluded from this article tree:

```text
03-stateful-agent-cloud-volumes/
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
