# pttllm : Push To Talk Large Language Model

This program provides a ham radio voice interface to a LLM.

## Setup

You will need the following hardware:

 * [Digirig Mobile](https://digirig.net/product/digirig-mobile) or [Digirig Lite](https://digirig.net/product/digirig-lite/)
 * Two handheld radios
   * Tested with two Baofeng AR-5RM.
 * A Linux PC.
 * Access to an OpenAI compatible LLM API.
   * Tested with [LM Studio](https://lmstudio.ai/)

## Configure Radios

You can configure the radios using the [chirp-next](https://chirpmyradio.com/projects/chirp/wiki/Download) software.

You need to find a clear frequency to use for your station and then
program it into both radios. 

For testing purposes, configure the radios for the lowest power
setting and range:

 * Use the shortest "duck" type antenna.
 * Use the 70cm (UHF) band. UHF has good wall penetration, but a
   pretty short range overall.
   * For amateur radio, [consult the ARRL band plan](https://www.arrl.org/images/view/Charts/Band_Chart_Image_for_ARRL_Web.jpg)
   * All licenced amateurs may use the 70cm band, with frequencies
     420.0MHz <-> 450.0MHz.
   * For this example, we will use the frequency `423.107500`.
 * On the Baofeng, set the power level to "Low".
 * Set a CTCSS tone to activate the LLM station, this is to reject
   unrelated transmissions not directed toward the LLM.
   * For this example, we will use the tone `179.9`.
 
Once you have found a clear frequency, you need to program two
channels into the CHIRP software:

 * Channel 1:
   * Frequency: `423.107500`
   * Name: `My LLM`
   * Tone Mode: `Tone`
   * Tone: `179.9`
   * Mode: `FM`
   * Power: `Low`
   
 * Channel 2:
   * Frequency: `423.107500`
   * Name: `LLM RECV`
   * Tone Mode: `TSQL`
   * Tone Squelch: `179.9`
   * Mode: `FM`
   * Power: `Low`
   
Save the file and program it into both radios using the programming
cable that came with your radios:

 * Go to `Radio` -> `Upload to Radio`.
 * Choose your USB port (e.g. `ttyUSB0`) (confirm the correct port via
   `dmesg` when you plug the cable in)
 * Select the radio vendor and model (e.g. `Baofeng` and `5RM`.)
 * Click `OK` to program the radio.
 * Do this for both radios. 

One of the radios will be your LLM base station connected to the PC,
and the other radio is your personal portable radio.

 * Set the LLM station radio to the channel `LLM RECV`. It will only
   open the squelch for transmissions with the correct CTCSS tone.
 * Set the other radio to the channel `My LLM`, this radio will
   transmit the tone so the LLM will respond, but it will also listen
   for all other traffic on the same frequency.

Plug the digirig cable into the base station radio and connect it to
the PC.

You need to find the ALSA name of the digirig sound device. Once you
have `pttllm` installed, you can run `pttllm list-devices` to find it.
In my case, the digirig is named `USB PnP Sound Device: Audio
(hw:3,0)`. This is the ALSA name, not the JACK name. Do not use the
JACK device.

Install the dependencies and follow the `Development` guide below. For
now, there are no prebuilt packages.

## Dependencies

 * Python 3.11
 * FFMpeg
 * llvm 10.0 (required by
   [openai-whisper](https://pypi.org/project/openai-whisper/))

## Development

On Arch linux, install
[python311](https://aur.archlinux.org/packages/python311) and
[llvm10](https://aur.archlinux.org/packages/llvm10) from AUR:

```
yay -S python311 llvm10
export LLVM_CONFIG=/opt/llvm10/bin/llvm-config 
```

Clone and setup project:

```
git clone https://github.com/EnigmaCurry/pttllm.git \
  ~/git/vendor/enigmacurry/pttllm
cd ~/git/vendor/enigmacurry/pttllm

poetry env use python3.11
poetry install

# Maybe put this in ~/.bashrc
alias pttllm="poetry -P ~/git/vendor/enigmacurry/pttllm run pttllm"
```

## Configure the .env file

Included in the source is a config file named `.env-dist`. Copy this
file to another name (e.g. `.env`) and edit it.

 * Make sure to enter your radio callsign `PTTLLM_CALLSIGN`.
 * The `PTTLLM_BASE_URL` is preconfigured for LM studio running on the
   same PC, but you can enter any OpenAI compatible endpoint.
 * Make sure to enter the correct `PTTLLM_INPUT` and `PTTLLM_OUTPUT`
   for your digirig sound device.

## Start the station receiver

```
pttllm --dotenv .env station
```

## Test it

The base station should now be listening for transmission (that carry
the correct CTCSS tone). Transmit your query to the LLM using the
portable radio, and the LLM should respond.
