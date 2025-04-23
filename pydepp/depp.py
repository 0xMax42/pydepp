from typing import List
import ctypes
from ctypes import c_ubyte, c_uint32
from .ffi import libdepp, libdmgr, HIF

class AdeptDepp:
    """
    High-level object-oriented wrapper for the Digilent DEPP interface.
    Provides convenient methods for register access and data streaming
    over a DEPP-compatible USB-FPGA connection using the Adept SDK.
    """

    def __init__(self, device_name: str):
        """
        Initialize the DEPP interface and open a handle to the given device.

        :param device_name: The name of the connected device (e.g., "Basys3")
        :raises RuntimeError: If device cannot be opened or enabled
        """
        self.hif = HIF()
        if not libdmgr.DmgrOpen(ctypes.byref(self.hif), device_name.encode()):
            raise RuntimeError(f"DmgrOpen failed for device '{device_name}'")

        if not libdepp.DeppEnable(self.hif):
            libdmgr.DmgrClose(self.hif)
            raise RuntimeError("DeppEnable failed")

    def __enter__(self):
        """
        Context manager entry: returns self for use with 'with' statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit: automatically closes the DEPP connection.
        """
        self.close()

    def get_reg(self, reg: int) -> int:
        """
        Read a single byte from a specified register address.

        :param reg: Register address (0-255)
        :return: Byte value read from the register
        :raises RuntimeError: If the read fails
        """
        value = c_ubyte()
        if not libdepp.DeppGetReg(self.hif, c_ubyte(reg), ctypes.byref(value), False):
            raise RuntimeError(f"DeppGetReg failed at reg {reg}")
        return value.value

    def set_reg(self, reg: int, value: int):
        """
        Write a single byte to a specified register address.

        :param reg: Register address (0-255)
        :param value: Byte value to write
        :raises RuntimeError: If the write fails
        """
        if not libdepp.DeppPutReg(self.hif, c_ubyte(reg), c_ubyte(value), False):
            raise RuntimeError(f"DeppPutReg failed at reg {reg}")

    def set_reg_block(self, addr_data: List[int]):
        """
        Write multiple address-value pairs in one transaction.

        :param addr_data: List of alternating register addresses and values
        :raises ValueError: If list length is not even
        :raises RuntimeError: If the write fails
        """
        if len(addr_data) % 2 != 0:
            raise ValueError("List must contain address-data pairs")
        buf = (c_ubyte * len(addr_data))(*addr_data)
        if not libdepp.DeppPutRegSet(self.hif, buf, len(addr_data) // 2, False):
            raise RuntimeError("DeppPutRegSet failed")

    def get_reg_block(self, addresses: List[int]) -> List[int]:
        """
        Read multiple registers in one transaction.

        :param addresses: List of register addresses
        :return: List of read values
        :raises RuntimeError: If the read fails
        """
        addr_buf = (c_ubyte * len(addresses))(*addresses)
        data_buf = (c_ubyte * len(addresses))()
        if not libdepp.DeppGetRegSet(self.hif, addr_buf, data_buf, len(addresses), False):
            raise RuntimeError("DeppGetRegSet failed")
        return list(data_buf)

    def put_stream(self, reg: int, data: bytes):
        """
        Stream a sequence of bytes to a single register address.

        :param reg: Register address
        :param data: Byte stream to write
        :raises RuntimeError: If the write fails
        """
        buf = (c_ubyte * len(data)).from_buffer_copy(data)
        if not libdepp.DeppPutRegRepeat(self.hif, c_ubyte(reg), buf, len(data), False):
            raise RuntimeError("DeppPutRegRepeat failed")

    def get_stream(self, reg: int, count: int) -> bytes:
        """
        Stream a sequence of bytes from a single register address.

        :param reg: Register address
        :param count: Number of bytes to read
        :return: Byte stream read
        :raises RuntimeError: If the read fails
        """
        buf = (c_ubyte * count)()
        if not libdepp.DeppGetRegRepeat(self.hif, c_ubyte(reg), buf, count, False):
            raise RuntimeError("DeppGetRegRepeat failed")
        return bytes(buf)

    def set_timeout(self, timeout_ns: int):
        """
        Set the DEPP communication timeout in nanoseconds.

        :param timeout_ns: Desired timeout in nanoseconds
        :raises RuntimeError: If setting the timeout fails
        """
        actual = c_uint32()
        if not libdepp.DeppSetTimeout(self.hif, timeout_ns, ctypes.byref(actual)):
            raise RuntimeError("DeppSetTimeout failed")

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the DEPP interface, including
        register values from 0 to 255, shown in both decimal and hexadecimal format.
        
        This method is useful for debugging or inspection, especially in interactive
        environments or when printing the object directly.
        
        :return: Formatted string showing register contents.
        """
        lines = ["AdeptDepp – Register dump (0-255):"]
        lines.append("+--------+-----------+-----------+")
        lines.append("| Addr   | Value (d) | Value (h) |")
        lines.append("+--------+-----------+-----------+")
        for i in range(256):
            try:
                val = self.get_reg(i)
                lines.append(f"| {i:6} | {val:9} | 0x{val:02X}     |")
            except RuntimeError:
                lines.append(f"| {i:6} |   <fail> |   <fail>   |")
        lines.append("+--------+-----------+-----------+")
        return "\n".join(lines)

    def close(self):
        """
        Cleanly close the DEPP interface and release the device handle.
        """
        libdepp.DeppDisable(self.hif)
        libdmgr.DmgrClose(self.hif)