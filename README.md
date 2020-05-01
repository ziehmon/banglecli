# banglecli

## Introduction

I use my [Bangle.js](https://banglejs.com/) as general input / output device, not only for typical "smartwatch use-cases". This repository collects CLI-based tools to interact with a Bangle.js over Bluetooth Low Energy I've written. Currently, `banglebang` is the only one.

## Tool Overview

## banglebang

Ever ran a `wget` in background, switched to your browser, and then forgot that you were downloading something at all? Or hate switching windows just to check if it's finished? This has come to an end with banglebang. It will take input from stdin (e.g by using a pipe, | ) and display it as notification on your Bangle.js. 

`curl -s https://example.com/file.zip | banglebang`

If there is no message specified by stdin, the Bangle.js will display "* BAM *". Please also notify that banglebang will only parse the first line of stdin, so you should filter (e.g by using an intermediate `grep`)

### Requirements

- A working bluetooth low energy stack (e.g. BlueZ) as described in the [Espruino Wiki](https://www.espruino.com/Quick+Start+BLE) 
    - Rule of thumb: if you can use the [Espruino Web IDE](https://www.espruino.com/ide/), you can use banglecli tools without any problems!
- A working Python 3 installation in `#!/usr/bin/python3`, also a working pip3 to install the bluetooth library

### Installation

By executing `setup.sh`, banglecli will be installed to /usr/local/bin and it's executables under /apps like `banglebang` will be symlinked to `/usr/local/bin/$appname` so you can easily call them by `bangleapps`. 

**The install script needs root permissions to run**, due to  `/usr/local/bin/` permissions and because BLE access requires a kernel capability that will be set during the install (`cap_net_raw,cap_net_admin+eip`); Please review the script before executing with `sudo setup.sh`.

### Setup

The only additional required step is to set the `BCLI_MAC` environment variable to your Bangle.js's MAC address. It should be very easy to find out by running `sudo hcitool lescan`. I suggest setting this in your shell's .rc file (e.g `.bashrc`)

### Configuration

Besides the already mentioned environment variable `BCLI_MAC`, there are some more configuration variables. See this table.

| Name         | Description                                           | Default            |
|--------------|-------------------------------------------------------|--------------------|
| BCLI_MAC     | MAC address of the Bangle.js to connect to            | **[Required]**     |
| BCLI_RETRIES | Number of retries when connecting to Bangle.js        | 3                  |
| BCLI_SOURCE  | Source that will be used for notifications            | "bcli"             |
| BCLI_TITLE   | Title that will be used for notifications             | [Command Output]   |
| BCLI_MSG     | Fallback message when no input from stdin is detected | "Command finished" |

### Contribution

I tried maintain a certain level of modularity and put the generic functions into bcli.py. If you want to write a new banglecli tool, you can start by importing this file. Connection setup can be copied from banglebang. Don't get confused by BTLE Characteristics, just get the TX and RX objects and write to them. Also, never forget to send your messages through packByteArray since send BLE packet size limit is 20 bytes, at least for the Nordic Semiconductor chip the Bangle is using.

