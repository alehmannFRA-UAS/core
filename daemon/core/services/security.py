"""
security.py: defines security services (vpnclient, vpnserver, ipsec and
firewall)
"""

import logging

from core import constants
from core.service import CoreService


class VPNClient(CoreService):
    name = "VPNClient"
    group = "Security"
    configs = ("vpnclient.sh",)
    startup = ("sh vpnclient.sh",)
    shutdown = ("killall openvpn",)
    validate = ("pidof openvpn",)
    custom_needed = True

    @classmethod
    def generate_config(cls, node, filename):
        """
        Return the client.conf and vpnclient.sh file contents to
        """
        cfg = "#!/bin/sh\n"
        cfg += "# custom VPN Client configuration for service (security.py)\n"
        fname = "%s/examples/services/sampleVPNClient" % constants.CORE_DATA_DIR

        try:
            cfg += open(fname, "rb").read()
        except IOError:
            logging.exception("Error opening VPN client configuration template (%s)", fname)

        return cfg


class VPNServer(CoreService):
    name = "VPNServer"
    group = "Security"
    configs = ("vpnserver.sh",)
    startup = ("sh vpnserver.sh",)
    shutdown = ("killall openvpn",)
    validate = ("pidof openvpn",)
    custom_needed = True

    @classmethod
    def generate_config(cls, node, filename):
        """
        Return the sample server.conf and vpnserver.sh file contents to
        GUI for user customization.
        """
        cfg = "#!/bin/sh\n"
        cfg += "# custom VPN Server Configuration for service (security.py)\n"
        fname = "%s/examples/services/sampleVPNServer" % constants.CORE_DATA_DIR

        try:
            cfg += open(fname, "rb").read()
        except IOError:
            logging.exception("Error opening VPN server configuration template (%s)", fname)

        return cfg


class IPsec(CoreService):
    name = "IPsec"
    group = "Security"
    configs = ("ipsec.sh",)
    startup = ("sh ipsec.sh",)
    shutdown = ("killall racoon",)
    custom_needed = True

    @classmethod
    def generate_config(cls, node, filename):
        """
        Return the ipsec.conf and racoon.conf file contents to
        GUI for user customization.
        """
        cfg = "#!/bin/sh\n"
        cfg += "# set up static tunnel mode security assocation for service "
        cfg += "(security.py)\n"
        fname = "%s/examples/services/sampleIPsec" % constants.CORE_DATA_DIR

        try:
            cfg += open(fname, "rb").read()
        except IOError:
            logging.exception("Error opening IPsec configuration template (%s)", fname)

        return cfg


class Firewall(CoreService):
    name = "Firewall"
    group = "Security"
    configs = ("firewall.sh",)
    startup = ("sh firewall.sh",)
    custom_needed = True

    @classmethod
    def generate_config(cls, node, filename):
        """
        Return the firewall rule examples to GUI for user customization.
        """
        cfg = "#!/bin/sh\n"
        cfg += "# custom node firewall rules for service (security.py)\n"
        fname = "%s/examples/services/sampleFirewall" % constants.CORE_DATA_DIR

        try:
            cfg += open(fname, "rb").read()
        except IOError:
            logging.exception("Error opening Firewall configuration template (%s)", fname)

        return cfg


class Nat(CoreService):
    """
    IPv4 source NAT service.
    """
    name = "NAT"
    executables = ("iptables",)
    group = "Security"
    configs = ("nat.sh", )
    startup = ("sh nat.sh",)
    custom_needed = False

    @classmethod
    def generateifcnatrule(cls, ifc, line_prefix=""):
        """
        Generate a NAT line for one interface.
        """
        cfg = line_prefix + "iptables -t nat -A POSTROUTING -o "
        cfg +=ifc.name + " -j MASQUERADE\n"

        cfg += line_prefix + "iptables -A FORWARD -i " + ifc.name
        cfg += " -m state --state RELATED,ESTABLISHED -j ACCEPT\n"

        cfg += line_prefix + "iptables -A FORWARD -i "
        cfg += ifc.name + " -j DROP\n"
        return cfg

    @classmethod
    def generate_config(cls, node, filename):
        """
        NAT out the first interface
        """
        cfg = "#!/bin/sh\n"
        cfg += "# generated by security.py\n"
        cfg += "# NAT out the first interface by default\n"
        have_nat = False
        for ifc in node.netifs():
            if hasattr(ifc, 'control') and ifc.control == True:
                continue
            if have_nat:
                cfg += cls.generateifcnatrule(ifc, line_prefix="#")
            else:
                have_nat = True
                cfg += "# NAT out the " + ifc.name + " interface\n"
                cfg += cls.generateifcnatrule(ifc)
                cfg += "\n"
        return cfg

