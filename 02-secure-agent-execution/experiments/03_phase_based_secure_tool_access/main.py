"""
Simulate phase-based secure tool access with Tensorlake network policies.

This experiment models a production security pattern for a long-running
automation workload: each execution phase receives only the outbound network
access it needs, while sandbox filesystem state persists across phases.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Callable

from dotenv import load_dotenv
from tensorlake.sandbox import CLEAR_NETWORK_POLICY, NetworkConfig, Sandbox

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

REPOSITORY_ROOT = PROJECT_ROOT.parent
from utils.output_logger import OutputLogger

SANDBOX_NAME = "tensorlake-secure-agent-phase-access-demo"
PROJECT_HOST = "buildaisystem.com"
TOOL_HOST = "example.org"
AGENT_CONTEXT_PATH = "/tmp/agent_context.txt"
TOOL_RESULT_PATH = "/tmp/tool_result.txt"
FINAL_RESULT_PATH = "/tmp/final_result.txt"


def print_phase(log: Callable[[str], None], title: str) -> None:
    log()
    log(title)
    log("=" * len(title))


def log_network_policy(
    log: Callable[[str], None],
    *,
    allow_internet_access: bool,
    allow_out: list[str] | None = None,
    deny_out: list[str] | None = None,
) -> None:
    log()
    log("Active Network Policy")
    log("---------------------")
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
    """Apply a runtime network policy directly to the running sandbox."""
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
    """Probe HTTPS reachability without logging response bodies."""
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
        "        length = response.headers.get('Content-Length', '<unknown>')\n"
        "        print(f'REACHABLE host={hostname} status={response.status} length={length}')\n"
        "except urllib.error.HTTPError as exc:\n"
        "    length = exc.headers.get('Content-Length', '<unknown>')\n"
        "    print(f'REACHABLE host={hostname} status={exc.code} length={length}')\n"
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
    content_length = "<none>"
    network_error = "<none>"

    for line in output.splitlines():
        if line.startswith("REACHABLE "):
            reachable = True
            for part in line.split()[1:]:
                key, _, value = part.partition("=")
                if key == "status":
                    http_status = value
                elif key == "length":
                    content_length = value
        elif line.startswith("BLOCKED "):
            network_error = line.removeprefix("BLOCKED ").strip()

    expected_text = "reachable" if expect_success else "blocked"
    actual_text = "reachable" if reachable else "blocked"

    log()
    log("Connectivity Test")
    log("-----------------")
    log(f"destination    : https://{hostname}")
    log(f"expected       : {expected_text}")
    log(f"actual         : {actual_text}")
    log(f"http status    : {http_status}")
    log(f"content length : {content_length}")
    log(f"network        : {actual_text}")
    if network_error != "<none>":
        log(f"network err    : {network_error}")
    log(f"stdout         : {output or '<empty>'}")
    log(f"stderr         : {error or '<empty>'}")
    log(f"result         : {'PASS' if reachable == expect_success else 'FAIL'}")

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
    """Run a sandbox command and fail if the command or expected output is wrong."""
    result = sandbox.run(command=command, args=args)
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()

    log()
    log(title)
    log("-" * len(title))
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


def write_file(
    log: Callable[[str], None],
    sandbox: Sandbox,
    *,
    path: str,
    value: str,
    title: str,
) -> None:
    code = (
        "from pathlib import Path\n"
        f"path = Path({path!r})\n"
        f"path.write_text({value!r}, encoding='utf-8')\n"
        "print(path.read_text(encoding='utf-8'))\n"
    )
    run_checked_command(
        log,
        sandbox,
        title=title,
        command="python",
        args=["-c", code],
        expected_stdout=value,
    )
    log(f"file      : {path}")
    log(f"value     : {value}")


def verify_file(
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
        "print(path.read_text(encoding='utf-8'))\n"
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


def main() -> None:
    logger = OutputLogger(__file__)
    log = logger.log

    load_dotenv(REPOSITORY_ROOT / ".env")
    api_key = os.getenv("TENSORLAKE_API_KEY")
    if not api_key:
        raise ValueError("TENSORLAKE_API_KEY is missing. Add it to your .env file.")

    sandbox = None
    try:
        log("Phase-Based Secure Tool Access")
        log("==============================")
        log("Model: execution phase -> required privilege -> network policy -> action")

        sandbox = Sandbox.create(
            api_key=api_key,
            name=SANDBOX_NAME,
            allow_internet_access=True,
        )
        log()
        log(f"sandbox id   : {sandbox.sandbox_id}")
        log(f"sandbox name : {sandbox.name}")

        print_phase(log, "Phase 1: Preparation")
        apply_network_policy(
            log,
            sandbox,
            allow_internet_access=True,
            allow_out=[PROJECT_HOST],
            deny_out=[],
        )
        probe_https(log, sandbox, PROJECT_HOST, expect_success=True)
        probe_https(log, sandbox, TOOL_HOST, expect_success=False)
        write_file(
            log,
            sandbox,
            path=AGENT_CONTEXT_PATH,
            value="trusted-context-loaded",
            title="State Action",
        )

        print_phase(log, "Phase 2: Approved Tool Execution")
        apply_network_policy(
            log,
            sandbox,
            allow_internet_access=True,
            allow_out=[TOOL_HOST],
            deny_out=[],
        )
        probe_https(log, sandbox, TOOL_HOST, expect_success=True)
        probe_https(log, sandbox, PROJECT_HOST, expect_success=False)
        write_file(
            log,
            sandbox,
            path=TOOL_RESULT_PATH,
            value="approved-tool-executed",
            title="Tool Action",
        )
        verify_file(
            log,
            sandbox,
            path=AGENT_CONTEXT_PATH,
            expected_value="trusted-context-loaded",
            title="State Continuity Check",
        )

        print_phase(log, "Phase 3: Untrusted Execution")
        apply_network_policy(log, sandbox, allow_internet_access=False)
        probe_https(log, sandbox, PROJECT_HOST, expect_success=False)
        probe_https(log, sandbox, TOOL_HOST, expect_success=False)
        local_code = (
            "from pathlib import Path\n"
            f"context = Path({AGENT_CONTEXT_PATH!r}).read_text(encoding='utf-8').strip()\n"
            f"tool = Path({TOOL_RESULT_PATH!r}).read_text(encoding='utf-8').strip()\n"
            "if context != 'trusted-context-loaded':\n"
            "    raise RuntimeError(f'unexpected context: {context}')\n"
            "if tool != 'approved-tool-executed':\n"
            "    raise RuntimeError(f'unexpected tool result: {tool}')\n"
            f"Path({FINAL_RESULT_PATH!r}).write_text('secure-execution-complete', encoding='utf-8')\n"
            "print('secure-execution-complete')\n"
        )
        run_checked_command(
            log,
            sandbox,
            title="Local-Only Computation",
            command="python",
            args=["-c", local_code],
            expected_stdout="secure-execution-complete",
        )

        print_phase(log, "Phase 4: Verification and Recovery")
        verify_file(
            log,
            sandbox,
            path=FINAL_RESULT_PATH,
            expected_value="secure-execution-complete",
            title="Final State Verification",
        )
        log()
        log("Active Network Policy")
        log("---------------------")
        log("network : CLEAR_NETWORK_POLICY")
        sandbox.update(network=CLEAR_NETWORK_POLICY)
        probe_https(log, sandbox, PROJECT_HOST, expect_success=True)
        probe_https(log, sandbox, TOOL_HOST, expect_success=True)

        log()
        log("Phase-based secure tool access experiment completed successfully.")

    except Exception as exc:
        log()
        log(f"Experiment failed: {exc}")
        raise

    finally:
        if sandbox is not None:
            log()
            log("Terminating sandbox...")
            sandbox.terminate()
            log("Sandbox terminated.")
        logger.save()


if __name__ == "__main__":
    main()
