import ctypes
import os

def load_library(libname: str) -> ctypes.CDLL:
    """
    Load a shared library from system or user-defined locations.
    
    Priority:
    1. DEPP_LIB_PATH environment variable
    2. Common system paths
    3. Rely on LD_LIBRARY_PATH or system defaults

    :param libname: The filename of the shared library (e.g. 'libdepp.so')
    :return: Loaded ctypes CDLL object
    :raises FileNotFoundError: If the library could not be found
    """
    search_paths = []

    # 1. Environment override
    env_path = os.environ.get("DEPP_LIB_PATH")
    if env_path:
        search_paths.append(os.path.join(env_path, libname))

    # 2. Common fallback paths
    search_paths += [
        f"/usr/lib64/digilent/adept/{libname}",
        f"/usr/lib/digilent/adept/{libname}",
        f"/usr/local/lib/digilent/adept/{libname}",
        f"/opt/digilent/adept/{libname}"
    ]

    # 3. Final fallback – system-wide discovery via LD_LIBRARY_PATH
    search_paths.append(libname)

    for path in search_paths:
        if os.path.exists(path) or '/' not in path:
            try:
                return ctypes.CDLL(path)
            except OSError:
                continue

    raise FileNotFoundError(
        f"Could not locate shared library '{libname}'. Tried paths:\n" +
        "\n".join(search_paths)
    )
