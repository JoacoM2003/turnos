from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    PROVEEDOR = "proveedor"
    CLIENTE = "cliente"
