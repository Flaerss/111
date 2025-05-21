from aiohttp import web
from notifier import send_notification

routes = web.RouteTableDef()

@routes.post("/webhook")
async def handle_webhook(request):
    data = await request.json()
    try:
        client_name = data.get("client", {}).get("name", "Неизвестно")
        visit_date = data.get("date", "не указана дата")
        event_type = data.get("event", "created")

        if event_type == "created":
            await send_notification("new", client_name, visit_date)
        elif event_type == "updated":
            await send_notification("rescheduled", client_name, visit_date)
        elif event_type == "deleted":
            await send_notification("cancelled", client_name, visit_date)

        return web.Response(text="OK")
    except Exception as e:
        print(f"Ошибка в вебхуке: {e}")
        return web.Response(status=500, text="Ошибка")