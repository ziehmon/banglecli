#!/usr/bin/python3

import logging
import json
import sys

from modules import bcli

if __name__ == "__main__":

    bcliSettings = bcli.handleEnv()

    if not bcliSettings:
        exit()

    commandOutput = bcli.handleStdin()

    if not commandOutput:
        commandOutput = bcliSettings["BCLI_MSG"]

    bangleJs = bcli.connectBangleJs(bcliSettings["BCLI_MAC"],
                                    bcliSettings["BCLI_RETRIES"])

    if not bangleJs:
        exit()

    bangleJsTxCharacteristic = bcli.getBangleJsTxCharacteristic(bangleJs)

    bangleJsRxCharacteristic = bcli.getBangleJsRxCharacteristic(bangleJs)

    msgJson = json.dumps({"t": "notify",
                          "id": "000001",
                          "src": bcliSettings["BCLI_SOURCE"],
                          "title": bcliSettings["BCLI_TITLE"],
                          "body": commandOutput
                          })

    msgJsonByteArray = bytearray("\x10GB(" + msgJson + ")\n", 'utf-8')

    packedMsgJsonByteArray = bcli.packByteArray(msgJsonByteArray)

    for packet in packedMsgJsonByteArray:
        bangleJsTxCharacteristic.write(packet)
