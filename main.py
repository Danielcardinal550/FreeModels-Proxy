import json
import re
import time
import uuid
from typing import Any

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse


# ============================================================
# CONFIG
# ============================================================

app = FastAPI()

UPSTREAM_URL = "https://freemodels-chat.freemodels.workers.dev/"

UPSTREAM_HEADERS = {
    "Accept": "text/event-stream",
    "Content-Type": "application/json",
    "Origin": "https://freemodels.pro",
    "Referer": "https://freemodels.pro/",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/131 Safari/537.36"
    ),
}


# ============================================================
# DEBUG
# ============================================================

DEBUG = True


def debug(title: str, data: Any = None):
    if not DEBUG:
        return

    print("\n" + "=" * 70)
    print(title)

    if data is not None:
        try:
            print(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=2
                )
            )
        except Exception:
            print(data)

    print("=" * 70)


# ============================================================
# CONTENT NORMALIZATION
# ============================================================

def normalize_content(content):

    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):

                item_type = item.get("type")

                if item_type == "text":
                    parts.append(
                        str(
                            item.get(
                                "text",
                                ""
                            )
                        )
                    )

                elif "text" in item:

                    text_value = item.get("text")

                    if isinstance(text_value, dict):
                        parts.append(
                            str(
                                text_value.get(
                                    "value",
                                    ""
                                )
                            )
                        )

                    else:
                        parts.append(
                            str(text_value)
                        )

        return "".join(parts)

    return str(content)


# ============================================================
# EXTRACT TOOLS FROM CHERRY STUDIO
# ============================================================

def extract_tools(data):

    tools = data.get(
        "tools",
        []
    )

    tool_map = {}

    for tool in tools:

        try:

            function = tool.get(
                "function",
                {}
            )

            real_name = function.get(
                "name",
                ""
            )

            if not real_name:
                continue

            short_name = real_name

            # نمونه:
            #
            # mcp__xxxxx__ls
            #
            # تبدیل می‌شود به:
            #
            # ls

            if "__" in real_name:

                short_name = (
                    real_name.split("__")[-1]
                )

            tool_map[
                short_name.lower()
            ] = real_name

            tool_map[
                real_name.lower()
            ] = real_name

        except Exception:
            continue

    return tool_map


# ============================================================
# NORMALIZE OPENAI MESSAGES
# ============================================================

def normalize_messages(messages):

    result = []

    for message in messages:

        role = message.get(
            "role",
            "user"
        )

        content = normalize_content(
            message.get(
                "content",
                ""
            )
        )

        # ----------------------------------------------------
        # TOOL RESULT
        # ----------------------------------------------------

        if role == "tool":

            tool_call_id = message.get(
                "tool_call_id",
                ""
            )

            tool_name = message.get(
                "name",
                "tool"
            )

            result.append(
                {
                    "role": "user",
                    "content": (
                        "<tool_result>\n"
                        f"tool: {tool_name}\n"
                        f"tool_call_id: {tool_call_id}\n"
                        f"{content}\n"
                        "</tool_result>\n\n"
                        "بر اساس نتیجه ابزار، "
                        "مرحله بعدی کار را ادامه بده. "
                        "اگر ابزار دیگری لازم است "
                        "از ابزار استفاده کن. "
                        "اگر کار تمام شده فقط در پایان "
                        "گزارش نهایی بده."
                    )
                }
            )

            continue

        # ----------------------------------------------------
        # ASSISTANT TOOL CALL HISTORY
        # ----------------------------------------------------

        if (
            role == "assistant"
            and message.get("tool_calls")
        ):

            tool_text = content

            for call in message.get(
                "tool_calls",
                []
            ):

                function = call.get(
                    "function",
                    {}
                )

                name = function.get(
                    "name",
                    ""
                )

                arguments = function.get(
                    "arguments",
                    "{}"
                )

                tool_text += (
                    "\n\n"
                    "<tool_call>"
                    f"{name}"
                    f"{arguments}"
                )

            result.append(
                {
                    "role": "assistant",
                    "content": tool_text
                }
            )

            continue

        # ----------------------------------------------------
        # NORMAL MESSAGE
        # ----------------------------------------------------

        result.append(
            {
                "role": role,
                "content": content
            }
        )

    return result


# ============================================================
# BUILD UPSTREAM PAYLOAD
# ============================================================

