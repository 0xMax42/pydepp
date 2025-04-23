import ctypes
from ctypes import c_bool, c_char_p, c_ubyte, c_void_p, POINTER

# Pfade zu den Digilent Libraries
libdmgr = ctypes.CDLL("/usr/lib64/digilent/adept/libdmgr.so")
libdepp = ctypes.CDLL("/usr/lib64/digilent/adept/libdepp.so")

# Typdefinition für das Handle
HIF = c_void_p

# Funktions-Signaturen definieren
libdmgr.DmgrOpen.argtypes = [POINTER(HIF), c_char_p]
libdmgr.DmgrOpen.restype = c_bool

libdmgr.DmgrClose.argtypes = [HIF]
libdmgr.DmgrClose.restype = c_bool

libdepp.DeppEnable.argtypes = [HIF]
libdepp.DeppEnable.restype = c_bool

libdepp.DeppDisable.argtypes = [HIF]
libdepp.DeppDisable.restype = c_bool

libdepp.DeppGetReg.argtypes = [HIF, c_ubyte, POINTER(c_ubyte), c_bool]
libdepp.DeppGetReg.restype = c_bool

libdepp.DeppPutReg.argtypes = [HIF, c_ubyte, c_ubyte, c_bool]
libdepp.DeppPutReg.restype = c_bool


class AdeptDepp:
    def __init__(self, device_name: str):
        self.hif = HIF()
        ok = libdmgr.DmgrOpen(ctypes.byref(self.hif), device_name.encode())
        if not ok:
            raise RuntimeError(f"DmgrOpen failed for device '{device_name}'")

        if not libdepp.DeppEnable(self.hif):
            libdmgr.DmgrClose(self.hif)
            raise RuntimeError("DeppEnable failed")

    def get_reg(self, reg: int) -> int:
        value = c_ubyte()
        if not libdepp.DeppGetReg(self.hif, c_ubyte(reg), ctypes.byref(value), False):
            raise RuntimeError(f"DeppGetReg failed at reg {reg}")
        return value.value

    def set_reg(self, reg: int, value: int):
        if not libdepp.DeppPutReg(self.hif, c_ubyte(reg), c_ubyte(value), False):
            raise RuntimeError(f"DeppPutReg failed at reg {reg}")

    def close(self):
        libdepp.DeppDisable(self.hif)
        libdmgr.DmgrClose(self.hif)
