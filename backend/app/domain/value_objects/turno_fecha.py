from datetime import datetime

class TurnoFecha:
    def __init__(self, fecha: datetime):
        self.value = fecha
        self._validate()

    def _validate(self):
        if self.value < datetime.now():
            raise ValueError('La fecha de turno debe ser futura')
