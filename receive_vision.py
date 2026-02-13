"""
SSL-Vision에서 로봇 좌표 정보를 수신하는 스크립트
멀티캐스트 주소 224.5.23.2:10006에서 데이터 수신
"""
import socket
import struct
import sys
import os

# generated 폴더를 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))

from ssl_vision_wrapper_pb2 import SSL_WrapperPacket


def create_multicast_socket(multicast_group: str, port: int) -> socket.socket:
    """멀티캐스트 수신용 소켓 생성"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Windows의 경우 빈 문자열에 바인드
    sock.bind(("", port))
    
    # 멀티캐스트 그룹 참가
    mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    return sock


def print_detection_frame(detection):
    """검출 프레임 정보 출력"""
    print(f"\n=== 프레임 {detection.frame_number} (카메라 {detection.camera_id}) ===")
    
    # 볼 정보
    if detection.balls:
        print("\n【볼】")
        for i, ball in enumerate(detection.balls):
            print(f"  볼{i}: x={ball.x:.1f}mm, y={ball.y:.1f}mm", end="")
            if ball.HasField("z"):
                print(f", z={ball.z:.1f}mm", end="")
            print(f" (신뢰도: {ball.confidence:.2f})")
    
    # 파란 팀 로봇
    if detection.robots_blue:
        print("\n【파란 팀】")
        for robot in detection.robots_blue:
            robot_id = robot.robot_id if robot.HasField("robot_id") else "?"
            orientation = f"{robot.orientation:.2f}rad" if robot.HasField("orientation") else "알 수 없음"
            print(f"  ID {robot_id}: x={robot.x:.1f}mm, y={robot.y:.1f}mm, 방향={orientation} (신뢰도: {robot.confidence:.2f})")
    
    # 노란 팀 로봇
    if detection.robots_yellow:
        print("\n【노란 팀】")
        for robot in detection.robots_yellow:
            robot_id = robot.robot_id if robot.HasField("robot_id") else "?"
            orientation = f"{robot.orientation:.2f}rad" if robot.HasField("orientation") else "알 수 없음"
            print(f"  ID {robot_id}: x={robot.x:.1f}mm, y={robot.y:.1f}mm, 방향={orientation} (신뢰도: {robot.confidence:.2f})")


def main():
    # SSL-Vision 멀티캐스트 주소
    MULTICAST_GROUP = "224.5.23.2"
    PORT = 10006
    
    print("SSL-Vision 데이터를 수신합니다...")
    print(f"멀티캐스트 주소: {MULTICAST_GROUP}:{PORT}")
    print("Ctrl+C로 종료")
    print()
    
    try:
        sock = create_multicast_socket(MULTICAST_GROUP, PORT)
        sock.settimeout(5.0)  # 5초 타임아웃
        
        while True:
            try:
                data, addr = sock.recvfrom(65535)
                
                # 패킷 파싱
                packet = SSL_WrapperPacket()
                packet.ParseFromString(data)
                
                # 검출 프레임이 있으면 출력
                if packet.HasField("detection"):
                    print_detection_frame(packet.detection)
                
                # 지오메트리 정보 (최초 1회만 출력)
                if packet.HasField("geometry"):
                    field = packet.geometry.field
                    print("\n【필드 정보】")
                    print(f"  크기: {field.field_length}mm x {field.field_width}mm")
                    print(f"  골: {field.goal_width}mm x {field.goal_depth}mm")
                    
            except socket.timeout:
                print("데이터 수신 대기 중... (타임아웃)")
                continue
                
    except KeyboardInterrupt:
        print("\n종료합니다...")
    except Exception as e:
        print(f"오류: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
