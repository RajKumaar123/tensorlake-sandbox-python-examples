"""
Validate network policy control around a long-running Tensorlake worker.

This experiment models a production security pattern where an orchestrator
changes the sandbox egress policy while a persistent worker process remains
alive and keeps local state.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from tensorlake.sandbox import CLEAR_NETWORK_POLICY, NetworkConfig, Sandbox

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

REPOSITORY_ROOT = PROJECT_ROOT.parent
from utils.output_logger import OutputLogger

SANDBOX_NAME = "tensorlake-secure-agent-long-worker-demo"
WORKER_NAME = "secure-agent-worker"
PROJECT_HOST = "buildaisystem.com"
TOOL_HOST = "example.org"
HEARTBEAT_PATH = "/tmp/worker_heartbeat.txt"
STATE_PATH = "/tmp/worker_state.txt"
ISOLATION_RESULT_PATH = "/tmp/isolation_result.txt"
ISOLATION_RESULT_VALUE = "worker-alive-under-network-isolation"


def print_section(log: Callable[[str], None], title: str, underline: str = "-") -> None:
    log()
    log(title)
    log(underline * len(title))


def enum_value(value: Any) -> str:
    return str(getattr(value, "value", getattr(value, "name", value)))


def traced_value(result: Any) -> Any:
    return getattr(result, "value", result)


def log_network_policy(
    log: Callable[[str], None],
    *,
    allow_internet_access: bool,
    allow_out: list[str] | None = None,
    deny_out: list[str] | None = None,
) -> None:
    print_section(log, "Active Network Policy")
    log(f"allow_internet_access : {allow_internet_access}")
    log(f"allow_out             : {', '.join(allow_out or []) or '<empty>'}")
    log(f"deny_out              : {', '.join(deny_out or []) or '<empty>'}")


def apply_network_policy(
    log: Callable[[str], None],
    sandbox: Sandbox,
    *,
    allow_internet_access: bool,
    allow_out: list[str] | None = None,
    deny_out: list[str] | None = None,
) -> None:
    """Apply a runtime egress policy to the running sandbox."""
    log_network_policy(
        log,
        allow_internet_access=allow_internet_access,
        allow_out=allow_out,
        deny_out=deny_out,
    )
    policy_kwargs = {"allow_internet_access": allow_internet_access}
    if allow_out is not None:
        policy_kwargs["allow_out"] = allow_out
    if deny_out is not None:
        policy_kwargs["deny_out"] = deny_out

    sandbox.update(network=NetworkConfig(**policy_kwargs))


def probe_https(
    log: Callable[[str], None],
    sandbox: Sandbox,
    hostname: str,
    expect_success: bool,
) -> None:
    """Probe network reachability without reading response bodies."""
    code = (
        "import http.client, socket, ssl, sys, urllib.error, urllib.request\n"
        f"hostname = {hostname!r}\n"
        "url = f'https://{hostname}/'\n"
        "request = urllib.request.Request(\n"
        "    url,\n"
        "    headers={'User-Agent': 'Tensorlake-Network-Policy-Experiment/1.0'},\n"
        ")\n"
        "try:\n"
        "    with urllib.request.urlopen(request, timeout=5) as response:\n"
        "        print(f'REACHABLE status={response.status}')\n"
        "except urllib.error.HTTPError as exc:\n"
        "    print(f'REACHABLE status={exc.code}')\n"
        "except (\n"
        "    urllib.error.URLError,\n"
        "    TimeoutError,\n"
        "    socket.timeout,\n"
        "    socket.gaierror,\n"
        "    ConnectionError,\n"
        "    OSError,\n"
        "    ssl.SSLError,\n"
        "    http.client.HTTPException,\n"
        ") as exc:\n"
        "    reason = getattr(exc, 'reason', exc)\n"
        "    print(f'BLOCKED error={type(exc).__name__} reason={reason}')\n"
        "    sys.exit(1)\n"
    )

    result = sandbox.run(command="python", args=["-c", code])
    output = (result.stdout or "").strip()
    error = (result.stderr or "").strip()
    reachable = False
    http_status = "<none>"
    network_error = "<none>"

    for line in output.splitlines():
        if line.startswith("REACHABLE "):
            reachable = True
            http_status = line.removeprefix("REACHABLE status=").strip()
        elif line.startswith("BLOCKED "):
            network_error = line.removeprefix("BLOCKED ").strip()

    expected_text = "reachable" if expect_success else "blocked"
    actual_text = "reachable" if reachable else "blocked"

    print_section(log, "Connectivity Test")
    log(f"destination : https://{hostname}")
    log(f"expected    : {expected_text}")
    log(f"actual      : {actual_text}")
    log(f"http status : {http_status}")
    log(f"network     : {actual_text}")
    if network_error != "<none>":
        log(f"network err : {network_error}")
    log(f"stdout      : {output or '<empty>'}")
    log(f"stderr      : {error or '<empty>'}")
    log(f"result      : {'PASS' if reachable == expect_success else 'FAIL'}")

    if reachable != expect_success:
        raise RuntimeError(
            f"Connectivity expectation failed for {hostname}: "
            f"expected {expected_text}, got {actual_text}"
        )


def run_checked_command(
    log: Callable[[str], None],
    sandbox: Sandbox,
    *,
    title: str,
    command: str,
    args: list[str],
    expected_stdout: str | None = None,
) -> str:
    result = sandbox.run(command=command, args=args)
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()

    print_section(log, title)
    log(f"exit code : {result.exit_code}")
    log(f"stdout    : {stdout or '<empty>'}")
    log(f"stderr    : {stderr or '<empty>'}")

    if result.exit_code != 0:
        raise RuntimeError(f"{title} failed with exit code {result.exit_code}")
    if expected_stdout is not None and stdout != expected_stdout:
        raise RuntimeError(
            f"{title} expected stdout {expected_stdout!r}, got {stdout!r}"
        )

    log("result    : PASS")
    return stdout


def worker_code() -> str:
    return (
        "from pathlib import Path\n"
        "import os, time\n"
        f"heartbeat_path = Path({HEARTBEAT_PATH!r})\n"
        f"state_path = Path({STATE_PATH!r})\n"
        "state_path.write_text('worker-started', encoding='utf-8')\n"
        "counter = 0\n"
        "while True:\n"
        "    counter += 1\n"
        "    heartbeat_path.write_text(\n"
        "        f'pid={os.getpid()} counter={counter} timestamp={time.time()}',\n"
        "        encoding='utf-8',\n"
        "    )\n"
        "    time.sleep(1)\n"
    )


def start_worker(log: Callable[[str], None], sandbox: Sandbox) -> int:
    start_result = sandbox.start_process(
        command="python",
        args=["-c", worker_code()],
        name=WORKER_NAME,
    )
    process = traced_value(start_result)
    pid = getattr(process, "pid", None)
    if pid is None:
        raise RuntimeError("Worker PID could not be determined.")

    managed = getattr(process, "managed", None)
    status = enum_value(getattr(process, "status", "<unknown>"))

    print_section(log, "Worker Process")
    log(f"name   : {getattr(managed, 'name', WORKER_NAME)}")
    log(f"pid    : {pid}")
    log(f"status : {status}")
    if status != "running":
        raise RuntimeError(f"Worker started with unexpected status: {status}")

    return int(pid)


def get_worker_process(sandbox: Sandbox, expected_pid: int) -> Any:
    process = traced_value(sandbox.get_process(process=expected_pid))
    actual_pid = getattr(process, "pid", None)
    if actual_pid != expected_pid:
        raise RuntimeError(
            f"Worker PID changed unexpectedly: expected {expected_pid}, got {actual_pid}"
        )
    return process


def parse_heartbeat(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for part in text.split():
        key, _, value = part.partition("=")
        if key and value:
            values[key] = value
    return values


def verify_worker_continuity(
    log: Callable[[str], None],
    sandbox: Sandbox,
    *,
    expected_pid: int,
) -> None:
    process = get_worker_process(sandbox, expected_pid)
    status = enum_value(getattr(process, "status", "<unknown>"))
    managed = getattr(process, "managed", None)
    managed_status = enum_value(getattr(managed, "status", "<unknown>"))

    code = (
        "from pathlib import Path\n"
        "import time\n"
        f"heartbeat_path = Path({HEARTBEAT_PATH!r})\n"
        "before = heartbeat_path.read_text(encoding='utf-8')\n"
        "time.sleep(2)\n"
        "after = heartbeat_path.read_text(encoding='utf-8')\n"
        "print(before)\n"
        "print(after)\n"
    )
    result = sandbox.run(command="python", args=["-c", code])
    if result.exit_code != 0:
        raise RuntimeError(f"Heartbeat check failed: {result.stderr}")

    lines = [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]
    if len(lines) != 2:
        raise RuntimeError(f"Unexpected heartbeat output: {result.stdout!r}")

    before = parse_heartbeat(lines[0])
    after = parse_heartbeat(lines[1])
    before_counter = int(before.get("counter", "0"))
    after_counter = int(after.get("counter", "0"))
    before_pid = int(before.get("pid", "0"))
    after_pid = int(after.get("pid", "0"))
    advancing = after_counter > before_counter
    pid_stable = before_pid == expected_pid and after_pid == expected_pid

    print_section(log, "Worker Continuity")
    log(f"expected pid   : {expected_pid}")
    log(f"actual pid     : {getattr(process, 'pid', '<missing>')}")
    log(f"status         : {status}")
    log(f"managed status : {managed_status}")
    log(f"heartbeat      : {'advancing' if advancing else 'stalled'}")
    log(f"counter before : {before_counter}")
    log(f"counter after  : {after_counter}")
    log(f"result         : {'PASS' if status == 'running' and advancing and pid_stable else 'FAIL'}")

    if status != "running":
        raise RuntimeError(f"Worker process is not running: {status}")
    if not pid_stable:
        raise RuntimeError("Worker heartbeat PID did not match the original worker PID.")
    if not advancing:
        raise RuntimeError("Worker heartbeat did not advance.")


def update_worker_state(
    log: Callable[[str], None],
    sandbox: Sandbox,
    value: str,
) -> None:
    code = (
        "from pathlib import Path\n"
        f"Path({STATE_PATH!r}).write_text({value!r}, encoding='utf-8')\n"
        f"print(Path({STATE_PATH!r}).read_text(encoding='utf-8'))\n"
    )
    run_checked_command(
        log,
        sandbox,
        title="Worker State Update",
        command="python",
        args=["-c", code],
        expected_stdout=value,
    )
    log(f"file      : {STATE_PATH}")
    log(f"value     : {value}")


def verify_file_value(
    log: Callable[[str], None],
    sandbox: Sandbox,
    *,
    path: str,
    expected_value: str,
    title: str,
) -> None:
    code = (
        "from pathlib import Path\n"
        f"path = Path({path!r})\n"
        "if not path.exists():\n"
        "    raise FileNotFoundError(path)\n"
        "print(path.read_text(encoding='utf-8').strip())\n"
    )
    run_checked_command(
        log,
        sandbox,
        title=title,
        command="python",
        args=["-c", code],
        expected_stdout=expected_value,
    )
    log(f"file      : {path}")
    log(f"value     : {expected_value}")


def run_isolated_local_computation(log: Callable[[str], None], sandbox: Sandbox) -> None:
    code = (
        "from pathlib import Path\n"
        f"state = Path({STATE_PATH!r}).read_text(encoding='utf-8').strip()\n"
        "if state != 'phase-2-complete':\n"
        "    raise RuntimeError(f'unexpected worker state: {state}')\n"
        f"Path({ISOLATION_RESULT_PATH!r}).write_text({ISOLATION_RESULT_VALUE!r}, encoding='utf-8')\n"
        "print('worker-alive-under-network-isolation')\n"
    )
    run_checked_command(
        log,
        sandbox,
        title="Local Execution Under Network Isolation",
        command="python",
        args=["-c", code],
        expected_stdout=ISOLATION_RESULT_VALUE,
    )


def stop_worker(log: Callable[[str], None], sandbox: Sandbox, pid: int) -> None:
    print_section(log, "Worker Shutdown")
    try:
        sandbox.kill_process(process=pid)
        log(f"stop requested for pid : {pid}")
    except Exception as exc:
        log(f"stop request failed    : {exc}")
        raise

    try:
        process = get_worker_process(sandbox, pid)
        status = enum_value(getattr(process, "status", "<unknown>"))
    except Exception:
        status = "stopped"

    log(f"status after stop     : {status}")
    if status == "running":
        raise RuntimeError(f"Worker PID {pid} is still running after shutdown.")
    log("result                : PASS")


def main() -> None:
    logger = OutputLogger(__file__)
    log = logger.log

    load_dotenv(REPOSITORY_ROOT / ".env")
    api_key = os.getenv("TENSORLAKE_API_KEY")
    if not api_key:
        raise ValueError("TENSORLAKE_API_KEY is missing. Add it to your .env file.")

    sandbox = None
    worker_pid: int | None = None

    try:
        log("Long-Running Worker Policy Control")
        log("==================================")
        log("Model: worker identity + worker state + dynamic network policy")

        sandbox = Sandbox.create(
            api_key=api_key,
            name=SANDBOX_NAME,
            allow_internet_access=True,
        )
        print_section(log, "Sandbox")
        log(f"sandbox id   : {sandbox.sandbox_id}")
        log(f"sandbox name : {sandbox.name}")

        worker_pid = start_worker(log, sandbox)
        verify_worker_continuity(log, sandbox, expected_pid=worker_pid)
        verify_file_value(
            log,
            sandbox,
            path=STATE_PATH,
            expected_value="worker-started",
            title="Initial Worker State",
        )

        print_section(log, "Phase 1: Approved Project Access", "=")
        apply_network_policy(
            log,
            sandbox,
            allow_internet_access=True,
            allow_out=[PROJECT_HOST],
            deny_out=[],
        )
        probe_https(log, sandbox, PROJECT_HOST, expect_success=True)
        probe_https(log, sandbox, TOOL_HOST, expect_success=False)
        verify_worker_continuity(log, sandbox, expected_pid=worker_pid)
        update_worker_state(log, sandbox, "phase-1-complete")

        print_section(log, "Phase 2: Change Approved Service", "=")
        apply_network_policy(
            log,
            sandbox,
            allow_internet_access=True,
            allow_out=[TOOL_HOST],
            deny_out=[],
        )
        probe_https(log, sandbox, TOOL_HOST, expect_success=True)
        probe_https(log, sandbox, PROJECT_HOST, expect_success=False)
        verify_worker_continuity(log, sandbox, expected_pid=worker_pid)
        verify_file_value(
            log,
            sandbox,
            path=STATE_PATH,
            expected_value="phase-1-complete",
            title="Worker State Persistence",
        )
        update_worker_state(log, sandbox, "phase-2-complete")

        print_section(log, "Phase 3: Network-Isolated Execution", "=")
        apply_network_policy(log, sandbox, allow_internet_access=False)
        probe_https(log, sandbox, PROJECT_HOST, expect_success=False)
        probe_https(log, sandbox, TOOL_HOST, expect_success=False)
        verify_worker_continuity(log, sandbox, expected_pid=worker_pid)
        verify_file_value(
            log,
            sandbox,
            path=STATE_PATH,
            expected_value="phase-2-complete",
            title="Worker State Under Isolation",
        )
        run_isolated_local_computation(log, sandbox)
        verify_file_value(
            log,
            sandbox,
            path=ISOLATION_RESULT_PATH,
            expected_value=ISOLATION_RESULT_VALUE,
            title="Isolation Result Verification",
        )
        update_worker_state(log, sandbox, "phase-3-complete")

        print_section(log, "Phase 4: Recovery", "=")
        print_section(log, "Active Network Policy")
        log("network : CLEAR_NETWORK_POLICY")
        sandbox.update(network=CLEAR_NETWORK_POLICY)
        probe_https(log, sandbox, PROJECT_HOST, expect_success=True)
        probe_https(log, sandbox, TOOL_HOST, expect_success=True)
        verify_worker_continuity(log, sandbox, expected_pid=worker_pid)
        verify_file_value(
            log,
            sandbox,
            path=STATE_PATH,
            expected_value="phase-3-complete",
            title="Worker State After Recovery",
        )
        verify_file_value(
            log,
            sandbox,
            path=ISOLATION_RESULT_PATH,
            expected_value=ISOLATION_RESULT_VALUE,
            title="Final Isolation Result",
        )
        update_worker_state(log, sandbox, "phase-4-complete")

        stop_worker(log, sandbox, worker_pid)
        worker_pid = None

        log()
        log("Long-running worker policy control experiment completed successfully.")

    except Exception as exc:
        log()
        log(f"Experiment failed: {exc}")
        raise

    finally:
        if sandbox is not None and worker_pid is not None:
            try:
                stop_worker(log, sandbox, worker_pid)
            except Exception as cleanup_exc:
                log()
                log(f"Worker cleanup failed: {cleanup_exc}")
        if sandbox is not None:
            log()
            log("Terminating sandbox...")
            try:
                sandbox.terminate()
                log("Sandbox terminated.")
            except Exception as cleanup_exc:
                log(f"Sandbox cleanup failed: {cleanup_exc}")
        logger.save()


if __name__ == "__main__":
    main()
