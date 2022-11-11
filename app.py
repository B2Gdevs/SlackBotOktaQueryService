import os
from slack_bolt.async_app import AsyncApp
from dotenv import load_dotenv
from pathlib import Path
from services import okta_service
from services import utility_service
from services.cache_service import BasicCache
import traceback


basic_cache = BasicCache()


load_dotenv(Path("configs") / ".env")


app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


# The registry is where query handling services will register their functions that
# to handle query related messages in the bot
# In my opinion, having the input specifing the service would allow for quite a bit
# scalability while maintaining roughly the same maintenance level
#
# {
#   'okta': {
#              'list': okta_service.list_employees,
#              'update': okta_service.update_employee,
#              'query': okta_service.query_employee,
#              'create': okta_service.create_employee
#            }
# }
#
# Which could correspond to a query protocol {verb} {service} {param1} {param2} ...
# and then further protocol support could be {verb} {service} {entity} {param1} ...
handler_registry = {**okta_service.get_handler_registry()}

# A default service could be used when the query protocol wasn't understood
# and try to discern what went wrong.  Like a documentation service or go beyond
# with a hueristic approach
DEFAULT_SERVICE = okta_service.SERVICE_NAME


@app.event("message")
async def message_channel(client, event, logger):
    """Listen for any messages the come and handle them appropriately.

    Parameters
    ----------
    client :
        The slack web client.
    event :
        The event that occurred in Slack.
    logger :
        The defualt python logger.
    """
    allowed_channel_type = "im"
    if "channel_type" in event \
        and (channel := event["channel_type"]) \
        and channel == allowed_channel_type:

        text = event["text"]
        channel = event["channel"]

        if not basic_cache["im_channel_id"]:
            basic_cache["im_channel_id"] = event["channel"]

        verb, query_params = utility_service.parse_chat_protocol(text)
        # TODO: Add an if statement here to support more chat services
        text = await handler_registry[DEFAULT_SERVICE][verb](query_params)
        await client.chat_postMessage(channel=channel, text=text)
    else:
        message = "Hey lets move this over to a direct conversation! Thanks!"
        await client.chat_postMessage(channel=channel, text=message)


@app.error
async def custom_error_handler(error, body, logger):
    """Handle any unhandled error and post the error to the user!

    Parameters
    ----------
    error :
        Any unhandled exception.
    body :
        The event that.
    logger :
        The logger used by Bolt and this application.
    """
    logger.exception(f"Error: {error}")

    error_string = f"I don't feel so good, can you check out my code?\n\n{traceback.format_exc()}"

    await app.client.chat_postMessage(channel=basic_cache["im_channel_id"], text=error_string)


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))