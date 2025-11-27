from django.db.models.signals import post_save
from django.dispatch import receiver
from task.models import Paciente, Odontograma,Diente

@receiver(post_save, sender=Paciente)
def crear_odontograma_automatico(sender, instance, created, **kwargs):
    if created:
        # 1. Crear el Odontograma vacío
        odontograma = Odontograma.objects.create(paciente=instance)

        # 2. Crear los 52 dientes (Adultos + Niños) según norma ISO
        # Dientes Adultos: 11-18, 21-28, 31-38, 41-48
        # Dientes Niños: 51-55, 61-65, 71-75, 81-85
        rango_adultos = [
            range(11, 19), range(21, 29),
            range(31, 39), range(41, 49)
        ]
        rango_ninos = [
            range(51, 56), range(61, 66),
            range(71, 76), range(81, 86)
        ]

        lista_dientes = []

        # Generar adultos
        for cuadrante in rango_adultos:
            for numero in cuadrante:
                lista_dientes.append(Diente(odontograma=odontograma, numero_diente=numero))

        # Generar niños
        for cuadrante in rango_ninos:
            for numero in cuadrante:
                lista_dientes.append(Diente(odontograma=odontograma, numero_diente=numero))

        # Guardar todos de golpe (muy rápido)
        Diente.objects.bulk_create(lista_dientes)