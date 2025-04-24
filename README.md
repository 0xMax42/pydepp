# PyDEPP: Python Bindings for the Digilent DEPP Protocol

PyDEPP is a Python library that provides a high-level, object-oriented interface for interacting with Digilent FPGA boards over the DEPP (Digilent Asynchronous Parallel Port) protocol. It leverages the Digilent Adept SDK to enable seamless communication with DEPP-compatible devices.

## Features

- **Register Access**: Read and write single or multiple registers with ease.
- **Data Streaming**: Stream data to and from registers for high-performance applications.
- **Timeout Configuration**: Set custom communication timeouts for DEPP operations.
- **Context Management**: Use Python's `with` statement for automatic resource management.
- **Debugging Tools**: Includes a detailed register dump for inspection and debugging.

## Requirements

- Python 3.7 or higher
- Digilent Adept Runtime and SDK installed on your system
- Shared libraries `libdmgr.so` and `libdepp.so` available in your library paths

## Installation

### From Source

1. Clone the repository:

   ```bash
   git clone https://github.com/0xMax42/pydepp.git
   cd pydepp
   ```

2. Install the library:

   ```bash
   pip install .
   ```

### Debian Package

You can also build and install the Debian package:

1. Build the package:

   ```bash
   dpkg-buildpackage -us -uc
   ```

2. Install the package:

   ```bash
   sudo dpkg -i ../pydepp_0.1.1_all.deb
   ```

## Usage

### Basic Example

```python
from pydepp import AdeptDepp

DEVICE_NAME = "Basys3"

with AdeptDepp(DEVICE_NAME) as depp:
    # Read a register
    value = depp.get_reg(0)
    print(f"Register 0 value: {value}")

    # Write to a register
    depp.set_reg(0, 42)
    print("Wrote 42 to register 0")

    # Stream data
    data = bytes([1, 2, 3, 4, 5])
    depp.put_stream(4, data)
    print("Streamed data to register 4")
```

### Full Example

For a more comprehensive example, see the [`example.py`](pydepp/example.py) file in the repository.

## API Overview

### `AdeptDepp` Class

- **Initialization**: Open a connection to a DEPP-compatible device.
- **Register Access**:
  - `get_reg(reg: int) -> int`: Read a single register.
  - `set_reg(reg: int, value: int)`: Write to a single register.
  - `get_reg_block(addresses: List[int]) -> List[int]`: Read multiple registers.
  - `set_reg_block(addr_data: List[int])`: Write multiple registers.
- **Data Streaming**:
  - `put_stream(reg: int, data: bytes)`: Stream data to a register.
  - `get_stream(reg: int, count: int) -> bytes`: Stream data from a register.
- **Timeout**:
  - `set_timeout(timeout_ns: int)`: Set communication timeout in nanoseconds.
- **Context Management**:
  - Use `with AdeptDepp(...)` for automatic resource cleanup.

## Development

### Building the Project

To build the project, ensure you have `setuptools` installed and run:

```bash
python setup.py sdist bdist_wheel
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/0xMax42/pydepp).

## Acknowledgments

- **Digilent Adept SDK**: This library relies on the [Adept SDK](https://digilent.com/reference/software/adept/start) for low-level DEPP communication.
- **Author**: [0xMax42](https://github.com/0xMax42)