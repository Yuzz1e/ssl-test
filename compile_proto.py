"""
protoファイルをPython用にコンパイルするスクリプト
"""
import subprocess
import sys
import os

def main():
    proto_dir = "proto"
    output_dir = "generated"
    
    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)
    
    # grSim関連のprotoファイルをコンパイル
    proto_files = [
        "grSim_Commands.proto",
        "grSim_Replacement.proto",
        "grSim_Packet.proto",
    ]
    
    for proto_file in proto_files:
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"--proto_path={proto_dir}",
            f"--python_out={output_dir}",
            f"{proto_dir}/{proto_file}"
        ]
        print(f"Compiling {proto_file}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            sys.exit(1)
    
    # __init__.pyを作成
    init_file = os.path.join(output_dir, "__init__.py")
    with open(init_file, "w") as f:
        f.write("")
    
    print("Proto files compiled successfully!")

if __name__ == "__main__":
    main()
