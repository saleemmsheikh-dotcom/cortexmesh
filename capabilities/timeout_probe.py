import time


def run(context):
    mode = context.input.get("mode", "sleep")

    if mode == "loop":
        while True:
            pass

    time.sleep(999999)
    return {"status": "unexpected_completion"}
