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

from apigateway.apis.web.constants import ExportTypeEnum
from apigateway.apps.support.constants import DocArchiveTypeEnum, DocLanguageEnum


class DocArchiveParseInputSLZ(serializers.Serializer):
    file = serializers.FileField(required=True, help_text="导入的归档文档文件")


class ArchiveParseOutputResourceSLZ(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    method = serializers.CharField(read_only=True)
    path = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)


class ArchiveParseOutputResourceDocSLZ(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    language = serializers.CharField(read_only=True)


class DocArchiveParseOutputSLZ(serializers.Serializer):
    filename = serializers.CharField(read_only=True)
    language = serializers.CharField(source="language.value", read_only=True)
    content_changed = serializers.BooleanField(read_only=True)
    resource = ArchiveParseOutputResourceSLZ(allow_null=True, read_only=True)
    resource_doc = ArchiveParseOutputResourceDocSLZ(allow_null=True, read_only=True)


class SelectedResourceDocSLZ(serializers.Serializer):
    language = serializers.ChoiceField(choices=DocLanguageEnum.get_choices())
    resource_name = serializers.CharField()


class DocImportByArchiveInputSLZ(serializers.Serializer):
    selected_resource_docs = serializers.JSONField(binary=True)
    file = serializers.FileField(required=True, help_text="导入的归档文档文件")

    def validate_selected_resource_docs(self, value):
        slz = SelectedResourceDocSLZ(data=value, many=True)
        slz.is_valid(raise_exception=True)
        return slz.validated_data


class DocImportBySwaggerInputSLZ(serializers.Serializer):
    selected_resource_docs = serializers.ListField(child=SelectedResourceDocSLZ(), allow_empty=False)
    language = serializers.ChoiceField(choices=DocLanguageEnum.get_choices())
    swagger = serializers.CharField()


class ResourceFilterConditionSLZ(serializers.Serializer):
    """导出资源文档时，当导出类型为：已筛选资源时，此处为筛选条件"""

    name = serializers.CharField(allow_blank=True, required=False)
    path = serializers.CharField(allow_blank=True, required=False)
    method = serializers.CharField(allow_blank=True, required=False)
    label_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    backend_id = serializers.IntegerField(allow_null=True, required=False)
    query = serializers.CharField(allow_blank=True, required=False)


class DocExportInputSLZ(serializers.Serializer):
    export_type = serializers.ChoiceField(
        choices=ExportTypeEnum.get_choices(),
        help_text="值为 all，不需其它参数；值为 filtered，支持 query/path/method/label_name 参数；值为 selected，支持 resource_ids 参数",
    )
    file_type = serializers.ChoiceField(choices=DocArchiveTypeEnum.get_choices(), default=DocArchiveTypeEnum.ZIP.value)
    resource_filter_condition = ResourceFilterConditionSLZ(required=False)
    resource_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=True, required=False)
