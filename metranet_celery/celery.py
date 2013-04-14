from __future__ import absolute_import

from celery import Celery

celery = Celery('metranet_celery.celery' , 
		 broker="amqp://10.10.2.59", 
		 backend="amqp://10.10.2.59", 
		 include=['metranet_celery.tasks'])

celery.conf.update(
	CELERY_TASK_RESULT_EXPIRES = 3600,
)

if __name__ == "__main__" :
    celery.start()
