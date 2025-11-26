from app.domain.entities.reserva import Reserva
from app.infrastructure.db.models.reserva_model import ReservaModel


class ReservaMapper:
    """
    Mapper entre entidad Reserva y modelo ReservaModel
    """
    
    @staticmethod
    def to_entity(model: ReservaModel) -> Reserva:
        """Convierte un modelo de DB a entidad de dominio"""
        return Reserva(
            id=model.id,
            cliente_id=model.cliente_id,
            recurso_id=model.recurso_id,
            fecha_hora_inicio=model.fecha_hora_inicio,
            fecha_hora_fin=model.fecha_hora_fin,
            duracion_minutos=model.duracion_minutos,
            estado=model.estado,
            precio_total=model.precio_total,
            seña=model.seña,
            saldo_pendiente=model.saldo_pendiente,
            metodo_pago=model.metodo_pago,
            pago_completo=model.pago_completo,
            notas_cliente=model.notas_cliente,
            notas_internas=model.notas_internas,
            motivo_cancelacion=model.motivo_cancelacion,
            fecha_cancelacion=model.fecha_cancelacion,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    @staticmethod
    def to_model(entity: Reserva) -> ReservaModel:
        """Convierte una entidad de dominio a modelo de DB"""
        model = ReservaModel(
            id=entity.id,
            cliente_id=entity.cliente_id,
            recurso_id=entity.recurso_id,
            fecha_hora_inicio=entity.fecha_hora_inicio,
            fecha_hora_fin=entity.fecha_hora_fin,
            duracion_minutos=entity.duracion_minutos,
            estado=entity.estado,
            precio_total=entity.precio_total,
            seña=entity.seña,
            saldo_pendiente=entity.saldo_pendiente,
            metodo_pago=entity.metodo_pago,
            pago_completo=entity.pago_completo,
            notas_cliente=entity.notas_cliente,
            notas_internas=entity.notas_internas,
            motivo_cancelacion=entity.motivo_cancelacion,
            fecha_cancelacion=entity.fecha_cancelacion,
        )
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model

    @staticmethod
    def update_model_from_entity(model: ReservaModel, entity: Reserva) -> None:
        """Actualiza un modelo existente con datos de la entidad"""
        model.fecha_hora_inicio = entity.fecha_hora_inicio
        model.fecha_hora_fin = entity.fecha_hora_fin
        model.duracion_minutos = entity.duracion_minutos
        model.estado = entity.estado
        model.precio_total = entity.precio_total
        model.seña = entity.seña
        model.saldo_pendiente = entity.saldo_pendiente
        model.metodo_pago = entity.metodo_pago
        model.pago_completo = entity.pago_completo
        model.notas_cliente = entity.notas_cliente
        model.notas_internas = entity.notas_internas
        model.motivo_cancelacion = entity.motivo_cancelacion
        model.fecha_cancelacion = entity.fecha_cancelacion
        model.updated_at = entity.updated_at