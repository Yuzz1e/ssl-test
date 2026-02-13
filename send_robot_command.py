"""
Script to send robot commands to grSim
Sample to move a robot forward, backward, left, and right
"""
import socket
import time
import math
import sys
import os

# Add generated folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))

from grSim_Packet_pb2 import grSim_Packet
from grSim_Commands_pb2 import grSim_Commands, grSim_Robot_Command


def create_robot_command(
    robot_id: int,
    veltangent: float = 0.0,  # Forward/backward velocity (m/s)
    velnormal: float = 0.0,   # Left/right velocity (m/s)
    velangular: float = 0.0,  # Angular velocity (rad/s)
    kickspeedx: float = 0.0,  # Kick speed X
    kickspeedz: float = 0.0,  # Kick speed Z (for chip kick)
    spinner: bool = False,    # Dribbler ON/OFF
) -> grSim_Robot_Command:
    """Create a robot command"""
    cmd = grSim_Robot_Command()
    cmd.id = robot_id
    cmd.kickspeedx = kickspeedx
    cmd.kickspeedz = kickspeedz
    cmd.veltangent = veltangent
    cmd.velnormal = velnormal
    cmd.velangular = velangular
    cmd.spinner = spinner
    cmd.wheelsspeed = False
    return cmd


def send_command(
    sock: socket.socket,
    address: tuple,
    robot_commands: list,
    is_yellow: bool = False,
):
    """Send command to grSim"""
    packet = grSim_Packet()
    packet.commands.timestamp = time.time()
    packet.commands.isteamyellow = is_yellow
    
    for cmd in robot_commands:
        packet.commands.robot_commands.append(cmd)
    
    data = packet.SerializeToString()
    sock.sendto(data, address)


def main():
    # grSim destination address
    GRSIM_ADDRESS = ("127.0.0.1", 20011)
    
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("Sending robot commands to grSim...")
    print(f"Destination: {GRSIM_ADDRESS}")
    print("Press Ctrl+C to exit")
    print()
    
    try:
        # Demo: move robot ID 0
        robot_id = 0
        is_yellow = False  # Blue team
        
        # Pattern 1: Move forward
        print("Moving forward...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, veltangent=1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)  # ~60Hz
        
        # Pattern 2: Stop
        print("Stopping...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # Pattern 3: Move backward
        print("Moving backward...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, veltangent=-1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # Pattern 4: Stop
        print("Stopping...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # Pattern 5: Move left
        print("Moving left...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, velnormal=1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # Pattern 6: Stop
        print("Stopping...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # Pattern 7: Move right
        print("Moving right...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, velnormal=-1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # Pattern 8: Stop
        print("Stopping...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # Pattern 9: Rotate
        print("Rotating...")
        for _ in range(100):
            cmd = create_robot_command(robot_id, velangular=3.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # Final stop
        print("Stopping...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        print("Demo complete!")
        
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Send stop command
        cmd = create_robot_command(robot_id)
        send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
        sock.close()


if __name__ == "__main__":
    main()
