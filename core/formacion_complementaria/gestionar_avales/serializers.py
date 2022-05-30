from rest_framework import serializers
from core.base.models import modelosUsuario

class UserAvalSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid()
        if is_valid and not self.instance:
            if modelosUsuario.Aval.objects.filter(usuario=self.initial_data.get('usuario')).exists():
                is_valid = False
                self._errors.setdefault('detail','El usuario ya presenta un aval')

        return is_valid

    class Meta:
        model = modelosUsuario.Aval
        exclude = ('id','usuario')