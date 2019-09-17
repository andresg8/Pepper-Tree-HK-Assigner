
import tika
from tika import parser

def test_tika_car():
    parsed = parser.from_file("../Custom Associates Report.pdf")
    rawText = parsed["content"]
    line = ""
    linedText = []
    for char in rawText:
        if char == '\n':
            if line: linedText.append(line)
            line = ""
        else:
            line += char
    i = 1
    relevantLines = []
    interestFlag = False
    for line in linedText:
        words = line.split()
        if words[0] in ["Custom", "Room"]: interestFlag = False
        if interestFlag:
            relevantLines.append(line)
            i+=1
        if words[-1] == "Remarks": interestFlag = True
    assert(i - 2 == int(relevantLines[-1][-3:]))
