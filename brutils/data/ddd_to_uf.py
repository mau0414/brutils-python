from collections import Counter

from .enums import UF

DDD_TO_UF = {
    11: UF.SP, 12: UF.SP, 13: UF.SP, 14: UF.SP, 15: UF.SP, 16: UF.SP, 17: UF.SP, 18: UF.SP, 19: UF.SP,
    21: UF.RJ, 22: UF.RJ, 24: UF.RJ,
    27: UF.ES, 28: UF.ES,
    31: UF.MG, 32: UF.MG, 33: UF.MG, 34: UF.MG, 35: UF.MG, 37: UF.MG, 38: UF.MG,
    41: UF.PR, 42: UF.PR, 43: UF.PR, 44: UF.PR, 45: UF.PR, 46: UF.PR,
    47: UF.SC, 48: UF.SC, 49: UF.SC,
    51: UF.RS, 53: UF.RS, 54: UF.RS, 55: UF.RS,
    61: UF.DF,
    62: UF.GO, 64: UF.GO,
    63: UF.TO,
    65: UF.MT, 66: UF.MT,
    67: UF.MS,
    68: UF.AC,
    69: UF.RO,
    71: UF.BA, 73: UF.BA, 74: UF.BA, 75: UF.BA, 77: UF.BA,
    79: UF.SE,
    81: UF.PE, 87: UF.PE,
    82: UF.AL,
    83: UF.PB,
    84: UF.RN,
    85: UF.CE, 88: UF.CE,
    86: UF.PI, 89: UF.PI,
    91: UF.PA, 93: UF.PA, 94: UF.PA,
    92: UF.AM, 97: UF.AM,
    95: UF.RR,
    96: UF.AP,
    98: UF.MA, 99: UF.MA,
}

UFS_WITH_SINGLE_DDD = {uf for uf, count in Counter(DDD_TO_UF.values()).items() if count == 1}
