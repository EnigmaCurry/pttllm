# pttllm : Push To Talk Large Language Model

This program provides a ham radio voice interface to a LLM.

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
