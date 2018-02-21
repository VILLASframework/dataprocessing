import re

def readsim(file_name,timeseries_names=None, is_regex=False):
    str_tmp = open(file_name,"r")
    low = 0
    high = 0
    flag = True
    dic = {}
    seq = []
    value = []
    i = 0
    isfloat = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    for line in str_tmp.readlines():
        line = line.replace(",",".")
        high -= high
        low -= low
        del value[:]
        for letter in line:
            if letter == "	" or letter == "\n":  # different data or end
                if low is not high:  # not NONE
                    if flag:  # seq
                        seq.append(line[low:high])
                    else:  # value
                        if isfloat.match(line[low:high]):
                            value.append(float(line[low:high]))
                        else:
                            value.append(line[low:high])
                else:  # NONE
                    value.append(r'#')
                low = high + 1
            high += 1
        flag = False
        dic[i] = dict(zip(seq, value))
        i += 1
    str_tmp.close()
    return dic