from backend.app.services.history_service import history_service
from backend.app.analyzer.traffic_analyzer import traffic_analyzer


records = history_service.get_latest(100)


for record in records:

    result = traffic_analyzer.analyze(record)

    print("=" * 70)

    print(
        f"URL      : {record['request']['url']}"
    )

    print(
        f"METHOD   : {record['request']['method']}"
    )

    print(
        f"PRIORITY : {result['priority']}"
    )

    print(
        f"REASONS  : {result['reasons']}"
    )