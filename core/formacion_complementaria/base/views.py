from rest_framework.generics import ListCreateAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from core.base.models.modelosSimple import Area
from core.base.models.modelosUsuario import Graduado
from core.base.permissions import IsDirectorRecursosHumanos, IsJefeArea, IsSameAreaPermissions
from core.formacion_complementaria.base.filters import GraduadoFilterSet
from core.formacion_complementaria.base.serializers import ImportarGraduadoSerializer, GraduadoSerializer, \
    ImportarTutorSerializer
from custom.authentication.LDAP.ldap_manager import LDAPManager
from custom.authentication.models import DirectoryUser


class ImportarGraduadosDirectorio(ListCreateAPIView):
    permission_classes = [IsDirectorRecursosHumanos]

    def list(self, request, **kwargs):
        graduados = LDAPManager().all_graduates()
        importados = Graduado.objects.filter(directorioID__in=[grad['areaId'] for grad in graduados])

        sin_importar = []
        for element in graduados:
            found = False
            it = iter(importados)
            try:
                while not found:
                    elem = next(it)
                    if elem.directorioID == element['areaId']:
                        found = True
            except StopIteration:  # SOLAMENTE SE LANZA CUANDO LLEGA AL FINAL
                sin_importar.append(element)

        return Response(sin_importar, HTTP_200_OK)

    def create(self, request, **kwargs):
        data = request.data
        serializer = ImportarGraduadoSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail': 'Graduados importados correctamente'}, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class ImportarTutoresDirectorio(ListCreateAPIView):
    permission_classes = (IsSameAreaPermissions, IsJefeArea | IsDirectorRecursosHumanos)

    # NO SE LE PUSO FILTRO PORQUE HARIA MAS COMPLEJA LA CONSULTA O TARDARIA MAS. EL FRONT QUE FILTRE
    def list(self, request, **kwargs):
        area = kwargs['area']
        tutores = LDAPManager().all_tutors_from_area(area)
        importados = DirectoryUser.objects.filter(directorioID__in=[tutor['areaId'] for tutor in tutores])

        sin_importar = []
        for element in tutores:
            found = False
            it = iter(importados)
            try:
                while not found:
                    elem = next(it)
                    if elem.directorioID == element['areaId']:
                        found = True
            except StopIteration:  # SOLAMENTE SE LANZA CUANDO LLEGA AL FINAL
                sin_importar.append(element)

        return Response(sin_importar, HTTP_200_OK)

    def create(self, request, **kwargs):
        data = request.data
        data['area'] = kwargs['area']
        serializer = ImportarTutorSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'detail': 'Tutores importados correctamente'}, HTTP_200_OK)
        else:
            return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class ListGraduadosDelArea(ListAPIView):
    serializer_class = GraduadoSerializer
    permission_classes = (IsSameAreaPermissions, IsJefeArea | IsDirectorRecursosHumanos)
    # FILTRADO
    filterset_class = GraduadoFilterSet
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering_fields = '__all__'

    def get_queryset(self):
        area = get_object_or_404(Area, pk=self.kwargs['areaID'])
        return Graduado.objects.filter(area=area).distinct()
