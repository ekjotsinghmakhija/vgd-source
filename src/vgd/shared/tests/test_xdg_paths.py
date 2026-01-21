"""Tests for XDG Base Directory Specification compliance."""

import os
import sys
from pathlib import Path
from unittest import mock


def test_xdg_paths_on_linux():
    """Test that XDG paths are used on Linux when XDG env vars are set."""
    with (
        mock.patch.dict(
            os.environ,
            {
                "XDG_CONFIG_HOME": "/tmp/test-config",
                "XDG_DATA_HOME": "/tmp/test-data",
                "XDG_CACHE_HOME": "/tmp/test-cache",
            },
            clear=False,
        ),
        mock.patch.object(sys, "platform", "linux"),
    ):
        # Re-import to pick up mocked values
        import importlib

        import vgd.shared.constants as constants

        importlib.reload(constants)

        assert Path("/tmp/test-config/vgd") == constants.VGD_CONFIG_HOME
        assert Path("/tmp/test-data/vgd") == constants.VGD_DATA_HOME
        assert Path("/tmp/test-cache/vgd") == constants.VGD_CACHE_HOME


def test_xdg_default_paths_on_linux():
    """Test that XDG default paths are used on Linux when env vars are not set."""
    # Remove XDG env vars and VGD_HOME
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("XDG_") and k != "VGD_HOME"
    }
    with (
        mock.patch.dict(os.environ, env, clear=True),
        mock.patch.object(sys, "platform", "linux"),
    ):
        import importlib

        import vgd.shared.constants as constants

        importlib.reload(constants)

        home = Path.home()
        assert home / ".config" / "vgd" == constants.VGD_CONFIG_HOME
        assert home / ".local/share" / "vgd" == constants.VGD_DATA_HOME
        assert home / ".cache" / "vgd" == constants.VGD_CACHE_HOME


def test_legacy_vgd_home_takes_precedence():
    """Test that VGD_HOME environment variable takes precedence for backward compatibility."""
    with mock.patch.dict(
        os.environ,
        {
            "VGD_HOME": ".custom-vgd",
            "XDG_CONFIG_HOME": "/tmp/test-config",
        },
        clear=False,
    ):
        import importlib

        import vgd.shared.constants as constants

        importlib.reload(constants)

        home = Path.home()
        assert home / ".custom-vgd" == constants.VGD_CONFIG_HOME
        assert home / ".custom-vgd" == constants.VGD_DATA_HOME


def test_macos_uses_traditional_paths():
    """Test that macOS uses traditional ~/.vgd directory."""
    # Remove VGD_HOME to ensure we test the default behavior
    env = {k: v for k, v in os.environ.items() if k != "VGD_HOME"}
    with (
        mock.patch.dict(os.environ, env, clear=True),
        mock.patch.object(sys, "platform", "darwin"),
    ):
        import importlib

        import vgd.shared.constants as constants

        importlib.reload(constants)

        home = Path.home()
        assert home / ".vgd" == constants.VGD_CONFIG_HOME
        assert home / ".vgd" == constants.VGD_DATA_HOME
        assert home / ".vgd" == constants.VGD_CACHE_HOME


def test_node_id_in_config_dir():
    """Test that node ID keypair is in the config directory."""
    import vgd.shared.constants as constants

    assert constants.VGD_NODE_ID_KEYPAIR.parent == constants.VGD_CONFIG_HOME


def test_models_in_data_dir():
    """Test that models directory is in the data directory."""
    # Clear VGD_MODELS_DIR to test default behavior
    env = {k: v for k, v in os.environ.items() if k != "VGD_MODELS_DIR"}
    with mock.patch.dict(os.environ, env, clear=True):
        import importlib

        import vgd.shared.constants as constants

        importlib.reload(constants)

        assert constants.VGD_MODELS_DIR.parent == constants.VGD_DATA_HOME
