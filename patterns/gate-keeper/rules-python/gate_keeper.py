import queue
import threading
from datetime import datetime, timedelta

from openhab import rule, Registry
from openhab.actions import Exec
from openhab.triggers import ItemCommandTrigger

commands = queue.Queue()
gate_timer = None
last_command = datetime.now().astimezone() - timedelta(seconds=1)


def process_queue():
    global gate_timer, last_command
    if not commands.empty():
        cmd = commands.get()
        results = Exec.executeCommandLine(cmd, 5000)
        print("433: " + str(results))
        last_command = datetime.now().astimezone()

    delta_millis = (datetime.now().astimezone() - last_command).total_seconds() * 1000
    delay = (100 - delta_millis) / 1000 if delta_millis < 100 else 0
    gate_timer = threading.Timer(delay, process_queue)
    gate_timer.start()


@rule(triggers=[ItemCommandTrigger("WirelessController")])
class Controller433MHz:
    def execute(self, module, input):
        global gate_timer
        commands.put(str(input["command"]))

        if gate_timer is None:
            process_queue()


@rule(triggers=[ItemCommandTrigger("Outlet_A")])
class OutletA:
    def execute(self, module, input):
        if str(input["command"]) == "ON":
            Registry.getItem("WirelessController").sendCommand("433-send xxxxx 1 1")
        else:
            Registry.getItem("WirelessController").sendCommand("433-send xxxxx 1 0")
