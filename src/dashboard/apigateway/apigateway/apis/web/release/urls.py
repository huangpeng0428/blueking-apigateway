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
from django.urls import include, path

from .views import (
    PublishEventsRetrieveAPI,
    ReleaseAvailableResourceListApi,
    ReleaseCreateApi,
    ReleasedResourceRetrieveApi,
    ReleaseHistoryListApi,
    ReleaseHistoryRetrieveApi,
)

urlpatterns = [
    path("", ReleaseCreateApi.as_view(), name="gateway.release.create"),
    path(
        "stages/<int:stage_id>/available_resources/",
        ReleaseAvailableResourceListApi.as_view(),
        name="gateway.releases.available_resources",
    ),
    path(
        "histories/",
        include(
            [
                path("", ReleaseHistoryListApi.as_view(), name="gateway.release_histories.list"),
                path("latest/", ReleaseHistoryRetrieveApi.as_view(), name="gateway.release_histories.retrieve_latest"),
            ]
        ),
    ),
    path(
        "resource-versions/<int:resource_version_id>/resources/<int:resource_id>/",
        ReleasedResourceRetrieveApi.as_view(),
        name="gateway.releases.released-resource.detail",
    ),
    path("publish/<int:publish_id>/events/", PublishEventsRetrieveAPI.as_view(), name="gateway.publish.events"),
]
