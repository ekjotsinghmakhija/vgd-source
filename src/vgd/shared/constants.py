import os
import sys
from pathlib import Path

_VGD_HOME_ENV = os.environ.get("VGD_HOME", None)


def _get_xdg_dir(env_var: str, fallback: str) -> Path:
    """Get XDG directory, prioritising VGD_HOME environment variable if its set. On non-Linux platforms, default to ~/.vgd."""

    if _VGD_HOME_ENV is not None:
        return Path.home() / _VGD_HOME_ENV

    if sys.platform != "linux":
        return Path.home() / ".vgd"

    xdg_value = os.environ.get(env_var, None)
    if xdg_value is not None:
        return Path(xdg_value) / "vgd"
    return Path.home() / fallback / "vgd"


VGD_CONFIG_HOME = _get_xdg_dir("XDG_CONFIG_HOME", ".config")
VGD_DATA_HOME = _get_xdg_dir("XDG_DATA_HOME", ".local/share")
VGD_CACHE_HOME = _get_xdg_dir("XDG_CACHE_HOME", ".cache")

# Models directory (data)
_VGD_MODELS_DIR_ENV = os.environ.get("VGD_MODELS_DIR", None)
VGD_MODELS_DIR = (
    VGD_DATA_HOME / "models"
    if _VGD_MODELS_DIR_ENV is None
    else Path.home() / _VGD_MODELS_DIR_ENV
)

# Log files (data/logs or cache)
VGD_LOG = VGD_CACHE_HOME / "vgd.log"
VGD_TEST_LOG = VGD_CACHE_HOME / "vgd_test.log"

# Identity (config)
VGD_NODE_ID_KEYPAIR = VGD_CONFIG_HOME / "node_id.keypair"
VGD_CONFIG_FILE = VGD_CONFIG_HOME / "config.toml"

# libp2p topics for event forwarding
LIBP2P_LOCAL_EVENTS_TOPIC = "worker_events"
LIBP2P_GLOBAL_EVENTS_TOPIC = "global_events"
LIBP2P_ELECTION_MESSAGES_TOPIC = "election_message"
LIBP2P_COMMANDS_TOPIC = "commands"

VGD_MAX_CHUNK_SIZE = 512 * 1024

VGD_IMAGE_CACHE_DIR = VGD_CACHE_HOME / "images"
