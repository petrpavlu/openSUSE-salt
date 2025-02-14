import logging
import os

# Import Salt libs
import salt.utils.json
import salt.utils.path
import salt.utils.stringutils
import salt.modules.cmdmod
from salt.exceptions import CommandExecutionError

__virtualname__ = "ansible"

log = logging.getLogger(__name__)


def __virtual__():  # pylint: disable=expected-2-blank-lines-found-0
    if salt.utils.path.which("ansible-inventory"):
        return __virtualname__
    return (False, "Install `ansible` to use inventory")


def targets(inventory="/etc/ansible/hosts", **kwargs):
    """
    Return the targets from the ansible inventory_file
    Default: /etc/salt/roster
    """
    if not os.path.isfile(inventory):
        raise CommandExecutionError("Inventory file not found: {}".format(inventory))

    extra_cmd = []
    if "export" in kwargs:
        extra_cmd.append("--export")
    if "yaml" in kwargs:
        extra_cmd.append("--yaml")
    inv = salt.modules.cmdmod.run(
        "ansible-inventory -i {} --list {}".format(inventory, " ".join(extra_cmd))
    )
    if kwargs.get("yaml", False):
        return salt.utils.stringutils.to_str(inv)
    else:
        return salt.utils.json.loads(salt.utils.stringutils.to_str(inv))
