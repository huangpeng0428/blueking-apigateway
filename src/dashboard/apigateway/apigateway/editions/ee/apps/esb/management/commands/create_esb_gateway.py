# -*- coding: utf-8 -*-
#
# TencentBlueKing is pleased to support the open source community by making
# 蓝鲸智云 - API 网关(BlueKing - APIGateway) available.
# Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.
#
# We undertake not to change the open source license (MIT license) applicable
# to the current version of the project delivered to anyone in the future.
#
"""
创建 esb 相关网关，如 bk-esb、apigw
"""
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apigateway.apis.open.gateway.serializers import GatewaySyncSLZ
from apigateway.core.models import Gateway
from apigateway.utils.django import get_object_or_None

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=False)

    @transaction.atomic
    def handle(self, dry_run: bool, *args, **options):
        for name, config in getattr(settings, "SYNC_ESB_JWT_KEY_GATEWAY_NAMES", {}).items():
            gateway = get_object_or_None(Gateway, name=name)
            if gateway:
                logger.info("gateway [name=%s] already exists, skip", name)
                continue

            if not dry_run:
                slz = GatewaySyncSLZ(
                    data=dict(config, name=name),
                    context={
                        "bk_app_code": settings.BK_APP_CODE,
                    },
                )
                slz.is_valid(raise_exception=True)
                slz.save(created_by="admin", updated_by="admin")

        logger.info("create esb gateway [name=%s]", name)
