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
from rest_framework import serializers
from tencent_apigateway_common.i18n.field import SerializerTranslatedField

from apigateway.biz.gateway import GatewayHandler
from apigateway.biz.gateway_type import GatewayTypeHandler


class GatewayOutputSLZ(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = SerializerTranslatedField(default_field="description_i18n", allow_blank=True)
    maintainers = serializers.ListField()
    is_official = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()

    def get_api_url(self, obj):
        return GatewayHandler.get_api_domain(obj)

    def get_is_official(self, obj):
        return GatewayTypeHandler.is_official(self.context["gateway_auth_configs"][obj.id].gateway_type)
