from celery import shared_task

from .simulation.scientists import ExperimentRunner, ExperimentCollater

@shared_task
def runExperimentTask(sim_params: dict) -> list:
    "Runs a SimExperiment, returning the resulting simtrial ids."
    runner = ExperimentRunner(sim_params)
    simtrial_ids = runner.run_experiment()
    return simtrial_ids

@shared_task
def pollExperimentsThenCollateTask(poll_task_ids: list , sim_params: dict,) -> str:
    """Polls parallel experiment run chunks till all complete, then collates their simtrial ids and saves the simexperiment, returning the simexperiment id."""
    # TO DO --> write poll logic here....
    chunked_simtrial_ids = ...

    collater = ExperimentCollater(sim_params, chunked_simtrial_ids)
    simexperiment_obj = collater.save_experiment()
    simexperiment_id = simexperiment_obj.id
    return simexperiment_id