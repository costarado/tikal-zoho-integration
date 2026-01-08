"""
Сервисы для работы с различными модулями Tikal API
"""

from .calls import CallsService
from .recordings import RecordingsService
from .agents import AgentsService
from .statistics import StatisticsService
from .cdr import CDRService, CDRWebhookHandler

__all__ = [
    'CallsService',
    'RecordingsService',
    'AgentsService',
    'StatisticsService',
    'CDRService',
    'CDRWebhookHandler'
]

