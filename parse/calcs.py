from datetime import datetime

def calc_time(a_h, a_m, b_h, b_m):
    
    time_stamp1, time_stamp2 = f"{a_h}:{a_m}", f"{b_h}:{b_m}"
    format_str = "%H:%M"
    time1 = datetime.strptime(time_stamp1, format_str)
    time2 = datetime.strptime(time_stamp2, format_str)

    time_diff = time2 - time1

    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes = remainder // 60

    return hours + 0.01 * minutes

def calc_salary(hours, minutes, wage, day):
    
    total = 0
    wage *= 1.5 if day in ['Friday', 'Saturday'] else 1

    if minutes:
        match hours:
            case hours if 8 <= hours < 10:
                total += (minutes / 60) * wage * 1.25
            case hours if 10 <= hours:
                total += (minutes / 60) * wage * 1.5
            case _:
                total += (minutes / 60) * wage

    while hours:
        match hours:
            case hours if 8 < hours <= 10:
                total += wage * 1.25
            case hours if 10 < hours:
                total += wage * 1.5
            case _:
                total += wage * hours
                break
        hours -= 1

    return total