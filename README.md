# pttllm : Push To Talk Large Language Model

This program provides a ham radio voice interface to a LLM.

## Development

Development is currently using Python 3.11:

```
git clone https://github.com/EnigmaCurry/pttllm.git \
  ~/git/vendor/enigmacurry/pttllm
cd ~/git/vendor/enigmacurry/pttllm

poetry env use python3.11
poetry install

# Maybe put this in ~/.bashrc
alias pttllm="poetry -P ~/git/vendor/enigmacurry/pttllm run pttllm"
```
