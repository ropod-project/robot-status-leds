import time
from ropod.pyre_communicator.base_class import RopodPyre

class LedPyreCommunicator(RopodPyre):
    '''A pyre communicator for receiving status from different components and
    setting the led lights accodingly.

    '''
    def __init__(self, robot_id='ropod_001'):
        super(LedPyreCommunicator, self).__init__(
                'led_pyre_communicator', ['MONITOR', 'ROPOD'], list(), verbose=False)
        self.robot_id = robot_id
        self.everything_working = False
        self.bringup_running = False
        self.start()

    def receive_msg_cb(self, msg):
        '''Processes requests for queries;

        :msg: string (a message in JSON format)

        '''
        dict_msg = self.convert_zyre_msg_to_dict(msg)
        if dict_msg is None:
            return

        if 'header' not in dict_msg or 'type' not in dict_msg['header'] or \
                'payload' not in dict_msg or 'robotId' not in dict_msg['payload']:
            return None

        message_type = dict_msg['header']['type']
        message_robot_id = dict_msg['payload']['robotId']
        if message_type != "HEALTH-STATUS" or message_robot_id != self.robot_id:
            return None

        status_msg = dict_msg['payload']['monitors']
        for component in status_msg:
            if component['component'] == 'ROS':
                for monitor in component['modes']:
                    if monitor['monitorName'] == 'ros_node_monitor':
                        self.bringup_running = monitor['healthStatus'].get('bringup', False)
                        break
                break
        statuses = [monitor.get('healthStatus', {'status':False}).get('status', False) \
                for component in status_msg for monitor in component['modes']]
        self.everything_working = False not in statuses
        # print(self.everything_working, self.bringup_running)


if __name__ == "__main__":
    led_pyre_comm = LedPyreCommunicator()

    try:
        while True:
            time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        print('Led pyre communicator interrupted. Exiting.')
        led_pyre_comm.shutdown()
