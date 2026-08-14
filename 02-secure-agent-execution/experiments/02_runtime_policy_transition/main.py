"""
Demonstrate runtime network policy transitions on one Tensorlake sandbox.

This experiment uses the installed Tensorlake SDK directly to verify that a
single running sandbox can have its outbound policy changed without being
recreated.
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

SANDBOX_NAME = "tensorlake-secure-agent-network-policy-demo"
PRIMARY_HOST = "buildaisystem.com"
COMPARISON_HOST = "example.org"


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
    log("Network Policy")
    log("--------------")
    log(f"allow_internet_access : {allow_internet_access}")
    log(f"allow_out             : {', '.join(allow_out or []) or '<empty>'}")
    log(f"deny_out              : {', '.join(deny_out or []) or '<empty>'}")


def probe_python_https(
    log: Callable[[str], None],
    sandbox: Sandbox,
    hostname: str,
    expect_success: bool,
) -> None:
    """Run a short HTTPS probe inside the sandbox and assert the result."""
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
    http_status = "<none>"
    network_error = "<none>"
    reachable = False

    for line in output.splitlines():
        if line.startswith("REACHABLE "):
            reachable = True
            http_status = line.removeprefix("REACHABLE status=").strip()
        elif line.startswith("BLOCKED "):
            network_error = line.removeprefix("BLOCKED ").strip()

    expected_text = "reachable" if expect_success else "blocked"
    actual_text = "reachable" if reachable else "blocked"
    log()
    log("Connectivity Test")
    log("-----------------")
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


def apply_network_policy(
    log: Callable[[str], None],
    sandbox: Sandbox,
    *,
    allow_internet_access: bool,
    allow_out: list[str] | None = None,
    deny_out: list[str] | None = None,
) -> None:
    """Apply a runtime network policy to the running sandbox."""
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

    policy = NetworkConfig(**policy_kwargs)
    sandbox.update(network=policy)


def main() -> None:
    logger = OutputLogger(__file__)
    log = logger.log

    load_dotenv(REPOSITORY_ROOT / ".env")
    api_key = os.getenv("TENSORLAKE_API_KEY")
    if not api_key:
        raise ValueError("TENSORLAKE_API_KEY is missing. Add it to your .env file.")

    sandbox = None
    try:
        print_phase(log, "Phase 1: Baseline connectivity")
        sandbox = Sandbox.create(
            api_key=api_key,
            name=SANDBOX_NAME,
            allow_internet_access=True,
        )
        log(f"sandbox id  : {sandbox.sandbox_id}")
        log(f"sandbox name: {sandbox.name}")

        probe_python_https(log, sandbox, PRIMARY_HOST, expect_success=True)
        probe_python_https(log, sandbox, COMPARISON_HOST, expect_success=True)

        print_phase(log, "Phase 2: Restrict to approved host")
        apply_network_policy(
            log,
            sandbox,
            allow_internet_access=True,
            allow_out=[PRIMARY_HOST],
            deny_out=[],
        )
        probe_python_https(log, sandbox, PRIMARY_HOST, expect_success=True)
        probe_python_https(log, sandbox, COMPARISON_HOST, expect_success=False)

        print_phase(log, "Phase 3: Change approved host")
        apply_network_policy(
            log,
            sandbox,
            allow_internet_access=True,
            allow_out=[COMPARISON_HOST],
            deny_out=[],
        )
        probe_python_https(log, sandbox, COMPARISON_HOST, expect_success=True)
        probe_python_https(log, sandbox, PRIMARY_HOST, expect_success=False)

        print_phase(log, "Phase 4: Block all outbound access")
        apply_network_policy(
            log,
            sandbox,
            allow_internet_access=False,
        )
        probe_python_https(log, sandbox, PRIMARY_HOST, expect_success=False)
        probe_python_https(log, sandbox, COMPARISON_HOST, expect_success=False)

        print_phase(log, "Phase 5: Clear policy")
        log()
        log("Network Policy")
        log("--------------")
        log("network : CLEAR_NETWORK_POLICY")
        sandbox.update(network=CLEAR_NETWORK_POLICY)
        probe_python_https(log, sandbox, PRIMARY_HOST, expect_success=True)
        probe_python_https(log, sandbox, COMPARISON_HOST, expect_success=True)

        log()
        log("Runtime policy transition experiment completed successfully.")

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
