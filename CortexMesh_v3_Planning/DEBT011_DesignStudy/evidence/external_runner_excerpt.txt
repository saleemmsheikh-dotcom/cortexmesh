import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
from importlib import util
from pathlib import Path


class ExternalRunner:
    """
    OS-level isolation for untrusted capabilities.
    Executes capabilities in Docker containers with no host access.
    """

    DEFAULT_IMAGE = "cortexmesh-capability"
    IMAGE_PREFIX = "cortexmesh-capability"
    TIMEOUT_SECONDS = 30
    PROJECT_ROOT = Path(__file__).resolve().parents[1]

    @classmethod
    def execute(cls, capability_module, capability_request, memory_context=None):
        """
        Execute capability in an isolated container.

        Args:
            capability_module: str, e.g. "capabilities.malicious_probe"
            capability_request: dict with "task", "input", etc.
            memory_context: dict serialized into the request envelope

        Returns:
            dict with "status", "output", "audit_trail"
        """
        request = dict(capability_request or {})
        request.setdefault("capability_module", capability_module)

        if memory_context is not None:
            request["memory_context"] = memory_context

        request_json = json.dumps(request)
        container_name = f"cortexmesh-{os.urandom(4).hex()}"

        try:
            image = cls._get_capability_image(capability_module)
            proc = subprocess.Popen(
                [
                    "docker",
                    "run",
                    "--name",
                    container_name,
                    "-i",
                    "--rm",
                    "--network=none",
                    "--read-only",
                    "--memory=256m",
                    "--cpus=0.5",
                    "-e",
                    "PYTHONDONTWRITEBYTECODE=1",
                    "-e",
                    f"CORTEXMESH_REQUEST={request_json}",
                    image,
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            killed_by_timer = threading.Event()

            def kill_container():
                killed_by_timer.set()
                subprocess.run(
                    ["docker", "kill", container_name],
                    capture_output=True,
                    timeout=10,
                )
                proc.kill()

            timer = threading.Timer(cls.TIMEOUT_SECONDS, kill_container)
            timer.start()

            try:
                stdout, stderr = proc.communicate(input=request_json)
                timer.cancel()

                if killed_by_timer.is_set():
                    return {
                        "status": "timeout",
                        "output": None,
                        "error": "Capability exceeded time limit",
                        "audit_trail": {
                            "isolated": True,
                            "image": image,
                            "killed": True,
                        },
                    }
            except Exception:
                timer.cancel()
                kill_container()
                return {
                    "status": "timeout",
                    "output": None,
                    "error": "Capability exceeded time limit",
                    "audit_trail": {
                        "isolated": True,
                        "image": image,
                        "killed": True,
                    },
                }

            if proc.returncode != 0:
                return {
                    "status": "error",
                    "output": None,
                    "error": _sanitize_error(stderr),
                    "audit_trail": {
                        "isolated": True,
                        "image": image,
                        "container_exited": proc.returncode,
                    },
                }

            result = json.loads(stdout)
            result["audit_trail"] = {
                "isolated": True,
                "image": image,
                "container_exited": 0,
                "stderr": _sanitize_error(stderr),
            }
            return result

        except json.JSONDecodeError as exc:
            return {
                "status": "error",
                "output": None,
                "error": _sanitize_error(f"Invalid JSON from capability: {exc}"),
                "audit_trail": {"isolated": True},
            }
        except Exception as exc:
            return {
                "status": "error",
                "output": None,
                "error": _sanitize_error(str(exc)),
                "audit_trail": {"isolated": True},
            }

    @classmethod
    def _get_capability_image(cls, capability_module):
        source_path = cls._module_source_path(capability_module)

        if source_path is None:
            return cls.DEFAULT_IMAGE

        digest = cls._source_digest(source_path)
        image = f"{cls.IMAGE_PREFIX}-{cls._safe_name(capability_module)}:{digest[:12]}"

        if cls._image_exists(image):
            return image

        cls._build_capability_image(image, source_path)
        return image

    @classmethod
    def _module_source_path(cls, capability_module):
        if not capability_module or capability_module == "__main__":
            return None

        spec = util.find_spec(capability_module)
        if spec is None or spec.origin is None:
            return None

        source_path = Path(spec.origin).resolve()
        if source_path.suffix != ".py":
            return None

        try:
            source_path.relative_to(cls.PROJECT_ROOT)
        except ValueError:
            return None

        return source_path

    @staticmethod
    def _source_digest(source_path):
        payload = source_path.read_bytes()
        return hashlib.sha256(payload).hexdigest()

    @staticmethod
    def _safe_name(capability_module):
        return "".join(
            char if char.isalnum() else "-"
            for char in capability_module.lower()
        ).strip("-")

    @staticmethod
    def _image_exists(image):
        proc = subprocess.run(
            ["docker", "image", "inspect", image],
            capture_output=True,
            text=True,
        )
        return proc.returncode == 0

    @classmethod
    def _build_capability_image(cls, image, source_path):
        with tempfile.TemporaryDirectory(prefix="cortexmesh-capability-") as directory:
            context = Path(directory)
            shutil.copy2(source_path, context / "capability_payload.py")
            (context / "Dockerfile").write_text(
                "\n".join([
                    f"FROM {cls.DEFAULT_IMAGE}",
                    "WORKDIR /app",
                    "COPY capability_payload.py /app/capability_payload.py",
                    'ENV CORTEXMESH_CAPABILITY_MODULE="capability_payload"',
                    "",
                ])
            )
            proc = subprocess.run(
                ["docker", "build", "-t", image, str(context)],
                capture_output=True,
                text=True,
                timeout=cls.TIMEOUT_SECONDS,
            )

            if proc.returncode != 0:
                raise RuntimeError(
                    "Failed to build capability image "
                    f"{image}: {proc.stderr}"
                )


def _sanitize_error(error_str):
    """Remove host paths from error messages."""
    if not error_str:
        return None

    sanitized = re.sub(r"/Users/[^/\s]+/[^\s]+", "<HOST_PATH>", error_str)
    sanitized = re.sub(r"/home/[^/\s]+/[^\s]+", "<HOST_PATH>", sanitized)
    return sanitized
