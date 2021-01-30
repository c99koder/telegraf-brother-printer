#!/usr/bin/python3

#  Copyright (C) 2021 Sam Steele
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import asyncio, json, sys
from brother import Brother, SnmpError, UnsupportedModel

async def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <hostname> [laser | ink]")
        sys.exit()
    host = sys.argv[1]
    kind = sys.argv[2] if len(sys.argv) > 2 else "laser"

    brother = Brother(host, kind=kind)
    try:
        await brother.async_update()
    except (ConnectionError, SnmpError, UnsupportedModel) as error:
        print(f"{error}")
        return

    brother.shutdown()

    if brother.available:
        print(json.dumps(brother.data, default=str))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()