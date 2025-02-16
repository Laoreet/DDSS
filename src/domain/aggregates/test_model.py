import unittest
from domain.aggregates.model_aggregate import (
    ModelAggregate,
    GetAttentionMapsCommand,
    GetModelResultCommand,
    AttentionMapBuildedEvent,
    ModelResultEvent,
)
from domain.entities.model import Model
from domain.entities.model_results import ModelResults
from domain.entities.attention_maps import AttentionMaps
from utils.base_uuid import BaseId


class TestModelAggregate(unittest.TestCase):
    def setUp(self):
        self.model_id = BaseId()
        self.ct_series_id = BaseId()

        self.model = Model(id=self.model_id)
        self.model_results = ModelResults()
        self.attention_maps = AttentionMaps()

        self.aggregate = ModelAggregate(
            model=self.model,
            model_results=self.model_results,
            attention_maps=self.attention_maps,
        )

    def test_handle_get_attention_maps_command(self):
        command = GetAttentionMapsCommand(
            ct_series_id=self.ct_series_id,
            model_id=self.model_id,
        )

        events = self.aggregate.handle(command)

        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], AttentionMapBuildedEvent)
        self.assertEqual(events[0].ct_series_id, self.ct_series_id)
        self.assertTrue(isinstance(events[0].attention_map_id, str))
        self.assertEqual(events[0].attention_map, "заглушка attention_map")

    def test_handle_get_model_result_command(self):
        command = GetModelResultCommand(
            ct_series_id=self.ct_series_id,
            model_id=self.model_id,
        )

        events = self.aggregate.handle(command)

        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], ModelResultEvent)
        self.assertEqual(events[0].model_id, self.model_id)
        self.assertEqual(events[0].ct_series_id, self.ct_series_id)
        self.assertEqual(events[0].hemorrhage_percent, 13.37)

    def test_handle_many_commands(self):
        commands = [
            GetAttentionMapsCommand(
                ct_series_id=self.ct_series_id,
                model_id=self.model_id,
            ),
            GetModelResultCommand(
                ct_series_id=self.ct_series_id,
                model_id=self.model_id,
            ),
        ]

        events = self.aggregate.handle_many(commands)

        self.assertEqual(len(events), 2)
        self.assertIsInstance(events[0], AttentionMapBuildedEvent)
        self.assertIsInstance(events[1], ModelResultEvent)


if __name__ == "__main__":
    unittest.main()
