from unittest import TestCase

from distribrewed_core.routes import route_task


class Tests(TestCase):
    def test_route_to_worker(self):
        route = route_task(
            'distribrewed_core.tasks.worker.call_method_by_name',
            None,
            None,
            {'worker_id': 'test_worker'}
        )

        self.assertEqual(
            route,
            {
                'exchange': 'worker.test_worker',
                'routing_key': 'worker.test_worker',
                'exchange_type': 'topic'
            }
        )

    def test_route_to_all_workers(self):
        route = route_task(
            'distribrewed_core.tasks.worker.call_method_by_name',
            None,
            None,
            {'all_workers': True}
        )

        self.assertEqual(
            route,
            {
                'exchange': 'worker.all',
                'routing_key': 'worker.all',
                'exchange_type': 'topic'
            }
        )

    def test_route_to_master(self):
        route = route_task(
            'distribrewed_core.tasks.master.call_method_by_name',
            None,
            None,
            {}
        )

        self.assertEqual(
            route,
            {
                'exchange': 'master',
                'routing_key': 'master',
                'exchange_type': 'topic'
            }
        )
