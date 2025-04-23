from .depp import AdeptDepp

DEVICE_NAME = "DOnbUsb"

print("[✓] Starting DEPP interface test")

with AdeptDepp(DEVICE_NAME) as depp:
    print("[✓] Connection established")

    # Single register read/write
    print("Reading register 0...")
    val = depp.get_reg(0)
    print(f"Value: {val}")

    print("Writing 42 to register 0...")
    depp.set_reg(0, 42)

    print("Reading back register 0...")
    val = depp.get_reg(0)
    print(f"New value: {val}")

    # Block write (address-data pairs: [reg, val, reg, val, ...])
    print("Writing block to registers 1, 2, 3...")
    depp.set_reg_block([1, 11, 2, 22, 3, 33])

    # Block read
    print("Reading block from registers 1, 2, 3...")
    values = depp.get_reg_block([1, 2, 3])
    print(f"Read values: {values}")

    # Streaming write
    print("Streaming bytes to register 4...")
    stream_data = bytes([10, 20, 30, 40, 50])
    depp.put_stream(4, stream_data)

    # Streaming read
    print("Reading streamed bytes from register 4...")
    received_data = depp.get_stream(4, len(stream_data))
    print(f"Received stream: {list(received_data)}")

    # Set timeout (e.g., 1ms)
    print("Setting timeout to 1 ms...")
    depp.set_timeout(1_000_000)

    # Dump all 256 8-bit registers with decimal and hex representation
    print("\nRegister dump (0-255):")
    print("+--------+-----------+-----------+")
    print("| Addr   | Value (d) | Value (h) |")
    print("+--------+-----------+-----------+")
    for i in range(256):
        try:
            val = depp.get_reg(i)
            print(f"| {i:6} | {val:9} | 0x{val:02X}     |")
        except RuntimeError:
            print(f"| {i:6} |   <fail> |   <fail>   |")
    print("+--------+-----------+-----------+")

print("[✓] DEPP interface test complete")
