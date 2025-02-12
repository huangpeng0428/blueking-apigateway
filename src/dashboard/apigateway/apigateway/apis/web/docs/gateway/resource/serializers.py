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


class ResourceListInputSLZ(serializers.Serializer):
    stage_name = serializers.CharField()


class ResourceOutputSLZ(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = SerializerTranslatedField(
        translated_fields={"en": "description_en"}, allow_blank=True, read_only=True
    )
    method = serializers.CharField(read_only=True)
    path = serializers.CharField(read_only=True)
    verified_user_required = serializers.BooleanField(read_only=True)
    verified_app_required = serializers.BooleanField(read_only=True)
    resource_perm_required = serializers.BooleanField(read_only=True)
    labels = serializers.SerializerMethodField()

    class Meta:
        ref_name = "apigateway.apis.web.docs.gateway.resource"

    def get_labels(self, obj):
        return self.context["labels"].get(obj.id, [])
