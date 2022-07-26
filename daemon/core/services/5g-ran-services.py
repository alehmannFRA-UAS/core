"""
Simple example custom service, used to drive shell commands on a node.
"""
from typing import Tuple
from core.nodes.base import CoreNode
from core.services.coreservices import CoreService, ServiceMode

GROUP_NAME = "5G"

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


class AMFService(CoreService):

    name: str = "AMF"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-amfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ('/etc/open5gs', '/var/log/open5gs',)
    configs: Tuple[str, ...] = ('/etc/open5gs/amf.yaml', 'start_amf.sh')
    startup: Tuple[str, ...] = ("sh start_amf.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """# logger:
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
#    domain: core,ngap,nas,gmm,sbi,amf,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/amf.log
#
# amf:
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
#          key: amf.key
#          pem: amf.pem
#
#  o SBI Server(https://127.0.0.5:443, http://[::1]:80)
#    sbi:
#      - addr: 127.0.0.5
#        tls:
#          key: amf.key
#          pem: amf.pem
#      - addr: ::1
#
#  o SBI Server(http://amf.open5gs.org:80)
#    sbi:
#      - name: amf.open5gs.org
#
#  o SBI Server(http://127.0.0.5:7777)
#    sbi:
#      - addr: 127.0.0.5
#        port: 7777
#
#  o SBI Server(http://<eth0 IP address>:80)
#    sbi:
#      - dev: eth0
#
#  o Provide custom SBI address to be advertised to NRF
#    sbi:
#      - dev: eth0
#        advertise: open5gs-amf.svc.local
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
#      addr: 127.0.0.5
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
#  <NGAP Server>>
#
#  o NGAP Server(all address avaiable)
#    ngap:
#
#  o NGAP Server(0.0.0.0:38412)
#    ngap:
#      addr: 0.0.0.0
#
#  o NGAP Server(127.0.0.5:38412, [::1]:38412)
#    ngap:
#      - addr: 127.0.0.5
#      - addr: ::1
#
#  o NGAP Server(different port)
#    ngap:
#      - addr: 127.0.0.5
#        port: 38413
#
#  o NGAP Server(address avaiable in `eth0` interface)
#    ngap:
#      dev: eth0
#
#  o NGAP Option (Default)
#    - sctp_nodelay : true
#    - so_linger.l_onoff : false
#
#    ngap:
#      addr: 127.0.0.5
#      option:
#        stcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
#  o NGAP SCTP Option (Default)
#    - spp_hbinterval : 5000 (5secs)
#    - spp_sackdelay : 200 (200ms)
#    - srto_initial : 3000 (3secs)
#    - srto_min : 1000 (1sec)
#    - srto_max : 5000 (5secs)
#    - sinit_num_ostreams : 30
#    - sinit_max_instreams : 65535
#    - sinit_max_attempts : 4
#    - sinit_max_init_timeo : 8000(8secs)
#
#    ngap:
#      addr: 127.0.0.5
#      option:
#        sctp:
#          spp_hbinterval : 5000
#          spp_sackdelay : 200
#          srto_initial : 3000
#          srto_min : 1000
#          srto_max : 5000
#          sinit_num_ostreams : 30
#          sinit_max_instreams : 65535
#          sinit_max_attempts : 4
#          sinit_max_init_timeo : 8000
#
#  <GUAMI>
#
#  o Multiple GUAMI
#    guami:
#      - plmn_id:
#          mcc: 901
#          mnc: 70
#        amf_id:
#          region: 2
#          set: 1
#          pointer: 4
#      - plmn_id:
#          mcc: 001
#          mnc: 01
#        amf_id:
#          region: 5
#          set: 2
#
#  <TAI>
#
#  o Multiple TAI
#    tai:
#      - plmn_id:
#          mcc: 001
#          mnc: 01
#        tac: [1, 2, 3]
#    tai:
#      - plmn_id:
#          mcc: 002
#          mnc: 02
#        tac: 4
#      - plmn_id:
#          mcc: 003
#          mnc: 03
#        tac: 5
#    tai:
#      - plmn_id:
#          mcc: 004
#          mnc: 04
#        tac: [6, 7]
#      - plmn_id:
#          mcc: 005
#          mnc: 05
#        tac: 8
#      - plmn_id:
#          mcc: 006
#          mnc: 06
#        tac: [9, 10]
#
#  <PLMN Support>
#
#  o Multiple PLMN Support
#    plmn_support:
#      - plmn_id:
#          mcc: 901
#          mnc: 70
#        s_nssai:
#          - sst: 1
#            sd: 010000
#      - plmn_id:
#          mcc: 901
#          mnc: 70
#        s_nssai:
#          - sst: 1
#
#  <Network Name>
#
#    network_name:
#        full: Open5GS
#        short: Next
#
#  <AMF Name>
#
#    amf_name: amf1.open5gs.amf.5gc.mnc70.mcc901.3gppnetwork.org
#
#  <Relative Capacity> - Default(255)
#
#    relative_capacity: 100
#
amf:
    sbi:
      - addr: <IP OF AMF HERE>
        port: 7777
    ngap:
      - addr: <IP OF AMF HERE>
    guami:
      - plmn_id:
          mcc: 001
          mnc: 01
        amf_id:
          region: 2
          set: 1
    tai:
      - plmn_id:
          mcc: 001
          mnc: 01
        tac: 1
    plmn_support:
      - plmn_id:
          mcc: 001
          mnc: 01
        s_nssai:
          - sst: 1
    security:
        integrity_order : [ NIA2, NIA1, NIA0 ]
        ciphering_order : [ NEA0, NEA1, NEA2 ]
    network_name:
        full: Open5GS
    amf_name: open5gs-amf0

#
# nrf:
#
#  <SBI Client>>
#
#  o SBI Client(http://127.0.0.10:7777)
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
      - addr: <IP OF NRF HERE>
        port: 7777

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
# usrsctp:
#    udp_port : 9899
#
usrsctp:

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
#    Time to wait for AMF to send UEContextReleaseCommand
#    to the source gNB after receiving HandoverNotify
#
#  o Handover Wait Duration (500ms)
#    handover:
#        duration: 500
time:
"""
        elif filename == cls.configs[1]:
            cfg += """#!/bin/sh
open5gs-amfd -D
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

class AUSFService(CoreService):

    name: str = "AUSF"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-ausfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ('/etc/open5gs', '/var/log/open5gs',)
    configs: Tuple[str, ...] = ('/etc/open5gs/ausf.yaml', 'start_ausf.sh')
    startup: Tuple[str, ...] = ("sh start_ausf.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """#
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
#    domain: core,sbi,ausf,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/ausf.log
#
# ausf:
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
#          key: ausf.key
#          pem: ausf.pem
#
#  o SBI Server(https://127.0.0.11:443, http://[::1]:80)
#    sbi:
#      - addr: 127.0.0.11
#        tls:
#          key: ausf.key
#          pem: ausf.pem
#      - addr: ::1
#
#  o SBI Server(http://ausf.open5gs.org:80)
#    sbi:
#      - name: ausf.open5gs.org
#
#  o SBI Server(http://127.0.0.11:7777)
#    sbi:
#      - addr: 127.0.0.11
#        port: 7777
#
#  o SBI Server(http://<eth0 IP address>:80)
#    sbi:
#      - dev: eth0
#
#  o Provide custom SBI address to be advertised to NRF
#    sbi:
#      - dev: eth0
#        advertise: open5gs-ausf.svc.local
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
#      addr: 127.0.0.11
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
ausf:
    sbi:
      - addr: <IP OF AUSF HERE>
        port: 7777

#
# nrf:
#
#  <SBI Client>>
#
#  o SBI Client(http://127.0.0.10:7777)
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
      - addr: <IP OF NRF HERE>
        port: 7777

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
time:
"""
        elif filename == cls.configs[1]:
            cfg += """#!/bin/sh
open5gs-ausfd -D      
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

class BSFService(CoreService):

    name: str = "BSF"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-bsfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ('/etc/open5gs', '/var/log/open5gs',)
    configs: Tuple[str, ...] = ('/etc/open5gs/bsf.yaml', 'start_bsf.sh',)
    startup: Tuple[str, ...] = ("sh start_bsf.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """db_uri: mongodb://<IP OF MONGODB HERE>:27017/open5gs

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
#    domain: core,sbi,bsf,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/bsf.log
#
# bsf:
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
#          key: bsf.key
#          pem: bsf.pem
#
#  o SBI Server(https://127.0.0.15:443, http://[::1]:80)
#    sbi:
#      - addr: 127.0.0.15
#        tls:
#          key: bsf.key
#          pem: bsf.pem
#      - addr: ::1
#
#  o SBI Server(http://bsf.open5gs.org:80)
#    sbi:
#      - name: bsf.open5gs.org
#
#  o SBI Server(http://127.0.0.15:7777)
#    sbi:
#      - addr: 127.0.0.15
#        port: 7777
#
#  o SBI Server(http://<eth0 IP address>:80)
#    sbi:
#      - dev: eth0
#
#  o Provide custom SBI address to be advertised to NRF
#    sbi:
#      - dev: eth0
#        advertise: open5gs-bsf.svc.local
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
#      addr: 127.0.0.15
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
bsf:
    sbi:
      - addr: <IP OF BSF HERE>
        port: 7777

#
# nrf:
#
#  <SBI Client>>
#
#  o SBI Client(http://127.0.0.10:7777)
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
      - addr: <IP OF NRF HERE>
        port: 7777

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
time:
"""
        elif filename == cls.configs[1]:
            cfg += """#!/bin/sh
# Block start of Network Function until MongoDB has correctly started
while ! nc -z <IP of MongoDB> <Port of MongoDB (default: 27017)>; do
 sleep 0.5
done
open5gs-bsfd -D
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

class NRFService(CoreService):

    name: str = "NRF"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-nrfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs/")
    configs: Tuple[str, ...] = ("/etc/open5gs/nrf.yaml", "start_nrf.sh")
    startup: Tuple[str, ...] = ("sh start_nrf.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """db_uri: mongodb://<IP OF MONGODB HERE>:27017/open5gs

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
#    domain: core,sbi,nrf,event,mem,sock
#
logger:
    file: /var/log/open5gs/nrf.log

#
# nrf:
#
#  <SBI Server>
#
#  o SBI Server(http://<all address available>:80)
#    sbi:
#
#  o SBI Server(http://<any address>:7777)
#    sbi:
#      - addr:
#          - 0.0.0.0
#          - ::0
#        port: 7777
#
#  o SBI Server(https://<all address avaiable>:443)
#    sbi:
#        tls:
#          key: nrf.key
#          pem: nrf.pem
#
#  o SBI Server(https://127.0.0.10:443, http://[::1]:80)
#    sbi:
#      - addr: 127.0.0.10
#        tls:
#          key: nrf.key
#          pem: nrf.pem
#      - addr: ::1
#
#  o SBI Server(http://nrf.open5gs.org:80)
#    sbi:
#      name: nrf.open5gs.org
#
#  o SBI Server(http://127.0.0.10:7777)
#    sbi:
#      - addr: 127.0.0.10
#        port: 7777
#
#  o SBI Server(http://<eth0 IP address>:80)
#    sbi:
#      dev: eth0
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
      addr: <IP OF NRF HERE>
      port: 7777

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
#  o NF Instance Heartbeat (Default : 10 seconds)
#
#  o NF Instance Heartbeat (Disabled)
#    nf_instance:
#      heartbeat: 0
#
#  o NF Instance Heartbeat (5 seconds)
#    nf_instance:
#      heartbeat: 5
#
#  o NF Instance Validity (Default : 3600 seconds = 1 hour)
#
#  o NF Instance Validity (10 seconds)
#    nf_instance:
#      validity: 10
#
#  o Subscription Validity (Default : 86400 seconds = 1 day)
#
#  o Subscription Validity (Disabled)
#    subscription:
#      validity: 0
#
#  o Subscription Validity (3600 seconds = 1 hour)
#    subscription:
#      validity: 3600
#
#  o Message Wait Duration (Default : 10,000 ms = 10 seconds)
#
#  o Message Wait Duration (3000 ms)
#    message:
#        duration: 3000
time:
"""
        elif filename == cls.configs[1]:
            cfg += """#!/bin/sh
while ! nc -z <IP of MongoDB> <Port of MongoDB (default: 27017)>; do
 sleep 0.5
done
open5gs-nrfd -D
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

class NSSFService(CoreService):

    name: str = "NSSF"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-nssfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs/",)
    configs: Tuple[str, ...] = ("/etc/open5gs/nssf.yaml", "start_nssf.sh")
    startup: Tuple[str, ...] = ("sh start_nssf.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """#
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
#    domain: core,sbi,nssf,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/nssf.log
#
# nssf:
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
#          key: nssf.key
#          pem: nssf.pem
#
#  o SBI Server(https://127.0.0.14:443, http://[::1]:80)
#    sbi:
#      - addr: 127.0.0.14
#        tls:
#          key: nssf.key
#          pem: nssf.pem
#      - addr: ::1
#
#  o SBI Server(http://nssf.open5gs.org:80)
#    sbi:
#      - name: nssf.open5gs.org
#
#  o SBI Server(http://127.0.0.14:7777)
#    sbi:
#      - addr: 127.0.0.14
#        port: 7777
#
#  o SBI Server(http://<eth0 IP address>:80)
#    sbi:
#      - dev: eth0
#
#  o Provide custom SBI address to be advertised to NRF
#    sbi:
#      - dev: eth0
#        advertise: open5gs-nssf.svc.local
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
#      addr: 127.0.0.14
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
#  <List of avaiable Network Slice Instance(NSI)>
#
#  o One NSI
#   - NRF[http://::1:7777/nnrf-nfm/v1/nf-instances]
#     NSSAI[SST:1]
#
#    nsi:
#      - addr: ::1
#        port: 7777
#        s_nssai:
#          sst: 1
#
#  o Three NSI
#   1. NRF[http://::1:7777/nnrf-nfm/v1/nf-instances]
#      S-NSSAI[SST:1]
#
#   2. NRF[http://127.0.0.19:7777/nnrf-nfm/v1/nf-instances]
#      NSSAI[SST:1, SD:000080]
#
#   2. NRF[http://127.0.0.10:7777/nnrf-nfm/v1/nf-instances]
#      NSSAI[SST:1, SD:009000]
#
#    nsi:
#      - addr: ::1
#        port: 7777
#        s_nssai:
#          sst: 1
#      - addr: 127.0.0.19
#        port: 7777
#        s_nssai:
#          sst: 1
#          sd: 000080
#      - addr: 127.0.0.10
#        port: 7777
#        s_nssai:
#          sst: 1
#          sd: 009000
#
#  o NSI Option (Default)
#    - tcp_nodelay : true
#    - so_linger.l_onoff : false
#
#    nsi:
#      addr: ::1
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
nssf:
    sbi:
      - addr: <IP OF NSSF HERE>
        port: 7777
    nsi:
      - addr: ::1 # NOT SURE ABOUT THIS ONE
        port: 7777
        s_nssai:
          sst: 1

#
# nrf:
#
#  <SBI Client>>
#
#  o SBI Client(http://127.0.0.10:7777)
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
nrf:
    sbi:
      - addr: <IP OF NRF HERE>
        port: 7777

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
#  o NF Instance Heartbeat (Disabled)
#    nf_instance:
#      heartbeat: 0
#
#  o NF Instance Heartbeat (10 seconds)
#    nf_instance:
#      heartbeat: 10
#
#  o Message Wait Duration (Default : 10,000 ms = 10 seconds)
#
#  o Message Wait Duration (3000 ms)
#    message:
#        duration: 3000
time:
"""

        elif filename == cls.configs[1]:
            cfg += """#!/bin/sh
open5gs-nssfd -D
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

class PCFService(CoreService):

    name: str = "PCF"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-pcfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs",)
    configs: Tuple[str, ...] = ("/etc/open5gs/pcf.yaml", "start_pcf.sh")
    startup: Tuple[str, ...] = ("sh start_pcf.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """db_uri: mongodb://<IP OF MONGODB HERE>:27017/open5gs

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
#    domain: core,sbi,pcf,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/pcf.log
#
# pcf:
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
#          key: pcf.key
#          pem: pcf.pem
#
#  o SBI Server(https://127.0.0.13:443, http://[::1]:80)
#    sbi:
#      - addr: 127.0.0.13
#        tls:
#          key: pcf.key
#          pem: pcf.pem
#      - addr: ::1
#
#  o SBI Server(http://pcf.open5gs.org:80)
#    sbi:
#      - name: pcf.open5gs.org
#
#  o SBI Server(http://127.0.0.13:7777)
#    sbi:
#      - addr: 127.0.0.13
#        port: 7777
#
#  o SBI Server(http://<eth0 IP address>:80)
#    sbi:
#      - dev: eth0
#
#  o Provide custom SBI address to be advertised to NRF
#    sbi:
#      - dev: eth0
#        advertise: open5gs-pcf.svc.local
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
#      addr: 127.0.0.13
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
pcf:
    sbi:
      - addr: <IP OF PCF HERE>
        port: 7777

#
# nrf:
#
#  <SBI Client>>
#
#  o SBI Client(http://127.0.0.10:7777)
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
      - addr: <IP OF NRF HERE>
        port: 7777

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
time:
"""
        elif filename == cls.configs[1]:
            cfg += """"#!/bin/sh
while ! nc -z <IP of MongoDB> <Port of MongoDB (default: 27017)>; do
 sleep 0.5
done
open5gs-pcfd -D
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

class SMFService(CoreService):

    name: str = "SMF"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-smfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs",)
    configs: Tuple[str, ...] = ("/etc/open5gs/smf.yaml","start_smf.sh")
    startup: Tuple[str, ...] = ("sh start_smf.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """#
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
      - addr: <IP OF SMF>
        port: 7777
    pfcp:
      - addr: <IP OF SMF>
    gtpc:
      - addr: <IP OF SMF>
    gtpu:
      - addr: <IP OF SMF>
    subnet:
      - addr: 10.45.0.1/16
        dnn: internet
    dns:
      - 8.8.8.8
      - 8.8.4.4
    mtu: 1400
    ctf:
      enabled: auto
    freeDiameter: /etc/freeDiameter/smf.conf
    info:
      - s_nssai:
          - sst: 1
            dnn:
              - internet
        tai:
          - plmn_id:
              mcc: 001
              mnc: 01
            tac: 1
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
      - addr: <IP OF NRF HERE>
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
      - addr: <IP OF UPF HERE>
        dnn: internet

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

        elif filename == cls.configs[1]:
            cfg += """#!/bin/sh
open5gs-smfd -D            
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

class UDMService(CoreService):

    name: str = "UDM"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-udmd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs",)
    configs: Tuple[str, ...] = ("/etc/open5gs/udm.yaml", "start_udmd.sh")
    #startup: Tuple[str, ...] = ("open5gs-udmd",)
    startup: Tuple[str, ...] = ("sh start_udmd.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """#
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
#    domain: core,sbi,udm,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/udm.log
#
# udm:
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
#          key: udm.key
#          pem: udm.pem
#
#  o SBI Server(https://127.0.0.12:443, http://[::1]:80)
#    sbi:
#      - addr: 127.0.0.12
#        tls:
#          key: udm.key
#          pem: udm.pem
#      - addr: ::1
#
#  o SBI Server(http://udm.open5gs.org:80)
#    sbi:
#      - name: udm.open5gs.org
#
#  o SBI Server(http://127.0.0.12:7777)
#    sbi:
#      - addr: 127.0.0.12
#        port: 7777
#
#  o SBI Server(http://<eth0 IP address>:80)
#    sbi:
#      - dev: eth0
#
#  o Provide custom SBI address to be advertised to NRF
#    sbi:
#      - dev: eth0
#        advertise: open5gs-udm.svc.local
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
#      addr: 127.0.0.12
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
udm:
    sbi:
      - addr: <IP OF UDM>
        port: 7777

#
# nrf:
#
#  <SBI Client>>
#
#  o SBI Client(http://127.0.0.10:7777)
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
      - addr: <IP OF NRF>
        port: 7777

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
time:
"""
        elif filename == cls.configs[1]:
            cfg += """#!/bin/sh
open5gs-udmd -D       
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

class UDRService(CoreService):

    name: str = "UDR"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-udrd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs/",)
    configs: Tuple[str, ...] = ("/etc/open5gs/udr.yaml", "start_udr.sh")
    #startup: Tuple[str, ...] = ("open5gs-udrd",)
    startup: Tuple[str, ...] = ("sh start_udr.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """db_uri: mongodb://<IP OF MONGODB HERE>:27017/open5gs
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
#    domain: core,sbi,udr,event,tlv,mem,sock
#
logger:
    file: /var/log/open5gs/udr.log
#
# udr:
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
#          key: udr.key
#          pem: udr.pem
#
#  o SBI Server(https://127.0.0.20:443, http://[::1]:80)
#    sbi:
#      - addr: 127.0.0.20
#        tls:
#          key: udr.key
#          pem: udr.pem
#      - addr: ::1
#
#  o SBI Server(http://udr.open5gs.org:80)
#    sbi:
#      - name: udr.open5gs.org
#
#  o SBI Server(http://127.0.0.20:7777)
#    sbi:
#      - addr: 127.0.0.20
#        port: 7777
#
#  o SBI Server(http://<eth0 IP address>:80)
#    sbi:
#      - dev: eth0
#
#  o Provide custom SBI address to be advertised to NRF
#    sbi:
#      - dev: eth0
#        advertise: open5gs-udr.svc.local
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
#      addr: 127.0.0.20
#      option:
#        tcp_nodelay: false
#        so_linger:
#          l_onoff: true
#          l_linger: 10
#
udr:
    sbi:
      - addr: <IP OF UDR>
        port: 7777

#
# nrf:
#
#  <SBI Client>>
#
#  o SBI Client(http://127.0.0.10:7777)
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
      - addr: <IP OF NRF>
        port: 7777

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
#  o NF Instance Heartbeat (Disabled)
#    nf_instance:
#      heartbeat: 0
#
#  o NF Instance Heartbeat (10 seconds)
#    nf_instance:
#      heartbeat: 10
#
#  o Message Wait Duration (Default : 10,000 ms = 10 seconds)
#
#  o Message Wait Duration (3000 ms)
#    message:
#        duration: 3000
time:
"""
        elif filename == cls.configs[1]:
            cfg += """#!/bin/sh
while ! nc -z <IP of MongoDB> <Port of MongoDB (default: 27017)>; do
 sleep 0.5
done
open5gs-udrd -D       
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

class UPFService(CoreService):

    name: str = "UPF"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ("open5gs-upfd",)
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/etc/open5gs", "/var/log/open5gs",)
    configs: Tuple[str, ...] = ("/etc/open5gs/upf.yaml", "start_upf.sh",)
    #startup: Tuple[str, ...] = ("open5gs-upfd", "ip addr add 10.0.45.0.1/16 dev ogstun", "ip link set ogstun up", "iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE",)
    startup: Tuple[str, ...] = ("sh start_upf.sh",)
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """#
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
      - addr: <IP OF UPF IN CORE NETWORK>
    gtpu:
      - addr: <IP OF UPF TO GNB>
    subnet:
      - addr: 10.45.0.1/16
        dnn: internet
        dev: ogstun

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
        elif filename == cls.configs[1]:
            cfg += """#!/bin/sh
open5gs-upfd -D
ip addr add 10.0.45.0.1/16 dev ogstun
ip link set ogstun up
iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
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

class MongoService(CoreService):
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

    name: str = "MongoDB"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ()
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ("/data/db", "/etc/mongo","/var/log/mongodb")
    configs: Tuple[str, ...] = ("/etc/mongo/mongodb.conf", "start_mongo.sh",)
    startup: Tuple[str, ...] = ()
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
        cfg = ""
        if filename == cls.configs[0]:
            cfg += """# mongodb.conf

# Where to store the data.
dbpath=/data/db

#where to log
logpath=/var/log/mongodb/mongodb.log

logappend=true

bind_ip = 0.0.0.0
#bind_ip = 127.0.0.1
#port = 27017

# Enable journaling, http://www.mongodb.org/display/DOCS/Journaling
journal=true

# Enables periodic logging of CPU utilization and I/O wait
#cpu = true

# Turn on/off security.  Off is currently the default
#noauth = true
#auth = true

# Verbose logging output.
#verbose = true

# Inspect all client data for validity on receipt (useful for
# developing drivers)
#objcheck = true

# Enable db quota management
#quota = true

# Set diagnostic logging level where n is
#   0=off (default)
#   1=W
#   2=R
#   3=both
#   7=W+some reads
#diaglog = 0

# Diagnostic/debugging option
#nocursors = true

# Ignore query hints
#nohints = true

# Disable the HTTP interface (Defaults to localhost:27018).
#nohttpinterface = true

# Turns off server-side scripting.  This will result in greatly limited
# functionality
#noscripting = true

# Turns off table scans.  Any query that would do a table scan fails.
#notablescan = true

# Disable data file preallocation.
#noprealloc = true

# Specify .ns file size for new databases.
# nssize = <size>

# Accout token for Mongo monitoring server.
#mms-token = <token>

# Server name for Mongo monitoring server.
#mms-name = <server-name>

# Ping interval for Mongo monitoring server.
#mms-interval = <seconds>

# Replication Options

# in replicated mongo databases, specify here whether this is a slave or master
#slave = true
#source = master.example.com
# Slave only: specify a single database to replicate
#only = master.example.com
# or
#master = true
#source = slave.example.com

# Address of a server to pair with.
#pairwith = <server:port>
# Address of arbiter server.
#arbiter = <server:port>
# Automatically resync if slave data is stale
#autoresync
# Custom size for replication operation log.
#oplogSize = <MB>
# Size limit for in-memory storage of op ids.
#opIdMem = <bytes>

# SSL options
# Enable SSL on normal ports
#sslOnNormalPorts = true
# SSL Key file and password
#sslPEMKeyFile = /etc/ssl/mongodb.pem
#sslPEMKeyPassword = pass

        """
        elif filename == cls.configs[1]:
            cfg += "#!/bin/sh\n\n"
            cfg += "# Start MongoDB with config file\n"
            cfg += "mongod --config etc.mongo/mongodb.conf &\n\n"
            cfg += "# Wait until MongoDB has started\n"
            cfg += "sleep 5\n\n"
            cfg += "# Configure users with open5gs-dbctl here\n"
            cfg += "open5gs-dbctl --db_uri=mongodb://localhost/open5gs add 001010000000001 465B5CE8B199B49FAA5F0A2EE238A6BC E8ED289DEBA952E4283B54E88E6183CA\n"
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

class WebUIService(CoreService):

    name: str = "WebUI"
    group: str = GROUP_NAME
    executables: Tuple[str, ...] = ( )
    dependencies: Tuple[str, ...] = ()
    dirs: Tuple[str, ...] = ( )
    configs: Tuple[str, ...] = ("start_webui.sh",)
    #startup: Tuple[str, ...] = ("open5gs-upfd", "ip addr add 10.0.45.0.1/16 dev ogstun", "ip link set ogstun up", "iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE",)
    startup: Tuple[str, ...] = ("sh start_webui.sh",)
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
        cfg = """#!/bin/sh
cp -rf /home/gregor/open5gs-webui .
export DB_URI="mongodb://<IP OF MONGODB>/open5gs"
cd open5gs-webui
npm run start
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
