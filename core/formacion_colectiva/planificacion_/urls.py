from django.urls import path
from rest_framework.routers import DefaultRouter

from core.formacion_colectiva.planificacion_.views import ListCreateRetrieveUpdatePlanFormacionColectivo, \
    ListEtapasPlanFormacionColectivo, RetrieveUpdateEtapaPlanFormacionColectivo, ListCreatePlanColectivoCommets, \
    ListCreateActividadColectiva, RetrieveDeleteUpdateActividadColectiva, RetrieveJovenPlanColectivo, \
    FirmarPlanColectivo, ActividadColectivaUploadFile

app_name = 'PlanificacionFormacionColectiva'

urlpatterns = [
    path('joven/<int:jovenID>/plan-colectivo', RetrieveJovenPlanColectivo.as_view()),

    path('plan-colectivo/<int:planID>/etapas', ListEtapasPlanFormacionColectivo.as_view()),
    path('plan-colectivo/<int:planID>/comentarios', ListCreatePlanColectivoCommets.as_view()),
    path('etapa/<int:etapaID>/actividades', ListCreateActividadColectiva.as_view()),
    path('plan-colectivo/<int:planID>/firmar', FirmarPlanColectivo.as_view()),
    path('actividad-colectiva/<int:actividadID>/subir-archivo', ActividadColectivaUploadFile.as_view()),

    # path('plan-colectivo/ID', APIView.as_view()),  # CAMBIAR ESTADO DEL PLAN
    # path('plan-colectivo/ID/exportar-pdf', APIView.as_view()),
    # path('plan-colectivo/ID/exportar-calendario', APIView.as_view()),
]

router = DefaultRouter()
router.register('plan-colectivo', ListCreateRetrieveUpdatePlanFormacionColectivo, 'plan-colectivo')
router.register('etapa', RetrieveUpdateEtapaPlanFormacionColectivo, 'etapa-colectiva')
router.register('actividad-colectiva', RetrieveDeleteUpdateActividadColectiva, 'actividad-colectiva')

urlpatterns += router.urls
