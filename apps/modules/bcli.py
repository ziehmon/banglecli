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

# This file belongs to bcli

import bluepy
import os
import sys

# Constants for Bangle.js (same on every device!)
# runtime and dynamic variables are stored in bcliSettings
global bangleJsTxCharacteristicUuid
bangleJsTxCharacteristicUuid = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

global bangleJsRxCharacteristicUuid
bangleJsRxCharacteristicUuid = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"


def connectBangleJs(deviceAddr, maxRetries):
    maxRetriesCounter = 0

    while maxRetriesCounter <= int(maxRetries):
        try:
            bangleJs = bluepy.btle.Peripheral(deviceAddr=deviceAddr,
                                              addrType="random")
            return bangleJs
        except bluepy.btle.BTLEDisconnectError:
            print("Info: retrying connection - " + str(maxRetriesCounter+1) +
                  " / " + str(maxRetries))
            pass

        maxRetriesCounter += 1


def getBangleJsTxCharacteristic(bangleJs):

    bangleJsTxCharacteristic = list(bangleJs.getCharacteristics(
        uuid=bangleJsTxCharacteristicUuid))

    if len(bangleJsTxCharacteristic) is not 1:
        print("Error: characteristics error for tx handler: " +
              str(bangleJsTxCharacteristic))
        return False

    return bangleJsTxCharacteristic[0]


def getBangleJsRxCharacteristic(bangleJs):

    bangleJsRxCharacteristic = list(bangleJs.getCharacteristics(
        uuid=bangleJsRxCharacteristicUuid))

    if len(bangleJsRxCharacteristic) is not 1:
        print("Error: characteristics error for rx handler: " +
              str(bangleJsRxCharacteristic))
        return False

    return bangleJsRxCharacteristic[0]


def packByteArray(rawByteArray):

    i = 0
    packedByteArrayList = []

    while i < len(rawByteArray):
        length = len(rawByteArray)-i

        if length > 20:
            length = 20

        # BLE needs 20 Bytes Packages
        packedByteArray = bytearray(length)

        j = 0
        while j < length:
            packedByteArray[j] = rawByteArray[int(i+j)]
            j += 1

        packedByteArrayList.append(packedByteArray)

        i += 20

    return packedByteArrayList


def handleEnv():

    if os.environ.get("BCLI_MAC") is None:
        print("Error: required BCLI_MAC environment variable not found")
        return False

    # set bcli default values
    bcliSettings = {}
    bcliSettings["BCLI_RETRIES"] = 3
    bcliSettings["BCLI_SOURCE"] = "bcli"
    bcliSettings["BCLI_TITLE"] = "Command Output"
    bcliSettings["BCLI_MSG"] = "* BANGLE *"

    # overwrite defaults from environment
    environmentOverwrite = "BCLI_RETRIES", "BCLI_MAC",
    "BCLI_TITLE", "BCLI_SOURCE", "BCLI_MSG"

    for environment in environmentOverwrite:
        if os.environ.get(environment) is not None:
            bcliSettings[environment] = os.environ.get(environment)

    return bcliSettings


def handleStdin():

    stdinMsg = False

    for line in sys.stdin:
        stdinMsg = line

    return stdinMsg
