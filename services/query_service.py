# services/query_service.py

from services.database import query_all, query_by_object


def show_all_events():
    events = query_all()
    print("\n--- ALL EVENTS ---")
    for e in events:
        print(e)


def show_by_object(obj):
    events = query_by_object(obj)
    print(f"\n--- EVENTS FOR: {obj.upper()} ---")
    for e in events:
        print(e)