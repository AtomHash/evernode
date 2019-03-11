"""
    Test Controller
"""
from flask import request, current_app # noqa
from evernode.classes import JsonResponse, Render, Security, Email, UserAuth, FormData, Translator, JWT, Paginate, Fail2Ban # noqa
from evernode.decorators import middleware # noqa
from ..models import TestModel


class TestCtrl:

    @staticmethod
    def model_serialization_json():
        test_model = TestModel()
        test_model.name = "AtomHash"
        test_model.save()
        test_model.add('groups', {'1-h': 1})
        test_model_2 = TestModel.where_id(1)
        return JsonResponse(200, None, [test_model, test_model_2])
