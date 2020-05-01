#!/usr/bin/python3

# Copyright (C) 2020  Simon Peters

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
