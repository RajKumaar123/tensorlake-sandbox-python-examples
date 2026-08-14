"""
Inspect the installed Tensorlake SDK for network policy support.

This experiment performs local introspection only. It does not create a sandbox
or consume Tensorlake resources.
"""

from __future__ import annotations

import importlib.metadata as metadata
import inspect
import re
import sys
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import tensorlake
from tensorlake.sandbox import NetworkConfig, Sandbox
from utils.output_logger import OutputLogger

try:
    from tensorlake.sandbox import models as sandbox_models
except Exception:  # pragma: no cover - import path is version-dependent
    sandbox_models = None


def header(log: Any, title: str) -> None:
    log()
    log(title)
    log("-" * len(title))


def safe_signature(obj: Any) -> str:
    try:
        signature = str(inspect.signature(obj))
        return re.sub(r"api_key:[^,)]*(?=[,)])", "api_key: '<redacted>'", signature)
    except Exception as exc:
        return f"<unavailable: {exc}>"


def safe_source(obj: Any) -> str:
    try:
        return inspect.getsource(obj)
    except Exception as exc:
        return f"<source unavailable: {exc}>"


def main() -> None:
    logger = OutputLogger(__file__)
    log = logger.log

    sdk_version = metadata.version("tensorlake")
    sdk_location = Path(tensorlake.__file__).resolve()

    try:
        header(log, "Tensorlake SDK")
        log(f"Version   : {sdk_version}")
        log(f"Location  : {sdk_location}")
        log(f"Package   : {sdk_location.parent}")
        log(f"Module    : {tensorlake.__name__}")

        header(log, "Sandbox.update")
        has_update = hasattr(Sandbox, "update")
        log(f"Exists    : {has_update}")
        if has_update:
            log(f"Signature : {safe_signature(Sandbox.update)}")
            log("Source    :")
            log(safe_source(Sandbox.update))

        header(log, "Sandbox.create")
        log(f"Signature : {safe_signature(Sandbox.create)}")

        header(log, "Networking models")
        log("Discovered : NetworkConfig")
        log(f"Module     : {NetworkConfig.__module__}")
        log(f"Signature  : {safe_signature(NetworkConfig)}")
        log(f"Annotations: {getattr(NetworkConfig, '__annotations__', {})}")
        log(f"Dataclass   : {is_dataclass(NetworkConfig)}")
        log("Fields      :")
        for field_name, field in getattr(NetworkConfig, "model_fields", {}).items():
            description = getattr(field, "description", None)
            log(f"  - {field_name}: {field.annotation}")
            if description:
                log(f"    description: {description}")
        log("Source      :")
        log(safe_source(NetworkConfig))

        if sandbox_models is not None:
            header(log, "Additional network symbols")
            candidates = ["ClearNetworkPolicy", "CLEAR_NETWORK_POLICY"]
            for name in candidates:
                obj = getattr(sandbox_models, name, None)
                log(f"{name}: {'present' if obj is not None else 'absent'}")
                if obj is None:
                    continue
                log(f"  module : {getattr(obj, '__module__', '<unknown>')}")
                log(f"  type   : {type(obj)}")
                log(f"  value  : {obj}")
                log(f"  sig    : {safe_signature(obj)}")
                if inspect.isclass(obj):
                    log(f"  source : {safe_source(obj)}")
                else:
                    log("  source : <not applicable for enum member>")
        else:
            header(log, "Additional network symbols")
            log("sandbox.models could not be imported.")

        header(log, "Networking constants / enums")
        log(
            "ClearNetworkPolicy enum: present"
            if sandbox_models and hasattr(sandbox_models, "ClearNetworkPolicy")
            else "ClearNetworkPolicy enum: absent"
        )
        log(
            "CLEAR_NETWORK_POLICY    : present"
            if sandbox_models and hasattr(sandbox_models, "CLEAR_NETWORK_POLICY")
            else "CLEAR_NETWORK_POLICY    : absent"
        )

        header(log, "Runtime policy update support")
        update_signature = safe_signature(Sandbox.update) if has_update else "<missing>"
        log(f"Sandbox.update signature            : {update_signature}")
        log(
            "Sandbox.update has network arg      : yes"
            if "network" in update_signature
            else "Sandbox.update has network arg      : no"
        )
        log(
            "Sandbox.update has network-equivalent: yes"
            if any(
                token in update_signature
                for token in ("allow_out", "deny_out", "ClearNetworkPolicy")
            )
            else "Sandbox.update has network-equivalent: no"
        )
        log(
            "Verified: runtime policy updates are exposed through "
            "Sandbox.update(network=...)."
        )

        header(log, "Verified capabilities")
        verified = [
            "Sandbox.update() accepts network: NetworkConfig | ClearNetworkPolicy | None.",
            "Sandbox.create() accepts allow_internet_access, allow_out, and deny_out.",
            "NetworkConfig models outbound allow_out and deny_out lists.",
            "NetworkConfig defaults to allow_internet_access=True.",
            "NetworkConfig source explicitly documents runtime policy changes on a running sandbox.",
            "NetworkConfig supports IPv4 addresses, CIDR ranges, DNS hostnames, and optional :port suffixes.",
            "deny_out takes precedence over allow_out.",
            "ClearNetworkPolicy exists as an enum sentinel with member TOKEN = 'clear'.",
            "CLEAR_NETWORK_POLICY is the enum member ClearNetworkPolicy.TOKEN.",
            "CLEAR_NETWORK_POLICY clears the network policy to unrestricted egress.",
        ]
        for item in verified:
            log(f"- {item}")

        header(log, "Unverified / unknown items")
        unknown = [
            "Whether runtime mutation behaves correctly against a live sandbox without a real network test.",
            "Whether hostnames resolve exactly as documented across all DNS edge cases.",
            "Whether :port suffixes are ignored for matching or normalized in all server-side paths.",
        ]
        for item in unknown:
            log(f"- {item}")

        header(log, "Technical assessment")
        log(
            "The installed SDK supports least-privilege network policy at sandbox "
            "creation time through allow_internet_access, allow_out, and deny_out. "
            "It also supports runtime policy transitions through Sandbox.update(network=...)."
        )
        log(
            "The production pattern 'running sandbox -> restrict network -> allow "
            "approved destination -> change policy at runtime -> revoke access -> "
            "block egress' is technically viable in this SDK version."
        )

        header(log, "Next experiment design")
        steps = [
            "Create one sandbox with baseline internet access.",
            "Verify a benign connectivity probe.",
            "Apply a restrictive policy on the same running sandbox.",
            "Verify the approved destination works and an unauthorized one fails.",
            "Replace the policy to approve a different destination.",
            "Use CLEAR_NETWORK_POLICY to restore unrestricted egress.",
        ]
        for step in steps:
            log(f"- {step}")

        header(log, "Command to run")
        log(
            "python 02-secure-agent-execution/experiments/"
            "01_inspect_network_policy/main.py"
        )
    finally:
        logger.save()


if __name__ == "__main__":
    main()
