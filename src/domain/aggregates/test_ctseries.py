import unittest
from domain.entities.ct_series import CTSeries
from domain.entities.projections import Projections
from domain.aggregates.ct_series_aggregate import (
    CTSeriesAggregate,
    UploadCTSeriesCommand,
    AddCommentCommand,
    GetProjectionsCommand,
    CTSeriesUploadedEvent,
    CommentAddedEvent,
    ProjectionsBuildedEvent,
)
from utils.base_uuid import BaseId
from fastapi import UploadFile


class TestCTSeriesAggregate(unittest.TestCase):

    def setUp(self):
        self.ct_series_id = BaseId()
        self.patient_id = "patient-123"
        self.comment_id = BaseId()
        self.projection_id = BaseId()
        self.author = "Dr. Smith"
        self.content = "This is a comment."
        self.axial = "axial-data"
        self.sagital = "sagital-data"
        self.coronal = "coronal-data"

        self.ct_series = CTSeries(id=self.ct_series_id, patient_id=self.patient_id)
        self.projections = Projections()
        self.comments = []

        self.aggregate = CTSeriesAggregate(
            ct_series=self.ct_series,
            projections=self.projections,
            comments=self.comments,
        )

    def test_handle_upload_ct_series_command(self):
        command = UploadCTSeriesCommand(
            ct_series_id=self.ct_series_id,
            patient_id=self.patient_id,
            files=[UploadFile(filename="file1.dcm"), UploadFile(filename="file2.dcm")],
        )

        events = self.aggregate.handle(command)

        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], CTSeriesUploadedEvent)
        self.assertEqual(events[0].ct_series_id, self.ct_series_id)
        self.assertEqual(events[0].patient_id, self.patient_id)
        self.assertTrue(isinstance(events[0].upload_date, str))

    def test_handle_add_comment_command(self):
        command = AddCommentCommand(
            comment_id=self.comment_id,
            ct_series_id=self.ct_series_id,
            author=self.author,
            content=self.content,
        )

        events = self.aggregate.handle(command)

        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], CommentAddedEvent)
        self.assertEqual(events[0].ct_series_id, self.ct_series_id)
        self.assertEqual(events[0].comment_id, self.comment_id)
        self.assertEqual(events[0].author, self.author)
        self.assertEqual(events[0].content, self.content)
        self.assertTrue(isinstance(events[0].timestamp, str))

    def test_handle_get_projections_command(self):
        command = GetProjectionsCommand(
            ct_series_id=self.ct_series_id,
            projection_id=self.projection_id,
            axial=self.axial,
            sagital=self.sagital,
            coronal=self.coronal,
        )

        events = self.aggregate.handle(command)

        self.assertEqual(len(events), 1)
        self.assertIsInstance(events[0], ProjectionsBuildedEvent)
        self.assertEqual(events[0].ct_series_id, self.ct_series_id)
        self.assertEqual(events[0].projection_id, self.projection_id)
        self.assertEqual(events[0].axial, self.axial)
        self.assertEqual(events[0].sagital, self.sagital)
        self.assertEqual(events[0].coronal, self.coronal)

    def test_handle_many_commands(self):
        commands = [
            UploadCTSeriesCommand(
                ct_series_id=self.ct_series_id,
                patient_id=self.patient_id,
                files=[UploadFile(filename="file1.dcm"), UploadFile(filename="file2.dcm")],
            ),
            AddCommentCommand(
                comment_id=self.comment_id,
                ct_series_id=self.ct_series_id,
                author=self.author,
                content=self.content,
            ),
            GetProjectionsCommand(
                ct_series_id=self.ct_series_id,
                projection_id=self.projection_id,
                axial=self.axial,
                sagital=self.sagital,
                coronal=self.coronal,
            ),
        ]

        events = self.aggregate.handle_many(commands)

        self.assertEqual(len(events), 3)
        self.assertIsInstance(events[0], CTSeriesUploadedEvent)
        self.assertIsInstance(events[1], CommentAddedEvent)
        self.assertIsInstance(events[2], ProjectionsBuildedEvent)


if __name__ == "__main__":
    unittest.main()
