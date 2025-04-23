from depp import AdeptDepp

DEVICE_NAME = "DOnbUsb"

depp = None

depp = AdeptDepp(DEVICE_NAME)
print("[✓] Verbindung erfolgreich")

print("Register 0 lesen...")
val = depp.get_reg(0)
print(f"Wert: {val}")

print("Register 0 auf 42 setzen...")
depp.set_reg(0, 42)

print("Zurücklesen...")
val = depp.get_reg(0)
print(f"Neuer Wert: {val}")

if depp is not None:
    depp.close()
print("[✓] Verbindung geschlossen")
