import json
import os
import re

def read_local_cmdr_logs() -> str:
    try:
        os.mkdir("LOGFILES")
    except FileExistsError:
        pass

    cmdr = ""
    path_to_logs = os.path.expanduser('~') + "\\Saved Games\\Frontier Developments\\Elite Dangerous"
    for filename in os.listdir(path_to_logs):
        if filename.find(".log") != -1:
            log_file = open(os.path.join(path_to_logs, filename), encoding="utf-8")
            for line in log_file:
                entry = json.loads(line)
                if entry["event"] == "Commander":
                    cmdr = entry["Name"]
                    united_log_file = open(f"LOGFILES\\{entry['Name']}.log", "w", encoding="utf-8")
                    break
            log_file.close()
            if cmdr != "":
                break

    for filename in os.listdir(path_to_logs):
        if filename.find(".log") != -1:
            log_file = open(os.path.join(path_to_logs, filename), encoding="utf-8")
            for line in log_file:
                entry = json.loads(line)
                if entry["event"] == "Commander":
                    if entry["Name"] != cmdr:
                        break
                if entry["event"] == "Scan" and entry["ScanType"] in {"Detailed", "AutoScan"} and entry["BodyName"].find("Cluster") == -1:
                    if re.match("^[A-Za-z\s]+\s[A-Z]{2}-[A-Z]\s[abcdefgh]", entry["StarSystem"]) is not None:
                        united_log_file.write(line)
                elif entry["event"] == "FSSAllBodiesFound":
                    if re.match("^[A-Za-z\s]+\s[A-Z]{2}-[A-Z]\s[abcdefgh]", entry["SystemName"]) is not None:
                        united_log_file.write(line)
            log_file.close()

    united_log_file.close()
    return cmdr

def read_local_strangers_logs(path_to_logs: str, local_cmdr: str):
    try:
        os.mkdir("LOGFILES")
    except FileExistsError:
        pass

    for filename in os.listdir("LOGFILES"):
        if filename != f"{local_cmdr}.log":
            os.remove(os.path.join("LOGFILES", filename))

    for filename in os.listdir(path_to_logs):
        if filename.find(".log") != -1:
            log_file = open(os.path.join(path_to_logs, filename), encoding="utf-8")
            for line in log_file:
                entry = json.loads(line)
                if entry["event"] == "Commander":
                    cmdr_log_file = open(f"LOGFILES\\{entry['Name']}.log", "a", encoding="utf-8")
                    continue
                if entry["event"] == "Scan" and entry["ScanType"] in {"Detailed", "AutoScan"} and entry["BodyName"].find("Cluster") == -1:
                    if re.match("^[A-Za-z\s]+\s[A-Z]{2}-[A-Z]\s[abcdefgh]", entry["StarSystem"]) is not None:
                        cmdr_log_file.write(line)
                elif entry["event"] == "FSSAllBodiesFound":
                    if re.match("^[A-Za-z\s]+\s[A-Z]{2}-[A-Z]\s[abcdefgh]", entry["SystemName"]) is not None:
                        cmdr_log_file.write(line)
            log_file.close()
            try:
                cmdr_log_file.close()
            except UnboundLocalError:
                pass

def check_if_cmdr_was_in_boxel(cmdr: str, boxel: str) -> bool:
    log_file = open(os.path.join("LOGFILES", f"{cmdr}.log"), encoding="utf-8")
    for line in log_file:
        entry = json.loads(line)
        if entry["event"] == "Scan" and entry["StarSystem"].find(boxel) != -1:
            return True
    return False

def how_many_cmdrs_were_in_boxel(boxel: str, local_cmdr: str) -> int:
    result = 0
    for filename in os.listdir("LOGFILES"):
        if filename[:-4] == local_cmdr:
            continue
        if check_if_cmdr_was_in_boxel(filename[:-4], boxel):
            result += 1
    return result

