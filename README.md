# SSL-Test

A Python toolkit for communicating with [grSim](https://github.com/RoboCup-SSL/grSim) and [SSL-Vision](https://github.com/RoboCup-SSL/ssl-vision) in the RoboCup Small Size League (SSL) environment.

## Features

- **Proto Compilation** — Compile `.proto` definitions to Python modules
- **Vision Reception** — Receive real-time robot and ball positions from SSL-Vision via multicast
- **Robot Control** — Send movement commands (velocity, rotation, kick, dribble) to grSim

## Prerequisites

- Python 3.8+
- [grSim](https://github.com/RoboCup-SSL/grSim) running locally

## Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux / macOS

# Install dependencies
pip install -r requirements.txt

# Compile proto files
python compile_proto.py
```

## Usage

### Receive Vision Data

Listens on multicast `224.5.23.2:10006` and prints detected robots and ball positions.

```bash
python receive_vision.py
```

### Send Robot Commands

Sends a movement demo (forward → stop → backward → stop → left → stop → right → stop → rotate → stop) to robot ID 0 on the blue team.

```bash
python send_robot_command.py
```

## Project Structure

```
ssl-test/
├── proto/                  # .proto definitions (grSim & SSL-Vision)
├── generated/              # Auto-generated Python protobuf modules
├── compile_proto.py        # Proto → Python compiler script
├── receive_vision.py       # SSL-Vision multicast receiver
├── send_robot_command.py   # grSim robot command sender
└── requirements.txt        # Python dependencies
```

## Network Configuration

| Purpose         | Protocol  | Address             |
|-----------------|-----------|---------------------|
| SSL-Vision data | Multicast | `224.5.23.2:10006`  |
| grSim commands  | UDP       | `127.0.0.1:20011`   |

## License

This project is for educational and experimental use with RoboCup SSL.
