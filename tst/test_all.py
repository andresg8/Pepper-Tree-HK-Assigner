import os
os.chdir("../src")
import sys
sys.path.insert(1, "../src")
from hk_pdf_processor import *
import tika
from tika import parser

def test_all():
    houseKeepers = [HouseKeeper("Judith", today, 0),
                    HouseKeeper("Maribel", today, 0),
                    HouseKeeper("Lesbia", today, 0),
                    HouseKeeper("Adriana", today, 0),
                    HouseKeeper("Vanessa", today, 0)]
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
    roomTypes = ["KING","QQ","CK","CQ", "ACK", "ACQ"]
    cleanTypes = ["Stay", "C/O"]
    rooms = []
    for line in relevantLines[:-1]:
        roomNumber = int(line[-3:])
        if "No Service" in line: continue
        if "Dirty" in line:
            roomType = [x for x in roomTypes if x in line]
            longStay = False
            arrival = False
            if "Yes" in line:
                arrival = True
            cleanType = ["C/O"]
            checkInDate = "07/12/1996"
            room = Room(roomNumber, roomType[0], cleanType[0], arrival, longStay, checkInDate)
            rooms.append(room)
        else:
            roomType = [x for x in roomTypes if x in line]
            cleanType = [x for x in cleanTypes if x in line]
            yesCounter = line.count("Yes")
            if yesCounter == 1:
                arrival = False
                longStay = True
            elif yesCounter == 2:
                arrival = True
                longStay = False
            else:
                arrival = False
                longStay = False
            checkInDate = line.split()[0]
            room = Room(roomNumber, roomType[0], cleanType[0], arrival, longStay, checkInDate)
            room.checkBlueness()
            rooms.append(room)
    towelTidies = []
    checkOuts = []
    for room in rooms:
        if (room.cleanType == "Stay"):
            towelTidies.append(room)
        else:
            checkOuts.append(room)
    numHK = len(houseKeepers)
    roomsPerHK = []
    for i in range(numHK):
        roomsPerHK.append([])
    coPerHK = smoothDivision(len(checkOuts), numHK)
    coPerHK.reverse()
    roomCounter = 0
    for hk in range(len(roomsPerHK)):
        for i in range(coPerHK[hk]):
            roomsPerHK[hk].append(checkOuts[roomCounter])
            roomCounter += 1
            if roomCounter > len(checkOuts):
                print("Partitioning Error!")
                break
    ttPerHK = smoothDivision(len(towelTidies), numHK)
    roomCounter = 0
    for hk in range(len(roomsPerHK)):
        for i in range(ttPerHK[hk]):
            roomsPerHK[hk].append(towelTidies[roomCounter])
            roomCounter += 1
            if roomCounter > len(towelTidies):
                print("Partitioning Error!")
                break
    true_cwd = os.getcwd()
    os.chdir("../")
    if os.getcwd().endswith("HK Assigner"):
        cwd = os.getcwd()
        for file in os.listdir(cwd):
            if file.endswith(".xlsx"):
                os.remove(file)
    os.chdir(true_cwd)

    yellowFill = PatternFill(start_color = '00FFFF00',
                                end_color = '00FFFF00',
                                fill_type = "solid")
    blueFill = PatternFill(start_color = '0037CBFF',
                                end_color = '0037CBFF',
                                fill_type = "solid")
    noFill = PatternFill(start_color = '00FFFFFF',
                                end_color = '00FFFFFF',
                                fill_type = "solid")
    i = 0
    for hk in roomsPerHK:
        name = houseKeepers[i].name
        wb = load_workbook("res/HK Template.xlsx")
        ws = wb["Sheet1"]
        aggregateRoomScore = 0
        ws["A1"] = name
        r = 3
        space_added = False
        for room in hk:
            tipo = room.cleanType
            if room.cleanType != "C/O": tipo = "TT"
            if tipo == "TT" and not space_added:
                r += 1
                space_added = True
            row = str(r)
            camas = room.roomType
            if room.roomType in ("CK", "ACK", "KING"): camas += " - 1"
            if room.roomType in ("CQ", "ACQ", "QQ"): camas += " - 2"
            ws["A" + row] = camas
            ws["B" + row] = room.roomNumber
            ws["C" + row] = tipo
            if tipo == "C/O" and room.arrival:
                ws["A" + row].fill = yellowFill
                ws["B" + row].fill = yellowFill
                ws["C" + row].fill = yellowFill
            if tipo == "TT" and room.longStay:
                ws["A" + row].fill = blueFill
                ws["B" + row].fill = blueFill
                ws["C" + row].fill = blueFill
            aggregateRoomScore += room.roomNumber
            r += 1
        i += 1
        wb.save("../" + name + ".xlsx")
        wb.close()
    wb = load_workbook('res/Pre-Room Check List.xlsx')
    ws = wb["Sheet1"]
    letters = "BCDEFGHIJKL" 
    i = 0
    l = 0
    pageNum = 1
    for hk in roomsPerHK:
        name = houseKeepers[i].name
        for room in hk:
            if room.cleanType == "C/O":
                ws[letters[l] + "2"] = room.roomNumber
                ws[letters[l] + "3"] = name[:3]
                if room.arrival:
                    ws[letters[l] + "2"].fill = yellowFill
                else:
                    ws[letters[l] + "2"].fill = noFill
                l += 1
                if (l > 10):
                    queuePrintJob(pageNum, ws, wb)
                    pageNum += 1
                    l = 0
        i += 1
    if l > 0:
        for i in range(l, 11):
            ws[letters[i] + "2"] = ""
            ws[letters[i] + "3"] = ""
            ws[letters[i] + "2"].fill = noFill
        queuePrintJob(pageNum, ws, wb)
    wb = load_workbook('res/Laundry Min.xlsx')
    wb.save('../Laundry Min.xlsx')
    wb.close()
    #AHK = AllHouseKeepers(allHouseKeepers)
    #pickle.dump(AHK, open("housekeepers.p", 'wb'))
    os.chdir("../")
    assert("Laundry Min.xlsx" in os.listdir())
    assert("Pre-Room Check List" + str(pageNum) + ".xlsx" in os.listdir())
    for hk in houseKeepers:
        assert(hk.name+".xlsx" in os.listdir())

    
