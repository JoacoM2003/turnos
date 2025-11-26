from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Reserva:
    """
    Reserva de un recurso
    """
    id: Optional[int]
    cliente_id: int
    recurso_id: int
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    duracion_minutos: int
    estado: str
    precio_total: float
    seña: Optional[float]
    saldo_pendiente: Optional[float]
    metodo_pago: Optional[str]
    pago_completo: bool
    notas_cliente: Optional[str]
    notas_internas: Optional[str]
    motivo_cancelacion: Optional[str]
    fecha_cancelacion: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def crear(
        cls,
        cliente_id: int,
        recurso_id: int,
        fecha_hora_inicio: datetime,
        fecha_hora_fin: datetime,
        duracion_minutos: int,
        precio_total: float,
        notas_cliente: Optional[str] = None,
    ):
        """
        Crea una nueva reserva
        """
        now = datetime.now(timezone.utc)
        
        # Validar que la fecha sea futura
        if fecha_hora_inicio <= now:
            raise ValueError("La fecha de reserva debe ser futura")
        
        # Validar que fecha_fin sea después de fecha_inicio
        if fecha_hora_fin <= fecha_hora_inicio:
            raise ValueError("La fecha de fin debe ser posterior al inicio")
        
        return cls(
            id=None,
            cliente_id=cliente_id,
            recurso_id=recurso_id,
            fecha_hora_inicio=fecha_hora_inicio,
            fecha_hora_fin=fecha_hora_fin,
            duracion_minutos=duracion_minutos,
            estado="pendiente",
            precio_total=precio_total,
            seña=None,
            saldo_pendiente=precio_total,
            metodo_pago=None,
            pago_completo=False,
            notas_cliente=notas_cliente,
            notas_internas=None,
            motivo_cancelacion=None,
            fecha_cancelacion=None,
            created_at=now,
            updated_at=now,
        )

    def confirmar(self):
        """Confirma la reserva"""
        if self.estado != "pendiente":
            raise ValueError("Solo se pueden confirmar reservas pendientes")
        self.estado = "confirmada"
        self.updated_at = datetime.now(timezone.utc)

    def cancelar(self, motivo: Optional[str] = None):
        """Cancela la reserva"""
        if self.estado in ["completada", "cancelada"]:
            raise ValueError("No se puede cancelar una reserva completada o ya cancelada")
        
        self.estado = "cancelada"
        self.motivo_cancelacion = motivo
        self.fecha_cancelacion = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def registrar_pago(self, monto: float, metodo: str, es_pago_completo: bool = False):
        """Registra un pago (seña o completo)"""
        if es_pago_completo:
            self.seña = monto
            self.saldo_pendiente = 0
            self.pago_completo = True
        else:
            self.seña = monto
            self.saldo_pendiente = self.precio_total - monto
        
        self.metodo_pago = metodo
        self.updated_at = datetime.now(timezone.utc)

    def completar(self):
        """Marca la reserva como completada"""
        if self.estado != "confirmada":
            raise ValueError("Solo se pueden completar reservas confirmadas")
        
        self.estado = "completada"
        self.updated_at = datetime.now(timezone.utc)