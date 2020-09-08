from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from qos_simple_switch_13 import *
from datapath_monitor_TOS import *
from ryu.lib.packet import arp
from ryu.lib.packet.arp import ARP_REQUEST, ARP_REPLY
from ryu.lib.packet import ipv4


class MainControllerMonitor(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MainControllerMonitor, self).__init__(*args, **kwargs)
        self.device_behaviour = SimpleSwitch13(*args, **kwargs)
        self.datapath_id_list = []
        self.mac_to_port = {}
        STEP = 300
        args = {
            "step":STEP,
            "logger":self.logger,
            "dp":self.datapath_id_list
        }
        self.monitor = DatapathMonitor(args)
        self.monitor.start()

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_feature_handler(self, ev):
        self.device_behaviour.switch_features_handler(ev)
        datapath = ev.msg.datapath
        if datapath not in self.datapath_id_list:
            self.datapath_id_list.append(datapath)
            self.monitor.update(self.datapath_id_list)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        self.device_behaviour._packet_in_handler(ev)

    @set_ev_cls(ofp_event.EventOFPDescStatsReply, MAIN_DISPATCHER)
    def desc_stat_reply_handler(self, ev):
        self.monitor.desc_reply(ev)
