from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SimExperimentSerializer
from .tasks import runExperimentTask, pollExperimentsThenCollateTask


class RunExperimentView(APIView):
    def post(self, request,):
        # process inputs
        serializer = SimExperimentSerializer(request.data)
        sim_params = serializer.validated_data
        
        # task workflow
        ## 1. simulate
        ### TO DO --> setup chunking for parallelization
        sim_task_id = runExperimentTask.delay(sim_params).id # queue up async task
        ## 2. poll then collate
        collater_task_id = pollExperimentsThenCollateTask.delay([sim_task_id], sim_params).id

        response_payload = {
            'accepted': True,
            'sim_task_ids': [sim_task_id],
            'collate_task_id': collater_task_id,
        }
        return Response(response_payload, 202)