if [ -v ZSH_VERSION ]
then
    # Assume that this script is executed by zsh
    THIS_DIRECTORY=${0:a:h}
else
    # Assume that this script is executed by bash
    THIS_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"
fi

VENV_DIRECTORY="${THIS_DIRECTORY}/.venv"

source "${VENV_DIRECTORY}/bin/activate"

PYTHONPATH="${THIS_DIRECTORY}:${PYTHONPATH}"
export PYTHONPATH



# ZSH caches the location of executables. `hash -r` forces it to discard the
# cache so that executables in this venv will be found.
hash -r