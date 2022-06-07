"""
Simple example custom service, used to drive shell commands on a node.
"""
from typing import Tuple
from core.nodes.base import CoreNode
from core.services.coreservices import CoreService, ServiceMode

GROUP_NAME = "4G"

"""
    Example Custom CORE Service

    :cvar name: name used as a unique ID for this service and is required, no spaces
    :cvar group: allows you to group services within the GUI under a common name
    :cvar executables: executables this service depends on to function, if executable is
        not on the path, service will not be loaded
    :cvar dependencies: services that this service depends on for startup, tuple of
        service names
    :cvar dirs: directories that this service will create within a node
    :cvar configs: files that this service will generate, without a full path this file
        goes in the node's directory e.g. /tmp/pycore.12345/n1.conf/myfile
    :cvar startup: commands used to start this service, any non-zero exit code will
        cause a failure
    :cvar validate: commands used to validate that a service was started, any non-zero
        exit code will cause a failure
    :cvar validation_mode: validation mode, used to determine startup success.
        NON_BLOCKING    - runs startup commands, and validates success with validation commands
        BLOCKING        - runs startup commands, and validates success with the startup commands themselves
        TIMER           - runs startup commands, and validates success by waiting for "validation_timer" alone
    :cvar validation_timer: time in seconds for a service to wait for validation, before
        determining success in TIMER/NON_BLOCKING modes.
    :cvar validation_period: period in seconds to wait before retrying validation,
        only used in NON_BLOCKING mode
    :cvar shutdown: shutdown commands to stop this service
"""