def build_upstream_payload(data):

    messages = normalize_messages(
        data.get(
            "messages",
            []
        )
    )

    requested_model = data.get(
        "model",
        "claude-sonnet-5"
    )

    # دستور سیستمی برای بهتر شدن Agent
    agent_instruction = (
        "\n\n"
        "دستور مهم برای حالت Agent:\n"
        "اگر نیاز به ابزار داری، ابزار را با یکی از "
        "فرمت‌های زیر فراخوانی کن.\n\n"
        "فرمت اول:\n"
        "<tool_call>نام_ابزار"
        "{\"argument\":\"value\"}\n\n"
        "مثال:\n"
        "<tool_call>ls"
        "{\"path\":\".\"}\n\n"
        "بعد از دریافت <tool_result>، "
        "خودت نتیجه را بررسی کن و کار را ادامه بده. "
        "تا زمانی که وظیفه کامل نشده متوقف نشو. "
        "اگر ابزار دیگری لازم است دوباره Tool Call ایجاد کن. "
        "فقط زمانی پاسخ نهایی بده که کار کاملاً تمام شده باشد."
    )

    # فقط برای درخواست‌هایی که پیام دارند
    if messages:

        # پیام آخر کاربر را تقویت می‌کنیم
        for message in reversed(messages):

            if message.get("role") == "user":

                message["content"] += (
                    agent_instruction
                )

                break

    return {
        "messages": messages,
        "modelId": requested_model,
        "thinking": False,
        "deepSearch": False,
        "stream": True
    }


# ============================================================
# OPENAI CHUNK
# ============================================================

def create_chunk(

    chunk_id,
    model,
    delta=None,
    finish_reason=None

):

    choice = {
        "index": 0,
        "delta": delta or {},
        "finish_reason": finish_reason
    }

    return {
        "id": chunk_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [
            choice
        ]
    }


# ============================================================
# PARSE TOOL CALL FORMAT:
#
# <tool_call>ls{"path":"."}
#
# OR
#
# <tool_call>mcp__xxx__ls{"path":"."}
# ============================================================

def parse_tag_tool_calls(
    text,
    tool_map
):

    results = []

    positions = []

    for match in re.finditer(
        r"<tool_call>",
        text,
        re.IGNORECASE
    ):

        positions.append(
            match.start()
        )

    if not positions:
        return results

    for index, start in enumerate(
        positions
    ):

        content_start = (
            start
            + len("<tool_call>")
        )

        if index + 1 < len(positions):

            end = positions[index + 1]

        else:

            end = len(text)

        block = text[
            content_start:end
        ].strip()

        # پیدا کردن اولین {
        json_start = block.find("{")

        if json_start == -1:
            continue

        name = block[
            :json_start
        ].strip()

        arguments_text = block[
            json_start:
        ].strip()

        # تلاش برای استخراج JSON واقعی
        decoder = json.JSONDecoder()

        try:

            arguments, json_end = (
                decoder.raw_decode(
                    arguments_text
                )
            )

            if not isinstance(
                arguments,
                dict
            ):
                continue

        except Exception:

            continue

        # تبدیل نام کوتاه به نام واقعی MCP
        real_name = resolve_tool_name(
            name,
            tool_map
        )

        results.append(
            {
                "id": (
                    "call_"
                    + uuid.uuid4().hex
                ),
                "type": "function",
                "function": {
                    "name": real_name,
                    "arguments": json.dumps(
                        arguments,
                        ensure_ascii=False
                    )
                }
            }
        )

    return results


# ============================================================
# PARSE JSON TOOL FORMAT:
#
# {
#   "tool": "ls",
#   "path": "."
# }
# ============================================================

def parse_json_tool_calls(
    text,
    tool_map
):

    results = []

    decoder = json.JSONDecoder()

    for match in re.finditer(
        r"\{",
        text
    ):

        start = match.start()

        try:

            obj, end = decoder.raw_decode(
                text[start:]
            )

        except Exception:

            continue

        if not isinstance(
            obj,
            dict
        ):
            continue

        tool_name = (
            obj.get("tool")
            or obj.get("function")
            or obj.get("name")
        )

        if not tool_name:
            continue

        # جلوگیری از تشخیص JSONهای معمولی
        if not isinstance(
            tool_name,
            str
        ):
            continue

        # حذف فیلد tool
        arguments = obj.copy()

        arguments.pop(
            "tool",
            None
        )

        arguments.pop(
            "function",
            None
        )

        arguments.pop(
            "name",
            None
        )

        real_name = resolve_tool_name(
            tool_name,
            tool_map
        )

        results.append(
            {
                "id": (
                    "call_"
                    + uuid.uuid4().hex
                ),
                "type": "function",
                "function": {
                    "name": real_name,
                    "arguments": json.dumps(
                        arguments,
                        ensure_ascii=False
                    )
                }
            }
        )

    return results


