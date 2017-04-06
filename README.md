# Distribrewed core
This repo contains the core communications between master and workers

## Installing package
```
$ pip install https://github.com/hif/DistriBrewed-Core/archive/master.zip#egg=distribrewed-core
```
Note: This only installs the the core package and not the django framework that is used for development!

## Environmental variables
#### For development
| Name        | Type           | Description  |
| ------------- |:-------------:| -----:|
| CELERY_ALWAYS_EAGER | boolean | If true, celery does not use broker |
| DEBUG      | boolean      |   Set to true for verbose output |
| DJANGO_SETTINGS_MODULE | string      |    Settings module to use, default: core_dev.settings.settings |

#### Other
| Name        | Type           | Description  |
| ------------- |:-------------:| -----:|
| WORKER_NAME | string | If set, core assumes that process is a worker and creates queues for him |

## Running
```
$ make docker-run-master
```
```
$ make docker-run-worker1
```
```
$ make docker-run-worker2
```

## Developing in pycharm
1. Start development stack
```$ make docker-stack-up```
2. Create remote interpreter using `distribrewed/core_dev` image
3. Enable django support
4. Create new run configuration
    * Host: `0.0.0.0`
    * Set links to development stack in container settings:
        * coredev_rabbitmq_1 -> rabbitmq
        * coredev_postgres_1 -> postgres