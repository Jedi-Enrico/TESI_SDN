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
##        match = parser.OFPMatch()
##        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,ofproto.OFPCML_NO_BUFFER)]

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        self.device_behaviour._packet_in_handler(ev)
##        msg = ev.msg
##        datapath = msg.datapath
##        ofproto = datapath.ofproto
##        parser = datapath.ofproto_parser
##        in_port = msg.match['in_port']
##        ip_dscp = msg.match.get('ip_dscp')
##        print 'ip dscp',ip_dscp
##        pkt = packet.Packet(msg.data)
##        eth = pkt.get_protocols(ethernet.ethernet)[0]
##        pkt = packet.Packet(msg.data)
##        arp_pkt = pkt.get_protocol(arp.arp)
##        ip_pkt = pkt.get_protocol(ipv4.ipv4)
##        dst = eth.dst
##        src=eth.src
##        print src
##        dpid = datapath.id
##        self.mac_to_port.setdefault(dpid, {})
##        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        # learn a mac address to avoid FLOOD next time.
##        self.mac_to_port[dpid][src] = in_port

##        if dst in self.mac_to_port[dpid]:
##            out_port = self.mac_to_port[dpid][dst]
##        else:
##            out_port = ofproto.OFPP_FLOOD
##            actions = [parser.OFPActionOutput(out_port)]
##        arp_pkt = pkt.get_protocol(arp.arp)
##
##         
##
##        # install a flow to avoid packet_in next time
##        if out_port != ofproto.OFPP_FLOOD:
##            if arp_pkt:
##                match = parser.OFPMatch( in_port=in_port, eth_src=src)
##            elif ip_dscp is not None and ip_dscp != 0:
##                match = parser.OFPMatch( eth_type=0x0800,ip_dscp=ip_dscp)
##                print match
       
        

##    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
##    def port_stats_reply_handler(self, ev):
##        self.monitor.port_stats_reply(ev)

##    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
##    def flow_stats_reply_handler(self, ev):
##        self.monitor.flow_stats_reply(ev)

##    @set_ev_cls(ofp_event.EventOFPQueueStatsReply, MAIN_DISPATCHER)
##    def queue_stats_reply_handler(self, ev):
##        self.monitor.queue_stats_reply(ev)
##
##    @set_ev_cls(ofp_event.EventOFPQueueGetConfigReply, MAIN_DISPATCHER)
##    def queue_desc_reply_handler(self, ev):
##        self.monitor.queue_desc_reply(ev)




    @set_ev_cls(ofp_event.EventOFPDescStatsReply, MAIN_DISPATCHER)
    def desc_stat_reply_handler(self, ev):
        self.monitor.desc_reply(ev)

##    @set_ev_cls(ofp_event.EventOFPQueueStatsReply, MAIN_DISPATCHER)
##    def send_queue_stats_handler(self, ev):
##        self.monitor.queue_stats_reply(ev)

