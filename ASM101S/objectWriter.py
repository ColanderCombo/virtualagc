#!/usr/bin/env python3
'''
License:    This program is declared by its author to be the U.S. Public Domain,
            and may be freely used, modified, or distributed for any purpose.
Filename:   objectWriter.py
Purpose:    Emit IBM object module format
Reference:  http://bitsavers.informatik.uni-stuttgart.de/pdf/ibm/360/os/R01-08/C28-6538-3_Linkage_Editor_Oct66.pdf
'''

from asciiToEbcdic import asciiToEbcdic

def toEbcdic(s, length=8):
    return bytearray(
        asciiToEbcdic[ord(s[i])] if i < len(s) and ord(s[i]) < 128 else 0x40
        for i in range(length)
    )

def be16(val): return val.to_bytes(2, 'big')
def be24(val): return val.to_bytes(3, 'big')

def makeCard(recType, data, seqNum):
    card = bytearray(80)
    card[0] = 0x02
    card[1:4] = toEbcdic(recType, 3)
    card[4:4+min(len(data), 68)] = data[:68]
    card[72:80] = toEbcdic(f"{seqNum % 100000000:08d}", 8)
    return card

def writeESD(f, esdItems, seqNum):
    """Write ESD (External Symbol Dictionary) records. Up to 3 items per card."""
    items = list(esdItems)
    for i in range(0, len(items), 3):
        batch = items[i:i+3]
        
        data = bytearray(68)
        data[6:8] = be16(len(batch) * 16)
        data[10:12] = be16(batch[0]['esdId'])
        
        for j, item in enumerate(batch):
            o = 12 + j * 16
            data[o:o+8] = toEbcdic(item['name'], 8)
            data[o+8] = item['typeCode']
            data[o+9:o+12] = be24(item.get('address', 0))
            data[o+12] = item.get('flags', 0)
            data[o+13:o+16] = be24(item.get('length', 0))
        
        f.write(makeCard("ESD", data, seqNum))
        seqNum += 1
    
    return seqNum

def writeTXT(f, esdId, address, data, seqNum):
    """Write TXT records. Up to 56 bytes of object code per card."""
    for offset in range(0, len(data), 56):
        chunk = data[offset:offset+56]
        
        cardData = bytearray(68)
        cardData[1:4] = be24(address + offset)
        cardData[6:8] = be16(len(chunk))
        cardData[10:12] = be16(esdId)
        cardData[12:12+len(chunk)] = chunk
        
        f.write(makeCard("TXT", cardData, seqNum))
        seqNum += 1
    
    return seqNum

def writeRLD(f, relocations, seqNum):
    """Write RLD (Relocation Dictionary) records. Up to 7 entries per card."""
    if not relocations:
        return seqNum
    
    for i in range(0, len(relocations), 7):
        batch = relocations[i:i+7]
        
        cardData = bytearray(68)
        cardData[6:8] = be16(len(batch) * 8)
        
        for j, reloc in enumerate(batch):
            o = 12 + j * 8
            cardData[o:o+2] = be16(reloc['relId'])
            cardData[o+2:o+4] = be16(reloc['posId'])
            cardData[o+4] = reloc.get('flags', 0)
            cardData[o+5:o+8] = be24(reloc['address'])
        
        f.write(makeCard("RLD", cardData, seqNum))
        seqNum += 1
    
    return seqNum

def writeEND(f, entryEsdId=None, entryAddr=None, ident="ASM101S", seqNum=1):
    """Write END record with optional entry point and assembler identification."""
    cardData = bytearray(68)
    cardData[1:4] = be24(entryAddr) if entryAddr is not None else b'\x40\x40\x40'
    if entryEsdId is not None:
        cardData[10:12] = be16(entryEsdId)
    cardData[28:68] = toEbcdic(ident, 40)
    f.write(makeCard("END", cardData, seqNum))
    return seqNum + 1


def writeObjectModule(filename, metadata, symtab, sects, entries, extrns):
    esdItems, esdIdMap, nextEsdId = [], {}, 1
    
    # Section Definitions (SD) for CSECTs
    for sectName, sectData in sects.items():
        if sectData.get('dsect'):
            continue
        esdIdMap[sectName] = nextEsdId
        esdItems.append({
            'esdId': nextEsdId,
            'name': sectName or '#MAIN',
            'typeCode': 0x00,  # SD
            'address': 0,
            'flags': 0x00,
            'length': sectData.get('used', 0)
        })
        nextEsdId += 1
    
    # Entry points (LD)
    for entryName in entries:
        if (sym := symtab.get(entryName)):
            esdIdMap[entryName] = nextEsdId
            esdItems.append({
                'esdId': nextEsdId,
                'name': entryName,
                'typeCode': 0x01,  # LD
                'address': sym.get('address', 0) * 2,  # halfword -> byte
                'flags': 0x00,
                'length': 0
            })
            nextEsdId += 1
    
    # External References (ER)
    for extName in extrns:
        esdIdMap[extName] = nextEsdId
        esdItems.append({
            'esdId': nextEsdId,
            'name': extName,
            'typeCode': 0x02,  # ER
            'address': 0,
            'flags': 0x00,
            'length': 0
        })
        nextEsdId += 1
    
    # Build RLD entries
    rldEntries = [
        {'relId': esdIdMap[r['symbol']], 'posId': esdIdMap[r['section']],
         'flags': 0x1C, 'address': r.get('address', 0)}  # 0x1C = 4-byte address constant
        for r in metadata.get('relocations', [])
        if r.get('symbol') in esdIdMap and r.get('section') in esdIdMap
    ]
    
    with open(filename, 'wb') as f:
        seqNum = 1
        
        if esdItems:
            seqNum = writeESD(f, esdItems, seqNum)
        
        for sectName, sectData in sects.items():
            if sectData.get('dsect'):
                continue
            if (used := sectData.get('used', 0)) > 0:
                memory = sectData.get('memory', bytearray())
                seqNum = writeTXT(f, esdIdMap.get(sectName, 1), 0, bytes(memory[:used]), seqNum)
        
        if rldEntries:
            seqNum = writeRLD(f, rldEntries, seqNum)
        
        entryEsdId, entryAddr = None, None
        if entries and (firstName := next(iter(entries))) and (sym := symtab.get(firstName)):
            entryEsdId = esdIdMap.get(sym.get('section', ''), 1)
            entryAddr = sym.get('address', 0) * 2
        
        writeEND(f, entryEsdId, entryAddr, "ASM101S 0.00", seqNum)
    
    return filename
