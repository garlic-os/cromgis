shopt -s nullglob

function log() {
    echo "-----> $*"
}

if [ -z "${PYTHON_RUNTIME_VERSION:-}" ] ; then
    log "Read Python version from poetry.lock"
    PYTHON_RUNTIME_VERSION="$(sed -n -e '/^\[metadata\]/,/^\[/p' poetry.lock | sed -n -e 's/^python-versions\s*=\s*//p' | tr -d \"\')"
    log "$PYTHON_RUNTIME_VERSION"
else
    log "Force Python version to $PYTHON_RUNTIME_VERSION, because PYTHON_RUNTIME_VERSION is set!"
fi

#if [[ "$PYTHON_RUNTIME_VERSION" =~ ^[2-9](\.[0-9]+){2}$ ]] ; then
    log "Write $PYTHON_RUNTIME_VERSION into $RUNTIME_FILE"
    echo "python-$PYTHON_RUNTIME_VERSION" > "$RUNTIME_FILE"
#else
#    log "$PYTHON_RUNTIME_VERSION is not valid. Please specify an exact Python version (e.g. 3.8.13) in your pyproject.toml (and thus poetry.lock)." >&2
#    exit 1
#fi