# ============================================================
# FIND REAL TOOL NAME
# ============================================================

def resolve_tool_name(
    model_name,
    tool_map
):

    name = model_name.strip()

    name_lower = name.lower()

    # نام دقیق
    if name_lower in tool_map:

        return tool_map[
            name_lower
        ]

    # اگر ابزار MCP باشد
    if "__" in name:

        short_name = (
            name.split("__")[-1]
        ).lower()

        if short_name in tool_map:

            return tool_map[
                short_name
            ]

    # ابزار کوتاه
    if name_lower in tool_map:

        return tool_map[
            name_lower
        ]

    # تلاش fuzzy
    for short_name, real_name in (
        tool_map.items()
    ):

        if short_name == name_lower:

            return real_name

    # اگر پیدا نشد همان نام
    return name


# ============================================================
# REMOVE TOOL CALL TEXT FROM VISIBLE OUTPUT
# ============================================================

def get_visible_text(text):

    # هر چیزی بعد از اولین tool_call
    if "<tool_call>" in text.lower():

        parts = re.split(
            r"<tool_call>",
            text,
            flags=re.IGNORECASE
        )

        return parts[0].strip()

    # اگر JSON tool پیدا شد
    # متن را نگه می‌داریم تا پاسخ خالی نشود
    return text.strip()


# ============================================================
# PARSE ALL TOOL CALLS
# ============================================================

def parse_all_tool_calls(
    text,
    tool_map
):

    tool_calls = []

    # روش 1
    tool_calls.extend(
        parse_tag_tool_calls(
            text,
            tool_map
        )
    )

    # اگر روش اول چیزی پیدا نکرد
    if not tool_calls:

        tool_calls.extend(
            parse_json_tool_calls(
                text,
                tool_map
            )
        )

    # حذف Toolهای تکراری
    unique_calls = []

    seen = set()

    for call in tool_calls:

        key = (
            call["function"]["name"],
            call["function"]["arguments"]
        )

        if key in seen:
            continue

        seen.add(key)

        unique_calls.append(
            call
        )

    return unique_calls


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():

    return {
        "status": "ok",
        "service": (
            "FreeModels "
            "OpenAI Agent Proxy"
        )
    }


# ============================================================
# MODELS
# ============================================================

@app.get("/v1/models")
async def models():

    model_list = [

        "claude-sonnet-5",

        "agnes-2.5-flash"

    ]

    return {

        "object": "list",

        "data": [

            {

                "id": model,

                "object": "model",

                "created": int(
                    time.time()
                ),

                "owned_by": (
                    "freemodels"
                )

            }

            for model in model_list

        ]

    }


# ============================================================
# STREAM RESPONSE
# ============================================================

