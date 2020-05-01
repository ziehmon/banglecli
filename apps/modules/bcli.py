#!/usr/bin/python3

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
