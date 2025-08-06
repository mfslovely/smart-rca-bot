def parse_logs(log_data: str):
    lines = log_data.strip().split("\n")
    events = [line for line in lines if "ERROR" in line or "FAIL" in line]
    return events
