# vlan_check.py

def check_vlan(vlan_id):
    if 1 <= vlan_id <= 1005:
        return "VLAN del rango normal"
    elif 1006 <= vlan_id <= 4094:
        return "VLAN del rango extendido"
    else:
        return "Número de VLAN fuera de rango"

try:
    vlan_id = int(input("Ingrese el número de VLAN: "))
    print(check_vlan(vlan_id))
except ValueError:
    print("Por favor, ingrese un número válido.")
