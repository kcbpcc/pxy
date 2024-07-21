def compute_depth(row, bcedepth, bpedepth, ncedepth, npedepth):

    if "CE" in row['key'] and row['key'].startswith("BANK"):
        if bcedepth > 1:
            return max(row['tgtoptsma'], (9 - bcedepth))
        else:
            return 5
    elif "PE" in row['key'] and row['key'].startswith("BANK"):
        if bpedepth > 1:
            return max(row['tgtoptsma'], (9 - bpedepth))
        else:
            return 5
    elif "CE" in row['key'] and row['key'].startswith("NIFTY"):
        if ncedepth > 1:
            return max(row['tgtoptsma'], (9 - ncedepth))
        else:
            return 5
    elif "PE" in row['key'] and row['key'].startswith("NIFTY"):
        if npedepth > 1:
            return max(row['tgtoptsma'], (9 - npedepth))
        else:
            return 5
    else:
        return 5
