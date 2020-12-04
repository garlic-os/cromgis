# nohup: keep running after logging out of the session
# setsid: group all the processes that spawn from this command together for easily killing them all later
# python3.7 main.py: start cromgis
# | ts '[time/date format]': timestamp every line of output
# &>> cromgis.log: redirect nohup's output to append to cromgis.log
# &: don't block the terminal while cromgis is running
nohup setsid python3.7 main.py | ts '[%Y-%m-%d %H:%M:%S]' &>> cromgis.log &

pid=$!

# Get the process group ID of the above command and store it in "./pgid"
echo $(ps -o pgid --no-headers $pid) > pgid
