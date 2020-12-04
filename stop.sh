# $(cat ./gid): read the id to kill from the "./pgid"
kill -TERM -$(cat ./pgid)
