import threading

timers = {}


def supervise_state(item_name, expected_state, action, timeout_seconds):
    if item_name in timers:
        timers[item_name].cancel()

    t = threading.Timer(timeout_seconds, action, args=(item_name, expected_state))
    t.start()
    timers[item_name] = t


def cancel_supervision(item_name):
    if item_name in timers:
        timers[item_name].cancel()
        del timers[item_name]