async def stream_response(

    payload,
    requested_model,
    tool_map

):

    chunk_id = (
        "chatcmpl-"
        + uuid.uuid4().hex
    )

    full_content = ""

    debug(
        "UPSTREAM REQUEST",
        payload
    )

    debug(
        "AVAILABLE TOOLS",
        tool_map
    )

    async with httpx.AsyncClient(
        timeout=None
    ) as client:

        async with client.stream(

            "POST",

            UPSTREAM_URL,

            headers=UPSTREAM_HEADERS,

            json=payload

        ) as response:

            debug(
                "UPSTREAM STATUS",
                response.status_code
            )

            if response.status_code != 200:

                error = (
                    await response.aread()
                )

                error_text = (
                    error.decode(
                        "utf-8",
                        errors="ignore"
                    )
                )

                debug(
                    "UPSTREAM ERROR",
                    error_text
                )

                error_data = {

                    "error": {

                        "message":
                        error_text,

                        "type":
                        "upstream_error"

                    }

                }

                yield (
                    "data: "
                    + json.dumps(
                        error_data,
                        ensure_ascii=False
                    )
                    + "\n\n"
                )

                yield (
                    "data: [DONE]\n\n"
                )

                return

            async for line in (
                response.aiter_lines()
            ):

                if not line:
                    continue

                if not line.startswith(
                    "data:"
                ):
                    continue

                raw = (
                    line[5:].strip()
                )

                if raw == "[DONE]":

                    break

                try:

                    chunk = json.loads(
                        raw
                    )

                except Exception:

                    continue

                choices = chunk.get(
                    "choices",
                    []
                )

                if not choices:
                    continue

                choice = choices[0]

                delta = choice.get(
                    "delta",
                    {}
                )

                content = delta.get(
                    "content",
                    ""
                )

                if content:

                    full_content += (
                        content
                    )

    # --------------------------------------------------------
    # DEBUG FULL MODEL RESPONSE
    # --------------------------------------------------------

    debug(
        "FULL MODEL RESPONSE",
        full_content
    )

    # --------------------------------------------------------
    # FIND TOOL CALLS
    # --------------------------------------------------------

    tool_calls = (
        parse_all_tool_calls(
            full_content,
            tool_map
        )
    )

    debug(
        "PARSED TOOL CALLS",
        tool_calls
    )

    # --------------------------------------------------------
    # IF TOOL CALL EXISTS
    # --------------------------------------------------------

    if tool_calls:

        visible_text = (
            get_visible_text(
                full_content
            )
        )

        # متن قبل از Tool Call
        if visible_text:

            chunk = create_chunk(

                chunk_id,

                requested_model,

                {
                    "content":
                    visible_text
                }

            )

            yield (
                "data: "
                + json.dumps(
                    chunk,
                    ensure_ascii=False
                )
                + "\n\n"
            )

        # ----------------------------------------------------
        # ارسال Tool Calls
        # ----------------------------------------------------

        tool_call_delta = []

        for index, call in enumerate(
            tool_calls
        ):

            tool_call_delta.append(
                {

                    "index": index,

                    "id":
                    call["id"],

                    "type":
                    "function",

                    "function": {

                        "name":
                        call[
                            "function"
                        ][
                            "name"
                        ],

                        "arguments":
                        call[
                            "function"
                        ][
                            "arguments"
                        ]

                    }

                }
            )

        chunk = create_chunk(

            chunk_id,

            requested_model,

            {

                "tool_calls":
                tool_call_delta

            }

        )

        yield (
            "data: "
            + json.dumps(
                chunk,
                ensure_ascii=False
            )
            + "\n\n"
        )

        # پایان Tool Call
        finish_chunk = create_chunk(

            chunk_id,

            requested_model,

            {},

            "tool_calls"

        )

        yield (
            "data: "
            + json.dumps(
                finish_chunk,
                ensure_ascii=False
            )
            + "\n\n"
        )

        yield (
            "data: [DONE]\n\n"
        )

        return

    # --------------------------------------------------------
    # NORMAL RESPONSE
    # --------------------------------------------------------

    if full_content:

        chunk = create_chunk(

            chunk_id,

            requested_model,

            {

                "content":
                full_content

            }

        )

        yield (
            "data: "
            + json.dumps(
                chunk,
                ensure_ascii=False
            )
            + "\n\n"
        )

    finish_chunk = create_chunk(

        chunk_id,

        requested_model,

        {},

        "stop"

    )

    yield (
        "data: "
        + json.dumps(
            finish_chunk,
            ensure_ascii=False
        )
        + "\n\n"
    )

    yield (
        "data: [DONE]\n\n"
    )


# ============================================================
# CHAT COMPLETIONS
# ============================================================

@app.post(
    "/v1/chat/completions"
)
async def chat_completions(
    request: Request
):

    try:

        data = await request.json()

    except Exception:

        return JSONResponse(

            status_code=400,

            content={

                "error": {

                    "message":
                    "Invalid JSON request",

                    "type":
                    "invalid_request_error"

                }

            }

        )

    debug(
        "CHERRY STUDIO REQUEST",
        data
    )

    requested_model = data.get(
        "model",
        "claude-sonnet-5"
    )

    # --------------------------------------------------------
    # دریافت خودکار ابزارهای MCP
    # --------------------------------------------------------

    tool_map = extract_tools(
        data
    )

    payload = build_upstream_payload(
        data
    )

    return StreamingResponse(

        stream_response(

            payload,

            requested_model,

            tool_map

        ),

        media_type=(
            "text/event-stream"
        ),

        headers={

            "Cache-Control":
            "no-cache",

            "Connection":
            "keep-alive",

            "X-Accel-Buffering":
            "no"

        }

    )


# ============================================================
# NON STREAMING SUPPORT
# ============================================================

@app.post(
    "/chat/completions"
)
async def chat_completions_without_v1(
    request: Request
):

    return await chat_completions(
        request
    )

# ============================================================
# DIRECT START
# ============================================================

if __name__ == "__main__":
    import os
    import uvicorn

    host = os.getenv("FREEMODELS_HOST", "127.0.0.1")
    port = int(os.getenv("FREEMODELS_PORT", "8000"))

    print()
    print("=" * 70)
    print("FreeModels Proxy")
    print(f"Running on: http://{host}:{port}")
    print("Cherry Studio Base URL:")
    print(f"http://{host}:{port}/v1")
    print("Press Ctrl+C to stop.")
    print("=" * 70)
    print()

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
    )
