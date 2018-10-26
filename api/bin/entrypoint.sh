#!/bin/bash
set -eu

usage() {
    echo "Usage: entrypoint.sh COMMAND [ARGS]"
    echo ""
    echo "Commands:"
    echo "  flask               -- Invoke the flask binary"
    echo "  server              -- Start the DeaconViz server in production mode"
    echo "  dev_server          -- Start the DeaconViz server in development mode"
}

flaskcmd() {
    export FLASK_APP=snow.wsgi
    export FLASK_DEBUG=1

    flask "$@"
}

server() {
    gunicorn -b 0.0.0.0:5000 --name snow -w3 snow.wsgi:app
}

dev_server() {
    export FLASK_DEBUG=1

    flaskcmd run --host 0.0.0.0
}


[ $# -ge 1 ] || { usage; exit 1; }


COMMAND="$1"

case "$COMMAND" in
    server)
        server ;;
    flask)
        shift
        flaskcmd "$@" ;;
    dev_server)
        dev_server ;;
     *)
        echo "Unrecognized command: '$COMMAND'"
        usage
        exit 1 ;;
esac