class HSSService(CoreService):

    name: str = "HSS"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-hssd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ('/etc/open5gs', '/var/log/open5gs',)
    configs: Tuple[str, ...] = ('/etc/open5gs/hss.yaml',)
    startup: Tuple[str, ...] = ("open5gs-hssd",)
    validate: Tuple[str, ...] = ()
    validation_mode: ServiceMode = ServiceMode.NON_BLOCKING
    validation_timer: int = 5
    validation_period: float = 0.5
    shutdown: Tuple[str, ...] = ()

    @classmethod
    def on_load(cls) -> None:
        """
        Provides a way to run some arbitrary logic when the service is loaded, possibly
        to help facilitate dynamic settings for the environment.

        :return: nothing
        """
        pass

    @classmethod
    def get_configs(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the config files from the node a service
        will run. Defaults to the class definition and can be left out entirely if not
        needed.

        :param node: core node that the service is being ran on
        :return: tuple of config files to create
        """
        return cls.configs

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = """db_uri: mongodb://localhost/open5gs

#
# logger:
#
#  o Set OGS_LOG_INFO to all domain level
#   - If `level` is omitted, the default level is OGS_LOG_INFO)
#   - If `domain` is omitted, the all domain level is set from 'level'
#    (Nothing is needed)
#
#  o Set OGS_LOG_ERROR to all domain level
#   - `level` can be set with none, fatal, error, warn, info, debug, trace
#    level: error
#
#  o Set OGS_LOG_DEBUG to mme/emm domain level
#    level: debug
#    domain: mme,emm
#
#  o Set OGS_LOG_TRACE to all domain level
#    level: trace
#    domain: core,fd,hss,event,mem,sock
#
logger:
    file: /var/log/open5gs/hss.log

hss:
    freeDiameter: /etc/freeDiameter/hss.conf

#    sms_over_ims: "sip:smsc.mnc001.mcc001.3gppnetwork.org:7060;transport=tcp"

#
# parameter:
#
#  o Disable use of IPv4 addresses (only IPv6)
#      no_ipv4: true
#
#  o Disable use of IPv6 addresses (only IPv4)
#      no_ipv6: true
#
#  o Prefer IPv4 instead of IPv6 for estabishing new GTP connections.
#      prefer_ipv4: true
#
parameter:

#
# max:
#
# o Maximum Number of UE per AMF/MME
#    ue: 1024
# o Maximum Number of gNB/eNB per AMF/MME
#    gnb: 64
#
max:
"""

        return cfg

    @classmethod
    def get_startup(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the startup commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of startup commands to run
        """
        return cls.startup

    @classmethod
    def get_validate(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the validate commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of commands to validate service startup with
        """
        return cls.validate

class MMEService(CoreService):

    name: str = "MME"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-mmed",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ('/etc/open5gs', '/var/log/open5gs',)
    configs: Tuple[str, ...] = ('/etc/open5gs/mme.yaml',)
    startup: Tuple[str, ...] = ("open5gs-mmed",)
    validate: Tuple[str, ...] = ()
    validation_mode: ServiceMode = ServiceMode.NON_BLOCKING
    validation_timer: int = 5
    validation_period: float = 0.5
    shutdown: Tuple[str, ...] = ()

    @classmethod
    def on_load(cls) -> None:
        """
        Provides a way to run some arbitrary logic when the service is loaded, possibly
        to help facilitate dynamic settings for the environment.

        :return: nothing
        """
        pass

    @classmethod
    def get_configs(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the config files from the node a service
        will run. Defaults to the class definition and can be left out entirely if not
        needed.

        :param node: core node that the service is being ran on
        :return: tuple of config files to create
        """
        return cls.configs

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = """db_uri: mongodb://localhost/open5gs

#
# logger:
#
#  o Set OGS_LOG_INFO to all domain level
#   - If `level` is omitted, the default level is OGS_LOG_INFO)
#   - If `domain` is omitted, the all domain level is set from 'level'
#    (Nothing is needed)
#
#  o Set OGS_LOG_ERROR to all domain level
#   - `level` can be set with none, fatal, error, warn, info, debug, trace
#    level: error
#
#  o Set OGS_LOG_DEBUG to mme/emm domain level
#    level: debug
#    domain: mme,emm
#
#  o Set OGS_LOG_TRACE to all domain level
#    level: trace
#    domain: core,fd,hss,event,mem,sock
#
logger:
    file: /var/log/open5gs/hss.log

hss:
    freeDiameter: /etc/freeDiameter/hss.conf

#    sms_over_ims: "sip:smsc.mnc001.mcc001.3gppnetwork.org:7060;transport=tcp"

#
# parameter:
#
#  o Disable use of IPv4 addresses (only IPv6)
#      no_ipv4: true
#
#  o Disable use of IPv6 addresses (only IPv4)
#      no_ipv6: true
#
#  o Prefer IPv4 instead of IPv6 for estabishing new GTP connections.
#      prefer_ipv4: true
#
parameter:

#
# max:
#
# o Maximum Number of UE per AMF/MME
#    ue: 1024
# o Maximum Number of gNB/eNB per AMF/MME
#    gnb: 64
#
max:
"""

        return cfg

    @classmethod
    def get_startup(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the startup commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of startup commands to run
        """
        return cls.startup

    @classmethod
    def get_validate(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the validate commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of commands to validate service startup with
        """
        return cls.validate

class PCRFService(CoreService):

    name: str = "PCRF"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-pcrfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs",)
    configs: Tuple[str, ...] = ("/etc/open5gs/pcrf.yaml",)
    startup: Tuple[str, ...] = ("open5gs-pcrfd",)
    validate: Tuple[str, ...] = ()
    validation_mode: ServiceMode = ServiceMode.NON_BLOCKING
    validation_timer: int = 5
    validation_period: float = 0.5
    shutdown: Tuple[str, ...] = ()

    @classmethod
    def on_load(cls) -> None:
        """
        Provides a way to run some arbitrary logic when the service is loaded, possibly
        to help facilitate dynamic settings for the environment.

        :return: nothing
        """
        pass

    @classmethod
    def get_configs(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the config files from the node a service
        will run. Defaults to the class definition and can be left out entirely if not
        needed.

        :param node: core node that the service is being ran on
        :return: tuple of config files to create
        """
        return cls.configs

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = """db_uri: mongodb://localhost/open5gs

#
# logger:
#
#  o Set OGS_LOG_INFO to all domain level
#   - If `level` is omitted, the default level is OGS_LOG_INFO)
#   - If `domain` is omitted, the all domain level is set from 'level'
#    (Nothing is needed)
#
#  o Set OGS_LOG_ERROR to all domain level
#   - `level` can be set with none, fatal, error, warn, info, debug, trace
#    level: error
#
#  o Set OGS_LOG_DEBUG to mme/emm domain level
#    level: debug
#    domain: mme,emm
#
#  o Set OGS_LOG_TRACE to all domain level
#    level: trace
#    domain: core,fd,pcrf,event,mem,sock
logger:
    file: /var/log/open5gs/pcrf.log

pcrf:
    freeDiameter: /etc/freeDiameter/pcrf.conf

#
# parameter:
#
#  o Disable use of IPv4 addresses (only IPv6)
#      no_ipv4: true
#
#  o Disable use of IPv6 addresses (only IPv4)
#      no_ipv6: true
#
#  o Prefer IPv4 instead of IPv6 for estabishing new GTP connections.
#      prefer_ipv4: true
#
parameter:

#
# max:
#
# o Maximum Number of UE per AMF/MME
#    ue: 1024
# o Maximum Number of gNB/eNB per AMF/MME
#    gnb: 64
#
max:
"""

        return cfg

    @classmethod
    def get_startup(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the startup commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of startup commands to run
        """
        return cls.startup

    @classmethod
    def get_validate(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the validate commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of commands to validate service startup with
        """
        return cls.validate

class SGWCService(CoreService):

    name: str = "SGWC"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-sgwcd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs",)
    configs: Tuple[str, ...] = ("/etc/open5gs/sgwc.yaml",)
    startup: Tuple[str, ...] = ("open5gs-sgwcd",)
    validate: Tuple[str, ...] = ()
    validation_mode: ServiceMode = ServiceMode.NON_BLOCKING
    validation_timer: int = 5
    validation_period: float = 0.5
    shutdown: Tuple[str, ...] = ()

    @classmethod
    def on_load(cls) -> None:
        """
        Provides a way to run some arbitrary logic when the service is loaded, possibly
        to help facilitate dynamic settings for the environment.

        :return: nothing
        """
        pass

    @classmethod
    def get_configs(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the config files from the node a service
        will run. Defaults to the class definition and can be left out entirely if not
        needed.

        :param node: core node that the service is being ran on
        :return: tuple of config files to create
        """
        return cls.configs

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = """#
# logger:
#
#  o Set OGS_LOG_INFO to all domain level
#   - If `level` is omitted, the default level is OGS_LOG_INFO)
#   - If `domain` is omitted, the all domain level is set from 'level'
#    (Nothing is needed)
#
#  o Set OGS_LOG_ERROR to all domain level
#   - `level` can be set with none, fatal, error, warn, info, debug, trace
#    level: error
#
#  o Set OGS_LOG_DEBUG to mme/emm domain level
#    level: debug
#    domain: mme,emm
#
#  o Set OGS_LOG_TRACE to all domain level
#    level: trace
#    domain: core,pfcp,gtp,sgwc,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/sgwc.log

#
# sgwc:
#
#  <GTP-C Server>
#
#  o GTP-C Server(127.0.0.3:2123, [fd69:f21d:873c:fa::2]:2123)
#    gtpc:
#      addr:
#        - 127.0.0.3
#        - fd69:f21d:873c:fa::2
#
#  o On SGW, Same Configuration(127.0.0.3:2123,
#  [fd69:f21d:873c:fa::2]:2123) as below.
#    gtpc:
#      - addr: 127.0.0.3
#      - addr: fd69:f21d:873c:fa::2
#
#  o GTP-C Option (Default)
#    - so_bindtodevice : NULL
#
#    gtpc:
#      addr: 127.0.0.3
#      option:
#        so_bindtodevice: vrf-blue
#
#  <PFCP Server>
#
#  o PFCP Server(127.0.0.3:8805, ::1:8805)
#    pfcp:
#      - addr: 127.0.0.3
#      - addr: ::1
#
#  o PFCP-U Server(127.0.0.1:2152, [::1]:2152)
#    pfcp:
#      name: localhost
#
#  o PFCP Option (Default)
#    - so_bindtodevice : NULL
#
#    pfcp:
#      addr: 127.0.0.3
#      option:
#        so_bindtodevice: vrf-blue
#
sgwc:
    gtpc:
      - addr: 127.0.0.3
    pfcp:
      - addr: 127.0.0.3

#
# sgwu:
#
#  <PFCP Client>>
#
#  o PFCP Client(127.0.0.6:8805)
#
#    pfcp:
#      addr: 127.0.0.6
#
#  <SGWU_SELECTION_MODE - EPC only>
#
#  sgwu:
#    pfcp:
#      - addr: 127.0.0.6
#      - addr: 127.0.0.12
#      - addr: 127.0.0.18
#
# o SGWU selection by eNodeB TAC
#   (either single TAC or multiple TACs, DECIMAL representation)
#
#  sgwu:
#    pfcp:
#      - addr: 127.0.0.6
#        tac: 1
#      - addr: 127.0.0.12
#        tac: [3,5,8]
#
# o SGWU selection by UE's APN (either single APN or multiple APNs)
#
#  sgwu:
#    pfcp:
#      - addr: 127.0.0.6
#        apn: ims
#      - addr: 127.0.0.12
#        apn: [internet, web]
#
# o SGWU selection by CellID(e_cell_id: 28bit)
#   (either single e_cell_id or multiple e_cell_id, HEX representation)
#
#  sgwu:
#    pfcp:
#      - addr: 127.0.0.6
#        e_cell_id: 463
#      - addr: 127.0.0.12
#        e_cell_id: [123456789, 9413]
#
sgwu:
    pfcp:
      - addr: 127.0.0.6

#
# parameter:
#
#  o Disable use of IPv4 addresses (only IPv6)
#      no_ipv4: true
#
#  o Disable use of IPv6 addresses (only IPv4)
#      no_ipv6: true
#
#  o Prefer IPv4 instead of IPv6 for estabishing new GTP connections.
#      prefer_ipv4: true
#
#  o Disable selection of SGW-U PFCP in Round-Robin manner
#      no_pfcp_rr_select: true
#
parameter:

#
# max:
#
# o Maximum Number of UE per AMF/MME
#    ue: 1024
# o Maximum Number of gNB/eNB per AMF/MME
#    gnb: 64
#
max:

#
# time:
#
#  o Message Wait Duration (Default : 10,000 ms = 10 seconds)
#
#  o Message Wait Duration (3000 ms)
#    message:
#        duration: 3000
time:
"""

        return cfg

    @classmethod
    def get_startup(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the startup commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of startup commands to run
        """
        return cls.startup

    @classmethod
    def get_validate(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the validate commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of commands to validate service startup with
        """
        return cls.validate

class SGWUService(CoreService):

    name: str = "SGWU"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-sgwud",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs",)
    configs: Tuple[str, ...] = ("/etc/open5gs/sgwu.yaml",)
    startup: Tuple[str, ...] = ("open5gs-sgwud",)
    validate: Tuple[str, ...] = ()
    validation_mode: ServiceMode = ServiceMode.NON_BLOCKING
    validation_timer: int = 5
    validation_period: float = 0.5
    shutdown: Tuple[str, ...] = ()

    @classmethod
    def on_load(cls) -> None:
        """
        Provides a way to run some arbitrary logic when the service is loaded, possibly
        to help facilitate dynamic settings for the environment.

        :return: nothing
        """
        pass

    @classmethod
    def get_configs(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the config files from the node a service
        will run. Defaults to the class definition and can be left out entirely if not
        needed.

        :param node: core node that the service is being ran on
        :return: tuple of config files to create
        """
        return cls.configs

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = """#
# logger:
#
#  o Set OGS_LOG_INFO to all domain level
#   - If `level` is omitted, the default level is OGS_LOG_INFO)
#   - If `domain` is omitted, the all domain level is set from 'level'
#    (Nothing is needed)
#
#  o Set OGS_LOG_ERROR to all domain level
#   - `level` can be set with none, fatal, error, warn, info, debug, trace
#    level: error
#
#  o Set OGS_LOG_DEBUG to mme/emm domain level
#    level: debug
#    domain: mme,emm
#
#  o Set OGS_LOG_TRACE to all domain level
#    level: trace
#    domain: core,pfcp,gtp,sgwu,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/sgwu.log

#
# sgwu:
#
#  <PFCP Server>
#
#  o PFCP Server(127.0.0.6:8805, ::1:8805)
#    pfcp:
#      - addr: 127.0.0.6
#      - addr: ::1
#
#  o PFCP-U Server(127.0.0.1:2152, [::1]:2152)
#    pfcp:
#      - name: localhost
#
#  o PFCP Option (Default)
#    - so_bindtodevice : NULL
#
#    pfcp:
#      addr: 127.0.0.6
#      option:
#        so_bindtodevice: vrf-blue
#
#  <GTP-U Server>
#
#  o GTP-U Server(127.0.0.6:2152, [::1]:2152)
#    gtpu:
#      - addr: 127.0.0.6
#      - addr: ::1
#
#  o GTP-U Server(127.0.0.1:2152, [::1]:2152)
#    gtpu:
#      - name: localhost
#
#  o User Plane IP Resource information
#    gtpu:
#      - addr:
#        - 127.0.0.6
#        - ::1
#        teid_range_indication: 4
#        teid_range: 10
#        network_instance: internet
#        source_interface: 0
#      - addr: 127.0.10.4
#        teid_range_indication: 4
#        teid_range: 5
#        network_instance: ims
#        source_interface: 1
#
#  o Provide custom SGW-U GTP-U address to be advertised inside S1AP messages
#    gtpu:
#      - addr: 10.4.128.21
#        advertise: 172.24.15.30
#
#    gtpu:
#      - addr: 10.4.128.21
#        advertise:
#        - 127.0.0.1
#        - ::1
#
#    gtpu:
#      - addr: 10.4.128.21
#        advertise: sgw1.epc.mnc001.mcc001.3gppnetwork.org
#
#    gtpu:
#      - dev: ens3
#        advertise: sgw1.epc.mnc001.mcc001.3gppnetwork.org
#
#  o GTP-U Option (Default)
#    - so_bindtodevice : NULL
#
#    gtpu:
#      addr: 127.0.0.6
#      option:
#        so_bindtodevice: vrf-blue
#
sgwu:
    pfcp:
      - addr: 127.0.0.6
    gtpu:
      - addr: 127.0.0.6

#
# sgwc:
#
#  <PFCP Client>>
#
#  o PFCP Client(127.0.0.3:8805)
#
#    pfcp:
#      addr: 127.0.0.3
#
sgwc:

#
# parameter:
#
#  o Disable use of IPv4 addresses (only IPv6)
#      no_ipv4: true
#
#  o Disable use of IPv6 addresses (only IPv4)
#      no_ipv6: true
#
#  o Prefer IPv4 instead of IPv6 for estabishing new GTP connections.
#      prefer_ipv4: true
#
parameter:

#
# max:
#
# o Maximum Number of UE per AMF/MME
#    ue: 1024
# o Maximum Number of gNB/eNB per AMF/MME
#    gnb: 64
#
max:

#
# time:
#
#  o Message Wait Duration (Default : 10,000 ms = 10 seconds)
#
#  o Message Wait Duration (3000 ms)
#    message:
#        duration: 3000
time:
"""

        return cfg

    @classmethod
    def get_startup(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the startup commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of startup commands to run
        """
        return cls.startup

    @classmethod
    def get_validate(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the validate commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of commands to validate service startup with
        """
        return cls.validate

class PGWCService(CoreService):

    name: str = "PGWC"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-smfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs",)
    configs: Tuple[str, ...] = ("/etc/open5gs/smf.yaml",)
    startup: Tuple[str, ...] = ("open5gs-smfd",)
    validate: Tuple[str, ...] = ()
    validation_mode: ServiceMode = ServiceMode.NON_BLOCKING
    validation_timer: int = 5
    validation_period: float = 0.5
    shutdown: Tuple[str, ...] = ()

    @classmethod
    def on_load(cls) -> None:
        """
        Provides a way to run some arbitrary logic when the service is loaded, possibly
        to help facilitate dynamic settings for the environment.

        :return: nothing
        """
        pass

    @classmethod
    def get_configs(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the config files from the node a service
        will run. Defaults to the class definition and can be left out entirely if not
        needed.

        :param node: core node that the service is being ran on
        :return: tuple of config files to create
        """
        return cls.configs

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = """#
# logger:
#
#  o Set OGS_LOG_INFO to all domain level
#   - If `level` is omitted, the default level is OGS_LOG_INFO)
#   - If `domain` is omitted, the all domain level is set from 'level'
#    (Nothing is needed)
#
#  o Set OGS_LOG_ERROR to all domain level
#   - `level` can be set with none, fatal, error, warn, info, debug, trace
#    level: error
#
#  o Set OGS_LOG_DEBUG to mme/emm domain level
#    level: debug
#    domain: mme,emm
#
#  o Set OGS_LOG_TRACE to all domain level
#    level: trace
#    domain: core,pfcp,fd,pfcp,gtp,smf,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/smf.log
#
# smf:
#
#  <SBI Server>
#
#  o SBI Server(http://<all address available>:80)
#    sbi:
#
#  o SBI Server(http://<any address>:80)
#    sbi:
#      - addr:
#          - 0.0.0.0
#          - ::0
#        port: 7777
#
#  o SBI Server(https://<all address avaiable>:443)
#    sbi:
#      - tls:
#          key: smf.key
#          pem: smf.pem
#
#  o SBI Server(https://127.0.0.4:443, http://[::1]:80)
#    sbi:
#      - addr: 127.0.0.4
#        tls:
#          key: smf.key
#          pem: smf.pem
#      - addr: ::1
#
#  o SBI Server(http://smf.open5gs.org:80)
#    sbi:
#      - name: smf.open5gs.org
#
#  o SBI Server(http://127.0.0.4:7777)
#    sbi:
#      - addr: 127.0.0.4
#        port: 7777
#
#  o SBI Server(http://<eth0 IP address>:80)
#    sbi:
#      - dev: eth0
#
#  o Provide custom SBI address to be advertised to NRF
#    sbi:
#      - dev: eth0
#        advertise: open5gs-smf.svc.local
#
#    sbi:
#      - addr: localhost
#        advertise:
#          - 127.0.0.99
#          - ::1
#
#  o SBI Option (Default)
#    - tcp_nodelay : true
#    - so_linger.l_onoff : false
#
#    sbi:
#      addr: 127.0.0.4
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
#  <PFCP Server>
#
#  o PFCP Server(127.0.0.4:8805, ::1:8805)
#    pfcp:
#      - addr: 127.0.0.4
#      - addr: ::1
#
#  o PFCP-U Server(127.0.0.1:2152, [::1]:2152)
#    pfcp:
#      name: localhost
#
#  o PFCP Option (Default)
#    - so_bindtodevice : NULL
#
#    pfcp:
#      addr: 127.0.0.4
#      option:
#        so_bindtodevice: vrf-blue
#
#  <GTP-C Server>
#
#  o GTP-C Server(127.0.0.4:2123, [fd69:f21d:873c:fa::3]:2123)
#    gtpc:
#      addr:
#        - 127.0.0.4
#        - fd69:f21d:873c:fa::3
#
#  o On SMF, Same configuration
#    (127.0.0.4:2123, [fd69:f21d:873c:fa::3]:2123).
#    gtpc:
#      - addr: 127.0.0.4
#      - addr: fd69:f21d:873c:fa::3
#
#  o GTP-C Option (Default)
#    - so_bindtodevice : NULL
#
#    gtpc:
#      addr: 127.0.0.4
#      option:
#        so_bindtodevice: vrf-blue
#
#  <GTP-U Server>>
#
#  o GTP-U Server(127.0.0.4:2152, [::1]:2152)
#    gtpu:
#      - addr: 127.0.0.4
#      - addr: ::1
#
#  o GTP-U Server(127.0.0.1:2152, [::1]:2152)
#    gtpu:
#      name: localhost
#
#  o GTP-U Option (Default)
#    - so_bindtodevice : NULL
#
#    gtpu:
#      addr: 127.0.0.4
#      option:
#        so_bindtodevice: vrf-blue
#
#  <Subnet for UE Pool>
#
#  o IPv4 Pool
#    subnet:
#      addr: 10.45.0.1/16
#
#  o IPv4/IPv6 Pool
#    subnet:
#      - addr: 10.45.0.1/16
#      - addr: 2001:db8:cafe::1/48
#
#
#  o Specific DNN/APN(e.g 'ims') uses 10.46.0.1/16, 2001:db8:babe::1/48
#    ; If the UE has unknown DNN/APN(not internet/ims), SMF/UPF will crash.
#
#    subnet:
#      - addr: 10.45.0.1/16
#        dnn: internet
#      - addr: 2001:db8:cafe::1/48
#        dnn: internet
#      - addr: 10.46.0.1/16
#        dnn: ims
#      - addr: 2001:db8:babe::1/48
#        dnn: ims
#
#  o Specific DNN/APN with the FALLBACK SUBNET(10.47.0.1/16)
#    ; Note that put the FALLBACK SUBNET last to avoid SMF/UPF crash.
#
#    subnet:
#      - addr: 10.45.0.1/16
#        dnn: internet
#      - addr: 10.46.0.1/16
#        dnn: ims
#      - addr: 10.50.0.1/16 ## FALLBACK SUBNET
#
#  o Pool Range Sample
#    subnet:
#      - addr: 10.45.0.1/24
#        range: 10.45.0.100-10.45.0.200
#
#    subnet:
#      - addr: 10.45.0.1/24
#        range:
#          - 10.45.0.5-10.45.0.50
#          - 10.45.0.100-
#
#    subnet:
#      - addr: 10.45.0.1/24
#        range:
#          - -10.45.0.200
#          - 10.45.0.210-10.45.0.220
#
#    subnet:
#      - addr: 10.45.0.1/16
#        range:
#          - 10.45.0.100-10.45.0.200
#          - 10.45.1.100-10.45.1.200
#      - addr: 2001:db8:cafe::1/48
#        range:
#          - 2001:db8:cafe:a0::0-2001:db8:cafe:b0::0
#          - 2001:db8:cafe:c0::0-2001:db8:cafe:d0::0
#
#  <Domain Name Server>
#
#  o Primary/Secondary can be configured. Others are ignored.
#
#    dns:
#      - 8.8.8.8
#      - 8.8.4.4
#      - 2001:4860:4860::8888
#      - 2001:4860:4860::8844
#
#  <MTU Size>
#
#  o Provisioning a limit on the size of the packets sent by the MS
#    to avoid packet fragmentation in the backbone network
#    between the MS and the GGSN/PGW and/or across the (S)Gi reference point)
#    when some of the backbone links does not support
#    packets larger then 1500 octets
#
#  <P-CSCF>
#
#  o Proxy Call Session Control Function
#
#    p-cscf:
#      - 127.0.0.1
#      - ::1
#
#  <CTF>
#
#  o Gy interface parameters towards OCS.
#  o enabled:
#    o auto: Default. Use Gy only if OCS available among Diameter peers
#    o yes:  Use Gy always;
#            reject subscribers if no OCS available among Diameter peers
#    o no:   Don't use Gy interface if there is an OCS available
#
#    ctf:
#      enabled: auto|yes|no
#
#
#  <SMF Selection - 5G Core only>
#  1. SMF sends SmfInfo(S-NSSAI, DNN, TAI) to the NRF
#  2. NRF responds to AMF with SmfInfo during NF-Discovery.
#  3. AMF selects SMF based on S-NSSAI, DNN and TAI in SmfInfo.
#
#  Note that if there is no SmfInfo, any AMF can select this SMF.
#
#  o S-NSSAI[SST:1] and DNN[internet] - At least 1 DNN is required in S-NSSAI
#    info:
#      - s_nssai:
#          - sst: 1
#            dnn:
#              - internet
#
#  o S-NSSAI[SST:1 SD:009000] and DNN[internet or ims]
#    info:
#      - s_nssai:
#          - sst: 1
#            sd: 009000
#            dnn:
#              - internet
#              - ims
#
#  o S-NSSAI[SST:1] and DNN[internet] and TAI[PLMN-ID:90170 TAC:1]
#    info:
#      - s_nssai:
#          - sst: 1
#            dnn:
#              - internet
#        tai:
#          - plmn_id:
#              mcc: 901
#              mnc: 70
#            tac: 1
#
#  o If any of conditions below are met:
#   - S-NSSAI[SST:1] and DNN[internet] and TAI[PLMN-ID:90170 TAC:1-9]
#   - S-NSSAI[SST:2 SD:000080] and DNN[internet or ims]
#   - S-NSSAI[SST:4] and DNN[internet] and TAI[PLMN-ID:90170 TAC:10-20,30-40]
#
#    info:
#      - s_nssai:
#          - sst: 1
#            dnn:
#              - internet
#        tai:
#          - plmn_id:
#              mcc: 901
#              mnc: 70
#            range:
#              - 1-9
#      - s_nssai:
#          - sst: 2
#            sd: 000080
#            dnn:
#              - internet
#              - ims
#      - s_nssai:
#          - sst: 4
#            dnn:
#              - internet
#        tai:
#          - plmn_id:
#              mcc: 901
#              mnc: 70
#            range:
#              - 10-20
#              - 30-40
#
#  o Complex Example
#    info:
#      - s_nssai:
#          - sst: 1
#            dnn:
#              - internet
#          - sst: 1
#            sd: 000080
#            dnn:
#              - internet
#              - ims
#          - sst: 1
#            sd: 009000
#            dnn:
#              [internet, ims]
#          - sst: 2
#            dnn:
#              - internet
#          - sst: 3
#            sd: 123456
#            dnn:
#              - internet
#        tai:
#          - plmn_id:
#              mcc: 901
#              mnc: 70
#            tac: [1, 2, 3]
#          - plmn_id:
#              mcc: 901
#              mnc: 70
#            tac: 4
#          - plmn_id:
#              mcc: 901
#              mnc: 70
#            tac:
#              - 5
#              - 6
#          - plmn_id:
#              mcc: 901
#              mnc: 70
#            range:
#              - 100-200
#              - 300-400
#          - plmn_id:
#              mcc: 901
#              mnc: 70
#            range:
#              - 500-600
#              - 700-800
#              - 900-1000
#      - s_nssai:
#          - sst: 4
#            dnn:
#              - internet
#        tai:
#          - plmn_id:
#              mcc: 901
#              mnc: 70
#            tac: 99
#

smf:
    sbi:
      - addr: 127.0.0.4
        port: 7777
    pfcp:
      - addr: 127.0.0.4
      - addr: ::1
    gtpc:
      - addr: 127.0.0.4
      - addr: ::1
    gtpu:
      - addr: 127.0.0.4
      - addr: ::1
    subnet:
      - addr: 10.45.0.1/16
      - addr: 2001:db8:cafe::1/48
    dns:
      - 8.8.8.8
      - 8.8.4.4
      - 2001:4860:4860::8888
      - 2001:4860:4860::8844
    mtu: 1400
    ctf:
      enabled: auto
    freeDiameter: /etc/freeDiameter/smf.conf

#
# nrf:
#
#  <SBI Client>>
#
#  o SBI Client(http://127.0.0.1:7777)
#    sbi:
#      addr: 127.0.0.10
#      port: 7777
#
#  o SBI Client(https://127.0.0.10:443, http://nrf.open5gs.org:80)
#    sbi:
#      - addr: 127.0.0.10
#        tls:
#          key: nrf.key
#          pem: nrf.pem
#      - name: nrf.open5gs.org
#
#  o SBI Client(http://[fd69:f21d:873c:fa::1]:80)
#    If prefer_ipv4 is true, http://127.0.0.10:80 is selected.
#
#    sbi:
#      addr:
#        - 127.0.0.10
#        - fd69:f21d:873c:fa::1
#
#  o SBI Option (Default)
#    - tcp_nodelay : true
#    - so_linger.l_onoff : false
#
#    sbi:
#      addr: 127.0.0.10
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
nrf:
    sbi:
      - addr:
          - 127.0.0.10
          - ::1
        port: 7777

#
# upf:
#
#  <PFCP Client>>
#
#  o PFCP Client(127.0.0.7:8805)
#
#    pfcp:
#      addr: 127.0.0.7
#
#  <UPF Selection>
#
#  o Round-Robin
#    (note that round robin can be disabled for a particular node
#     by setting flag 'rr' to 0)
#
#  upf:
#    pfcp:
#      - addr: 127.0.0.7
#      - addr: 127.0.0.12
#        rr: 0
#      - addr: 127.0.0.19
#
#  o UPF selection by eNodeB TAC
#    (either single TAC or multiple TACs, DECIMAL representation)
#
#  upf:
#    pfcp:
#      - addr: 127.0.0.7
#        tac: 1
#      - addr: 127.0.0.12
#        tac: [3,5,8]
#
#  o UPF selection by UE's DNN/APN (either single DNN/APN or multiple DNNs/APNs)
#
#  upf:
#    pfcp:
#      - addr: 127.0.0.7
#        dnn: ims
#      - addr: 127.0.0.12
#        dnn: [internet, web]
#
#  o UPF selection by CellID(e_cell_id: 28bit, nr_cell_id: 36bit)
#    (either single enb_id or multiple enb_ids, HEX representation)
#
#  upf:
#    pfcp:
#      - addr: 127.0.0.7
#        e_cell_id: 463
#      - addr: 127.0.0.12
#        nr_cell_id: [123456789, 9413]
#
upf:
    pfcp:
      - addr: 127.0.0.7

#
# parameter:
#
#  o Disable use of IPv4 addresses (only IPv6)
#      no_ipv4: true
#
#  o Disable use of IPv6 addresses (only IPv4)
#      no_ipv6: true
#
#  o Prefer IPv4 instead of IPv6 for estabishing new GTP connections.
#      prefer_ipv4: true
#
#  o Disable selection of UPF PFCP in Round-Robin manner
#      no_pfcp_rr_select: true
#
#  o Legacy support for pre-release LTE 11 devices
#    - Omits adding local address in packet filters for compatibility
#      no_ipv4v6_local_addr_in_packet_filter: true
#
parameter:

#
# max:
#
# o Maximum Number of UE per AMF/MME
#    ue: 1024
# o Maximum Number of gNB/eNB per AMF/MME
#    gnb: 64
#
max:

#
# time:
#
#  o NF Instance Heartbeat (Default : 0)
#    NFs will not send heart-beat timer in NFProfile
#    NRF will send heart-beat timer in NFProfile
#
#  o NF Instance Heartbeat (20 seconds)
#    NFs will send heart-beat timer (20 seconds) in NFProfile
#    NRF can change heart-beat timer in NFProfile
#
#    nf_instance:
#      heartbeat: 20
#
#  o Message Wait Duration (Default : 10,000 ms = 10 seconds)
#
#  o Message Wait Duration (3000 ms)
#    message:
#        duration: 3000
#
#  o Handover Wait Duration (Default : 300 ms)
#    Time to wait for SMF to send
#    PFCP Session Modification Request(Remove Indirect Tunnel) to the UPF
#    after sending Nsmf_PDUSession_UpdateSMContext Response(hoState:COMPLETED)
#
#  o Handover Wait Duration (500ms)
#    handover:
#        duration: 500
time:
"""

        return cfg

    @classmethod
    def get_startup(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the startup commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of startup commands to run
        """
        return cls.startup

    @classmethod
    def get_validate(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the validate commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of commands to validate service startup with
        """
        return cls.validate

class PGWUService(CoreService):

    name: str = "PGWU"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-upfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs",)
    configs: Tuple[str, ...] = ("/etc/open5gs/upf.yaml",)
    startup: Tuple[str, ...] = ("open5gs-upfd",)
    validate: Tuple[str, ...] = ()
    validation_mode: ServiceMode = ServiceMode.NON_BLOCKING
    validation_timer: int = 5
    validation_period: float = 0.5
    shutdown: Tuple[str, ...] = ()

    @classmethod
    def on_load(cls) -> None:
        """
        Provides a way to run some arbitrary logic when the service is loaded, possibly
        to help facilitate dynamic settings for the environment.

        :return: nothing
        """
        pass

    @classmethod
    def get_configs(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the config files from the node a service
        will run. Defaults to the class definition and can be left out entirely if not
        needed.

        :param node: core node that the service is being ran on
        :return: tuple of config files to create
        """
        return cls.configs

    @classmethod
    def generate_config(cls, node: CoreNode, filename: str) -> str:
        """
        Returns a string representation for a file, given the node the service is
        starting on the config filename that this information will be used for. This
        must be defined, if "configs" are defined.

        :param node: core node that the service is being ran on
        :param filename: configuration file to generate
        :return: configuration file content
        """
        cfg = """#
# logger:
#
#  o Set OGS_LOG_INFO to all domain level
#   - If `level` is omitted, the default level is OGS_LOG_INFO)
#   - If `domain` is omitted, the all domain level is set from 'level'
#    (Nothing is needed)
#
#  o Set OGS_LOG_ERROR to all domain level
#   - `level` can be set with none, fatal, error, warn, info, debug, trace
#    level: error
#
#  o Set OGS_LOG_DEBUG to mme/emm domain level
#    level: debug
#    domain: mme,emm
#
#  o Set OGS_LOG_TRACE to all domain level
#    level: trace
#    domain: core,pfcp,gtp,upf,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/upf.log

#
# upf:
#
#  <PFCP Server>
#
#  o PFCP Server(127.0.0.7:8805, ::1:8805)
#    pfcp:
#      - addr: 127.0.0.7
#      - addr: ::1
#
#  o PFCP-U Server(127.0.0.1:2152, [::1]:2152)
#    pfcp:
#      name: localhost
#
#  o PFCP Option (Default)
#    - so_bindtodevice : NULL
#
#    pfcp:
#      addr: 127.0.0.7
#      option:
#        so_bindtodevice: vrf-blue
#
#  <GTP-U Server>>
#
#  o GTP-U Server(127.0.0.7:2152, [::1]:2152)
#    gtpu:
#      - addr: 127.0.0.7
#      - addr: ::1
#
#  o GTP-U Server(127.0.0.1:2152, [::1]:2152)
#    gtpu:
#      name: localhost
#
#  o User Plane IP Resource information
#    gtpu:
#      - addr:
#        - 127.0.0.7
#        - ::1
#        teid_range_indication: 4
#        teid_range: 10
#        network_instance: internet
#        source_interface: 0
#      - addr: 127.0.10.4
#        teid_range_indication: 4
#        teid_range: 5
#        network_instance: ims
#        source_interface: 1
#
#  o Provide custom UPF GTP-U address to be advertised inside NGAP messages
#    gtpu:
#      - addr: 10.4.128.21
#        advertise: 172.24.15.30
#
#    gtpu:
#      - addr: 10.4.128.21
#        advertise:
#        - 127.0.0.1
#        - ::1
#
#    gtpu:
#      - addr: 10.4.128.21
#        advertise: upf1.5gc.mnc001.mcc001.3gppnetwork.org
#
#    gtpu:
#      - dev: ens3
#        advertise: upf1.5gc.mnc001.mcc001.3gppnetwork.org
#
#  o GTP-U Option (Default)
#    - so_bindtodevice : NULL
#
#    gtpu:
#      addr: 127.0.0.7
#      option:
#        so_bindtodevice: vrf-blue
#
#  <Subnet for UE network>
#
#  Note that you need to setup your UE network using TUN device.
#  (ogstun, ogstun2, ogstunX, ..)
#
#  o IPv4 Pool
#    $ sudo ip addr add 10.45.0.1/16 dev ogstun
#
#    subnet:
#      addr: 10.45.0.1/16
#
#  o IPv4/IPv6 Pool
#    $ sudo ip addr add 10.45.0.1/16 dev ogstun
#    $ sudo ip addr add 2001:db8:cafe::1/48 dev ogstun
#
#    subnet:
#      - addr: 10.45.0.1/16
#      - addr: 2001:db8:cafe::1/48
#
#
#  o Specific DNN/APN(e.g 'ims') uses 10.46.0.1/16, 2001:db8:babe::1/48
#    All other APNs use 10.45.0.1/16, 2001:db8:cafe::1/48
#    $ sudo ip addr add 10.45.0.1/16 dev ogstun
#    $ sudo ip addr add 10.46.0.1/16 dev ogstun
#    $ sudo ip addr add 2001:db8:cafe::1/48 dev ogstun
#    $ sudo ip addr add 2001:db8:babe::1/48 dev ogstun
#
#    ; If the UE has unknown DNN/APN(not internet/ims), SMF/UPF will crash.
#
#    subnet:
#      - addr: 10.45.0.1/16
#        dnn: internet
#      - addr: 2001:db8:cafe::1/48
#        dnn: internet
#      - addr: 10.46.0.1/16
#        dnn: ims
#      - addr: 2001:db8:babe::1/48
#        dnn: ims
#
#  o Specific DNN/APN with the FALLBACK SUBNET(10.47.0.1/16)
#    ; Note that put the FALLBACK SUBNET last to avoid SMF/UPF crash.
#
#    subnet:
#      - addr: 10.45.0.1/16
#        dnn: internet
#      - addr: 10.46.0.1/16
#        dnn: ims
#      - addr: 10.50.0.1/16 ## FALLBACK SUBNET
#
#  o Multiple Devices (default: ogstun)
#    $ sudo ip addr add 10.45.0.1/16 dev ogstun
#    $ sudo ip addr add 2001:db8:cafe::1/48 dev ogstun2
#    $ sudo ip addr add 10.46.0.1/16 dev ogstun3
#    $ sudo ip addr add 2001:db8:babe::1/48 dev ogstun3
#
#    subnet:
#      - addr: 10.45.0.1/16
#        dnn: internet
#      - addr: 2001:db8:cafe::1/48
#        dnn: internet
#        dev: ogstun2
#      - addr: 10.46.0.1/16
#        dnn: ims
#        dev: ogstun3
#      - addr: 2001:db8:babe::1/48
#        dnn: ims
#        dev: ogstun3
#
upf:
    pfcp:
      - addr: 127.0.0.7
    gtpu:
      - addr: 127.0.0.7
    subnet:
      - addr: 10.45.0.1/16
      - addr: 2001:db8:cafe::1/48

#
# smf:
#
#  <PFCP Client>>
#
#  o PFCP Client(127.0.0.4:8805)
#
#    pfcp:
#      addr: 127.0.0.4
#
smf:

#
# parameter:
#
#  o Number of output streams per SCTP associations.
#      sctp_streams: 30
#
#  o Disable use of IPv4 addresses (only IPv6)
#      no_ipv4: true
#
#  o Disable use of IPv6 addresses (only IPv4)
#      no_ipv6: true
#
#  o Prefer IPv4 instead of IPv6 for estabishing new GTP connections.
#      prefer_ipv4: true
#
parameter:

#
# max:
#
# o Maximum Number of UE per AMF/MME
#    ue: 1024
# o Maximum Number of gNB/eNB per AMF/MME
#    gnb: 64
#
max:

#
# time:
#
#  o Message Wait Duration (Default : 10,000 ms = 10 seconds)
#
#  o Message Wait Duration (3000 ms)
#    message:
#        duration: 3000
time:
"""

        return cfg

    @classmethod
    def get_startup(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the startup commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of startup commands to run
        """
        return cls.startup

    @classmethod
    def get_validate(cls, node: CoreNode) -> Tuple[str, ...]:
        """
        Provides a way to dynamically generate the validate commands from the node a
        service will run. Defaults to the class definition and can be left out entirely
        if not needed.

        :param node: core node that the service is being ran on
        :return: tuple of commands to validate service startup with
        """
        return cls.validate

