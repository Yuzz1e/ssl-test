"""
Script to receive robot coordinate data from SSL-Vision
Receives data from multicast address 224.5.23.2:10006
"""
import socket
import struct
import sys
import os

# Add generated folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))

from ssl_vision_wrapper_pb2 import SSL_WrapperPacket


def create_multicast_socket(multicast_group: str, port: int) -> socket.socket:
    """Create a socket for multicast reception"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # On Windows, bind to empty string
    sock.bind(("", port))
    
    # Join multicast group
    mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    return sock


def print_detection_frame(detection):
    """Print detection frame information"""
    print(f"\n=== Frame {detection.frame_number} (Camera {detection.camera_id}) ===")
    
    # Ball information
    if detection.balls:
        print("\n[Ball]")
        for i, ball in enumerate(detection.balls):
            print(f"  Ball{i}: x={ball.x:.1f}mm, y={ball.y:.1f}mm", end="")
            if ball.HasField("z"):
                print(f", z={ball.z:.1f}mm", end="")
            print(f" (confidence: {ball.confidence:.2f})")
    
    # Blue team robots
    if detection.robots_blue:
        print("\n[Blue Team]")
        for robot in detection.robots_blue:
            robot_id = robot.robot_id if robot.HasField("robot_id") else "?"
            orientation = f"{robot.orientation:.2f}rad" if robot.HasField("orientation") else "unknown"
            print(f"  ID {robot_id}: x={robot.x:.1f}mm, y={robot.y:.1f}mm, orientation={orientation} (confidence: {robot.confidence:.2f})")
    
    # Yellow team robots
    if detection.robots_yellow:
        print("\n[Yellow Team]")
        for robot in detection.robots_yellow:
            robot_id = robot.robot_id if robot.HasField("robot_id") else "?"
            orientation = f"{robot.orientation:.2f}rad" if robot.HasField("orientation") else "unknown"
            print(f"  ID {robot_id}: x={robot.x:.1f}mm, y={robot.y:.1f}mm, orientation={orientation} (confidence: {robot.confidence:.2f})")


def main():
    # SSL-Vision multicast address
    MULTICAST_GROUP = "224.5.23.2"
    PORT = 10006
    
    print("Receiving SSL-Vision data...")
    print(f"Multicast address: {MULTICAST_GROUP}:{PORT}")
    print("Press Ctrl+C to exit")
    print()
    
    try:
        sock = create_multicast_socket(MULTICAST_GROUP, PORT)
        sock.settimeout(5.0)  # 5 second timeout
        
        while True:
            try:
                data, addr = sock.recvfrom(65535)
                
                # Parse packet
                packet = SSL_WrapperPacket()
                packet.ParseFromString(data)
                
                # Print if detection frame is present
                if packet.HasField("detection"):
                    print_detection_frame(packet.detection)
                
                # Geometry information (print only once)
                if packet.HasField("geometry"):
                    field = packet.geometry.field
                    print("\n[Field Info]")
                    print(f"  Size: {field.field_length}mm x {field.field_width}mm")
                    print(f"  Goal: {field.goal_width}mm x {field.goal_depth}mm")
                    
            except socket.timeout:
                print("Waiting for data... (timeout)")
                continue
                
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
