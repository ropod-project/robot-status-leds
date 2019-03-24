from __future__ import print_function
import time
from datetime import datetime
import uuid

from ropod.pyre_communicator.base_class import RopodPyre
from black_box_tools.data_utils import DataUtils

class LedPyreCommunicator(RopodPyre):
    '''A pyre communicator for receiving status from different components and
    setting the led lights accodingly.

    '''
    def __init__(self, robot_id='ropod_001', black_box_id='black_box_001'):
        super(LedPyreCommunicator, self).__init__(
                'led_pyre_communicator', ['MONITOR', 'ROPOD'], list(), verbose=False)
        self.robot_id = robot_id
        self.black_box_id = black_box_id
        self.sender_ids = []
        self.data = {
            'everything_working': False,
            'bringup_running': False,
            'robot_performing_task': False,
            'battery_percentage': 0.0,
            'e_stop_pressed': False,
            'bb_variables': {}
        }
        self.start()

    def send_query(self, variables):
        """create and send a query message to black box query interface through
        pyre shout.

        :variables: list of strings
        :returns: None

        """
        if len(variables) == 0:
            return None
        msg_sender_id = str(uuid.uuid4())
        data_query_msg = DataUtils.get_bb_latest_data_query_msg(
                msg_sender_id,
                self.black_box_id,
                variables)
        self.sender_ids.append(msg_sender_id)
        self.data['bb_variables'] = {}
        self.shout(data_query_msg)

    def send_fms_query(self):
        """Create and send a query message to fms query interface to get the 
        status of the robot.
        :returns: None

        """
        query_msg = {'header':{}, 'payload': {}}
        query_msg['header']['type'] = 'GET-ROBOT-STATUS'
        query_msg['header']['timestamp'] = datetime.now().timestamp()
        query_msg['header']['metamodel'] = 'ropod-msg-schema.json'
        query_msg['header']['msgId'] =  uuid.uuid4()

        msg_sender_id = str(uuid.uuid4())
        query_msg['payload']['senderId'] = msg_sender_id
        query_msg['payload']['robotId'] = self.robot_id
        self.sender_ids.append(msg_sender_id)
        self.shout(query_msg)

    def receive_msg_cb(self, msg):
        '''Processes requests for queries;

        :msg: string (a message in JSON format)

        '''
        dict_msg = self.convert_zyre_msg_to_dict(msg)
        if dict_msg is None:
            return

        if 'header' not in dict_msg or 'type' not in dict_msg['header']:
            return None

        message_type = dict_msg['header']['type']
        if message_type == "HEALTH-STATUS": #comp monitor shouts
            if 'robotId' not in dict_msg['payload']:
                return None
            message_robot_id = dict_msg['payload']['robotId']
            if message_robot_id != self.robot_id:
                return None

            status_msg = dict_msg['payload']['monitors']
            for component in status_msg:
                if component['component'] == 'ROS':
                    for monitor in component['modes']:
                        if monitor['monitorName'] == 'ros_node_monitor':
                            self.data['bringup_running'] = \
                                    monitor['healthStatus'].get('bringup', False)
                            break
                if component['component'] == 'battery_monitor':
                    self.data['battery_percentage'] = \
                            component['modes'][0]['healthStatus'].get('battery_percentage', 0.0)
                if component['component'] == 'e_stop_monitor':
                    self.data['e_stop_pressed'] = \
                            component['modes'][0]['healthStatus'].get('e_stop_pressed', False)

            statuses = [monitor.get('healthStatus', {'status':False}).get('status', False) \
                    for component in status_msg for monitor in component['modes']]
            self.data['everything_working'] = False not in statuses
            # print(self.data['everything_working'],self.data['bringup_running'], self.data['battery_percentage'])

        elif message_type == "LATEST-DATA-QUERY": # bb query interface response whisper
            if 'receiverId' not in dict_msg['payload']:
                return None
            receiver_id = dict_msg['payload']['receiverId']
            if receiver_id in self.sender_ids:
                self.data['bb_variables'] = dict_msg['payload']['dataList']
                self.sender_ids.remove(receiver_id)

        elif message_type == "GET-ROBOT-STATUS":
            if 'status' not in dict_msg['payload'] or 'receiverId' not in dict_msg['payload']:
                return None
            receiver_id = dict_msg['payload']['receiverId']
            if receiver_id in self.sender_ids:
                if dict_msg['payload']['success'] :
                    self.data['robot_performing_task'] = \
                            dict_msg['payload']['status'][self.robot_id] != 'idle'
                else:
                    self.data['robot_performing_task'] = False
                self.sender_ids.remove(receiver_id)

        else:
            return None


if __name__ == "__main__":
    led_pyre_comm = LedPyreCommunicator()

    try:
        while True:
            time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        print('Led pyre communicator interrupted. Exiting.')
        led_pyre_comm.shutdown()
