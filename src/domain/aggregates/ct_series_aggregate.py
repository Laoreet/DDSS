from domain.entities.ct_series import CTSeries
from domain.entities.projections import Projections
from domain.entities.comment import Comment
from typing import List


class CTSeriesAggregate:
    def __init__(self, ct_series: CTSeries, projections: Projections = None,
                 comments: List[Comment] = None):
        self.ct_series = ct_series
        self.projections = projections
        self.comments = comments or []
