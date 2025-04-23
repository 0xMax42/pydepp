import ctypes
from ctypes import c_bool, c_char_p, c_ubyte, c_void_p, POINTER, c_uint32

# Load Digilent Adept shared libraries
from .loader import load_library
libdmgr = load_library("libdmgr.so")
libdepp = load_library("libdepp.so")

# Type alias for device handle
HIF = c_void_p

# Configure function signatures for DMGR API
libdmgr.DmgrOpen.argtypes = [POINTER(HIF), c_char_p]
libdmgr.DmgrOpen.restype = c_bool

libdmgr.DmgrClose.argtypes = [HIF]
libdmgr.DmgrClose.restype = c_bool

# Configure function signatures for DEPP API
libdepp.DeppEnable.argtypes = [HIF]
libdepp.DeppEnable.restype = c_bool

libdepp.DeppEnableEx.argtypes = [HIF, ctypes.c_int32]
libdepp.DeppEnableEx.restype = c_bool

libdepp.DeppDisable.argtypes = [HIF]
libdepp.DeppDisable.restype = c_bool

libdepp.DeppGetVersion.argtypes = [c_char_p]
libdepp.DeppGetVersion.restype = c_bool

libdepp.DeppGetPortCount.argtypes = [HIF, POINTER(ctypes.c_int32)]
libdepp.DeppGetPortCount.restype = c_bool

libdepp.DeppGetPortProperties.argtypes = [HIF, ctypes.c_int32, POINTER(ctypes.c_uint32)]
libdepp.DeppGetPortProperties.restype = c_bool

libdepp.DeppSetTimeout.argtypes = [HIF, c_uint32, POINTER(c_uint32)]
libdepp.DeppSetTimeout.restype = c_bool

libdepp.DeppPutReg.argtypes = [HIF, c_ubyte, c_ubyte, c_bool]
libdepp.DeppPutReg.restype = c_bool

libdepp.DeppGetReg.argtypes = [HIF, c_ubyte, POINTER(c_ubyte), c_bool]
libdepp.DeppGetReg.restype = c_bool

libdepp.DeppPutRegSet.argtypes = [HIF, POINTER(c_ubyte), c_uint32, c_bool]
libdepp.DeppPutRegSet.restype = c_bool

libdepp.DeppGetRegSet.argtypes = [HIF, POINTER(c_ubyte), POINTER(c_ubyte), c_uint32, c_bool]
libdepp.DeppGetRegSet.restype = c_bool

libdepp.DeppPutRegRepeat.argtypes = [HIF, c_ubyte, POINTER(c_ubyte), c_uint32, c_bool]
libdepp.DeppPutRegRepeat.restype = c_bool

libdepp.DeppGetRegRepeat.argtypes = [HIF, c_ubyte, POINTER(c_ubyte), c_uint32, c_bool]
libdepp.DeppGetRegRepeat.restype = c_bool