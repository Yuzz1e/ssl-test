"""
grSimにロボットコマンドを送信するスクリプト
ロボットを前後左右に動かすサンプル
"""
import socket
import time
import math
import sys
import os

# generatedフォルダをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))

from grSim_Packet_pb2 import grSim_Packet
from grSim_Commands_pb2 import grSim_Commands, grSim_Robot_Command


def create_robot_command(
    robot_id: int,
    veltangent: float = 0.0,  # 前後方向の速度 (m/s)
    velnormal: float = 0.0,   # 左右方向の速度 (m/s)
    velangular: float = 0.0,  # 回転速度 (rad/s)
    kickspeedx: float = 0.0,  # キック速度X
    kickspeedz: float = 0.0,  # キック速度Z (チップキック用)
    spinner: bool = False,    # ドリブラーON/OFF
) -> grSim_Robot_Command:
    """ロボットコマンドを作成"""
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
    """grSimにコマンドを送信"""
    packet = grSim_Packet()
    packet.commands.timestamp = time.time()
    packet.commands.isteamyellow = is_yellow
    
    for cmd in robot_commands:
        packet.commands.robot_commands.append(cmd)
    
    data = packet.SerializeToString()
    sock.sendto(data, address)


def main():
    # grSimの送信先アドレス
    GRSIM_ADDRESS = ("127.0.0.1", 20011)
    
    # UDPソケットを作成
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("grSimにロボットコマンドを送信します...")
    print(f"送信先: {GRSIM_ADDRESS}")
    print("Ctrl+Cで終了")
    print()
    
    try:
        # ロボットID 0を動かすデモ
        robot_id = 0
        is_yellow = False  # 青チーム
        
        # パターン1: 前進
        print("前進中...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, veltangent=1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)  # 約60Hz
        
        # パターン2: 停止
        print("停止...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # パターン3: 後退
        print("後退中...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, veltangent=-1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # パターン4: 停止
        print("停止...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # パターン5: 左移動
        print("左移動中...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, velnormal=1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # パターン6: 停止
        print("停止...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # パターン7: 右移動
        print("右移動中...")
        for _ in range(50):
            cmd = create_robot_command(robot_id, velnormal=-1.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # パターン8: 停止
        print("停止...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # パターン9: 回転
        print("回転中...")
        for _ in range(100):
            cmd = create_robot_command(robot_id, velangular=3.0)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        # 最終停止
        print("停止...")
        for _ in range(30):
            cmd = create_robot_command(robot_id)
            send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
            time.sleep(0.016)
        
        print("デモ完了!")
        
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        # 停止コマンドを送信
        cmd = create_robot_command(robot_id)
        send_command(sock, GRSIM_ADDRESS, [cmd], is_yellow)
        sock.close()


if __name__ == "__main__":
    main()
