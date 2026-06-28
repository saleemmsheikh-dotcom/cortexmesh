def adjust_reliability(item, success):
    current = item.get("reliability", 1.0)

    if success:
        current += 0.04
    else:
        current -= 0.06

    item["reliability"] = max(0.3, min(1.5, current))


def reliable(item, threshold=0.7):
    return item.get("reliability", 1.0) >= threshold
