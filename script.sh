gnome-terminal -- bash -c "source /opt/ros/noetic/setup.bash; roslaunch rosbridge_server rosbridge_websocket.launch; exec bash";
cd middleware;
clear;
python3 fault_engine.py
