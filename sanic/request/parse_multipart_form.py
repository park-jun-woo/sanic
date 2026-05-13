# ff:func feature=request type=parser control=iteration dimension=1
# ff:what Parse a multipart form request body into fields and files RequestPara

from __future__ import annotations

import email.utils
import unicodedata

from urllib.parse import unquote

from sanic.headers import parse_content_header
from sanic.log import logger
from sanic.request.file import File
from sanic.request.parameters import RequestParameters


def parse_multipart_form(body, boundary):
    """Parse a request body and returns fields and files

    Args:
        body (bytes): Bytes request body.
        boundary (bytes): Bytes multipart boundary.

    Returns:
        tuple[RequestParameters, RequestParameters]: A tuple containing fields and files as `RequestParameters`.
    """  # noqa: E501

    def _extract_filename(form_parameters):
        file_name = form_parameters.get("filename")
        if file_name is None and form_parameters.get("filename*"):
            encoding, _, value = email.utils.decode_rfc2231(
                form_parameters["filename*"]
            )
            file_name = unquote(value, encoding=encoding)
        if file_name is not None:
            file_name = unicodedata.normalize("NFC", file_name)
        return file_name

    def _parse_headers(form_part):
        file_name = None
        content_type = "text/plain"
        content_charset = "utf-8"
        field_name = None
        line_index = 2
        line_end_index = 0
        while not line_end_index == -1:
            line_end_index = form_part.find(b"\r\n", line_index)
            form_line = form_part[line_index:line_end_index].decode("utf-8")
            line_index = line_end_index + 2
            if not form_line:
                break
            colon_index = form_line.index(":")
            form_header_field = form_line[0:colon_index].lower()
            form_header_value, form_parameters = parse_content_header(
                form_line[colon_index + 2 :]
            )
            if form_header_field == "content-disposition":
                field_name = form_parameters.get("name")
                file_name = _extract_filename(form_parameters)
            elif form_header_field == "content-type":
                content_type = form_header_value
                content_charset = form_parameters.get("charset", "utf-8")
        return field_name, file_name, content_type, content_charset, line_index

    def _parse_form_part(form_part, fields, files):
        field_name, file_name, content_type, content_charset, line_index = (
            _parse_headers(form_part)
        )
        if not field_name:
            logger.debug(
                "Form-data field does not have a 'name' parameter "
                "in the Content-Disposition header"
            )
            return
        post_data = form_part[line_index:-4]
        if file_name is None:
            value = post_data.decode(content_charset)
            fields.setdefault(field_name, []).append(value)
        else:
            form_file = File(type=content_type, name=file_name, body=post_data)
            files.setdefault(field_name, []).append(form_file)

    files = {}
    fields = {}

    form_parts = body.split(boundary)
    for form_part in form_parts[1:-1]:
        _parse_form_part(form_part, fields, files)

    return RequestParameters(fields), RequestParameters(files)
