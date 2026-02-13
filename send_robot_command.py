"""
grSim에 로봇 명령을 전송하는 스크립트
로봇을 전후좌우로 움직이는 샘플
"""
import socket
import time
import math
import sys
import os

# generated 폴더를 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))

from grSim_Packet_pb2 import grSim_Packet
from grSim_Commands_pb2 import grSim_Commands, grSim_Robot_Command


def create_robot_command(
    robot_id: int,
    veltangent: float = 0.0,  # 전후 방향 속도 (m/s)
    velnormal: float = 0.0,   # 좌우 방향 속도 (m/s)
    velangular: float = 0.0,  # 회전 속도 (rad/s)
    kickspeedx: float = 0.0,  # 킥 속도 X
    kickspeedz: float = 0.0,  # 킥 속도 Z (칩 킥용)
    spinner: bool = False,    # 드리블 ON/OFF
) -> grSim_Robot_Command:
    """로봇 명령 생성"""
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
    """grSim에 명령 전송"""
    packet = grSim_Packet()
    packet.commands.timestamp = time.time()
    packet.commands.isteamyellow = is_yellow
    
    for cmd in robot_commands:
        packet.commands.robot_commands.append(cmd)
    
    data = packet.SerializeToString()
    sock.sendto(data, address)


def main():
    # grSim 전송 주소
    GRSIM_ADDRESS = ("127.0.0.1", 20011)
    
    # UDP 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("grSim에 로봇 명령을 전송합니다...")
    print(f"전송 대상: {GRSIM_ADDRESS}")
    print("Ctrl+C로 종료")
    print()
    
    try:
        # 로봇 ID 0을 움직이는 데모
        robot_id = 0
        is_yellow = False  # 파란 팀
        
        # 패턴 1: 전진
        print("전진 중...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, veltangent=1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)  # 약 60Hz
        
        # 패턴 2: 정지
        print("정지...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # 패턴 3: 후진
        print("후진 중...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, veltangent=-1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # 패턴 4: 정지
        print("정지...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # 패턴 5: 좌측 이동
        print("좌측 이동 중...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, velnormal=1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # 패턴 6: 정지
        print("정지...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # 패턴 7: 우측 이동
        print("우측 이동 중...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, velnormal=-1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # 패턴 8: 정지
        print("정지...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # 패턴 9: 회전
        print("회전 중...")
        for _ in range(100):
            cmd = create_robot_command(robot_id, velangular=3.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # 최종 정지
        print("정지...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        print("데모 완료!")
        
    except KeyboardInterrupt:
        print("\n종료합니다...")
    finally:
        # 정지 명령 전송
        cmd = create_robot_command(robot_id)
        send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
        sock.close()


if __name__ == "__main__":
    main()