def unite_logs(boxel: str) -> (str, str):
    body_count = {
        "visited": 0,
        "min sys": 0,
        "bodies": 0,
        "ELW": 0,
        "AW": 0,
        "WW": 0,
        "HMC": 0,
        "RB": 0,
        "MR": 0,
        "WG": 0,
        "GGWL": 0,
        "GGAL": 0,
        "GG1": 0,
        "GG2": 0,
        "GG3": 0,
        "GG4": 0,
        "GG5": 0,
        "HRGG": 0,
        "IB": 0
    }
    boxel_stats = {
        "visited": 0,
        "full scan": 0,
        "min total sys": 0,
        "body count": 0,
        "body avg": 0,
        "ELWs": 0,
        "ELW avg": "",
        "AWs": 0,
        "AW avg": "",
        "TFWWs": 0,
        "TFWW avg": "",
        "TFHMCs": 0,
        "TFHMC avg": "",
        "Min HE": 100.0,
        "Max HE": 0.0
    }

    unique_systems = []
    unique_full_scanned_systems = []
    unique_bodies = []
    for filename in os.listdir("LOGFILES"):
        log_file = open(os.path.join("LOGFILES", filename), "r", encoding="utf-8")
        for line in log_file:
            entry = json.loads(line)
            if "SystemName" in entry and entry["SystemName"].find(boxel) == -1:
                continue
            if "StarSystem" in entry and entry["StarSystem"].find(boxel) == -1:
                continue
            if "SystemName" in entry and entry["SystemName"] in unique_full_scanned_systems:
                continue
            if "StarSystem" in entry and entry["StarSystem"] in unique_full_scanned_systems:
                continue
            if entry["event"] == "FSSAllBodiesFound":
                boxel_stats["full scan"] += 1
                unique_full_scanned_systems.append(entry["SystemName"])
            elif entry["event"] == "Scan":
                if entry["StarSystem"] not in unique_systems:
                    unique_systems.append(entry["StarSystem"])
                    body_count["visited"] += 1
                    boxel_stats["visited"] += 1
                if entry["BodyName"] in unique_bodies:
                    continue
                else:
                    unique_bodies.append("BodyName")
                body_count["bodies"] += 1
                boxel_stats["body count"] += 1
                if "PlanetClass" in entry:
                    body_type = entry["PlanetClass"]
                    match body_type:
                        case "Earthlike body":
                            body_count["ELW"] += 1
                            boxel_stats["ELWs"] += 1
                        case "Ammonia world":
                            body_count["AW"] += 1
                            boxel_stats["AWs"] += 1
                        case "Water world":
                            body_count["WW"] += 1
                            if entry["TerraformState"] == "Terraformable":
                                boxel_stats["TFWWs"] += 1
                        case "High metal content body":
                            body_count["HMC"] += 1
                            if entry["TerraformState"] == "Terraformable":
                                boxel_stats["TFHMCs"] += 1
                        case "Rocky body":
                            body_count["RB"] += 1
                        case "Metal rich body":
                            body_count["MR"] += 1
                        case "Water giant":
                            body_count["WG"] += 1
                        case "Gas giant with water based life":
                            body_count["GGWL"] += 1
                        case "Gas giant with ammonia based life":
                            body_count["GGAL"] += 1
                        case "Sudarsky class I gas giant":
                            body_count["GG1"] += 1
                        case "Sudarsky class II gas giant":
                            body_count["GG2"] += 1
                        case "Sudarsky class III gas giant":
                            body_count["GG3"] += 1
                        case "Sudarsky class IV gas giant":
                            body_count["GG4"] += 1
                        case "Sudarsky class V gas giant":
                            body_count["GG5"] += 1
                        case "Helium rich gas giant":
                            body_count["HRGG"] += 1
                        case "Icy body":
                            body_count["IB"] += 1
                    if "Sudarsky" in entry["PlanetClass"]:
                        he = 0.0
                        for element in entry.get("AtmosphereComposition", []):
                            if element["Name"] == "Helium":
                                he = element["Percent"]
                        if he > boxel_stats["Max HE"]:
                            boxel_stats["Max HE"] = he
                        if he < boxel_stats["Min HE"]:
                            boxel_stats["Min HE"] = he
        
    boxel_stats["body avg"] = boxel_stats["body count"] / boxel_stats["visited"]
    if boxel_stats["ELWs"] != 0:
        boxel_stats["ELW avg"] = "1 in " + str(round(boxel_stats["visited"] / boxel_stats["ELWs"], 2))
    else:
        boxel_stats["ELW avg"] = "-"
    if boxel_stats["AWs"] != 0:
        boxel_stats["AW avg"] = "1 in " + str(round(boxel_stats["visited"] / boxel_stats["AWs"], 2))
    else:
        boxel_stats["AW avg"] = "-"
    if boxel_stats["TFWWs"] != 0:
        boxel_stats["TFWW avg"] = "1 in " + str(round(boxel_stats["visited"] / boxel_stats["TFWWs"], 2))
    else:
        boxel_stats["TFWW avg"] = "-"
    if boxel_stats["TFHMCs"] != 0:
        boxel_stats["TFHMC avg"] = "1 in " + str(round(boxel_stats["visited"] / boxel_stats["TFHMCs"], 2))
    else:
        boxel_stats["TFHMC avg"] = "-"

    max_system = 0
    for system in unique_systems:
        number = int(system[system.rfind('-')+1:])
        if number > max_system:
            max_system = number
    body_count["min sys"] = max_system + 1
    boxel_stats["min total sys"] = max_system + 1

    for key, value in body_count.items():
        if type(value) is float:
            body_count[key] = round(value, 3)
    for key, value in boxel_stats.items():
        if type(value) is float:
            boxel_stats[key] = round(value, 3)

    body_count_string = f"{boxel}xx"
    for _, value in body_count.items():
        body_count_string += f"\t{value}"
    boxel_stats_string = f"{boxel}xx"
    for _, value in boxel_stats.items():
        boxel_stats_string += f"\t{value}"

    return (body_count_string, boxel_stats_string)