from celery import Celery
import glob
import sys

try:
    import run_spec2vec
except:
    pass


celery_instance = Celery('tasks', backend='redis://gnpssimilarity-redis', broker='pyamqp://guest@gnpssimilarity-rabbitmq//', )

@celery_instance.task(time_limit=60)
def task_computeheartbeat():
    print("UP", file=sys.stderr, flush=True)
    return "Up"

@celery_instance.task(time_limit=60)
def tasks_compute_similarity_gnpsalignment(usi1, usi2):
    results = {}
    results["sim"] = 1.0
    results["matched_peaks"] = 6
    results["type"] = "gnpsalignment"

    return results

@celery_instance.task(time_limit=60)
def tasks_compute_similarity_usi(usi1, usi2):
    results = {}
    results["sim"] = 1.0
    results["matched_peaks"] = 6
    results["type"] = "usi"

    return results

@celery_instance.task(time_limit=60)
def tasks_compute_similarity_matchms(usi1, usi2):
    score = run_spec2vec.calculate_modified_cosine(usi1, usi2)

    results = {}
    results["sim"] = float(score["score"].flat[0])
    results["matched_peaks"] = int(score["matches"].flat[0])
    results["type"] = "matchms"

    return results

@celery_instance.task(time_limit=60)
def tasks_compute_similarity_spec2vec(usi1, usi2):
    score = run_spec2vec.calculate_spec2vec(usi1, usi2)
    
    results = {}
    results["sim"] = 1.0
    results["matched_peaks"] = 6
    results["type"] = "spec2vec"

    return results

@celery_instance.task(time_limit=60)
def tasks_compute_similarity_simile(usi1, usi2):
    results = {}
    results["sim"] = 1.0
    results["matched_peaks"] = 6
    results["type"] = "simile"

    return results

# celery_instance.conf.beat_schedule = {
#     "cleanup": {
#         "task": "tasks._task_cleanup",
#         "schedule": 3600
#     }
# }


celery_instance.conf.task_routes = {
    'tasks.task_computeheartbeat': {'queue': 'worker'},

    
    'tasks.tasks_compute_similarity_gnpsalignment': {'queue': 'worker'},
    'tasks.tasks_compute_similarity_usi': {'queue': 'worker'},

    'tasks.tasks_compute_similarity_spec2vec': {'queue': 'spec2vec'},
    'tasks.tasks_compute_similarity_matchms': {'queue': 'spec2vec'},

    'tasks.tasks_compute_similarity_simile': {'queue': 'worker'},
}