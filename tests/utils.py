from models import Result, Activity


def create_result(tracking_type="personal"):
    return Result(
        distance=10.0,
        time=3000,
        tracking_type=tracking_type,
        pace=300,
        speed=12.0,
        distance_tag="10k"
    )


def create_activity(name="activity"):
    return Activity(
        user_id=1,
        month_id=1,
        year_id=1,
        name=name,
        type="running",
        description="a test",
        date="2023-11-22",
        results=[create_result()],
        environment="road",
        training_type="base",
        with_friends=0,
        distance_tag="10k"
    )


def get_result_json(tracking_type="personal"):
    return {
        "distance": 10.0,
        "time": 3000,
        "tracking_type": tracking_type,
        "url": None,
        "pace": 300,
        "speed": 12.0,
        "distance_tag": "10k"
    }


def get_activity_json(id=1, name="activity", tracking_type="personal"):
    return {
        "name": name,
        "type": "running",
        "description": "a test",
        "date": "2023-11-22",
        "environment": "road",
        "training_type": "base",
        "race_type": None,
        "with_friends": False,
        "id": id,
        "user_id": 1,
        "month_id": 1,
        "year_id": 1,
        "results": [
            get_result_json(tracking_type)
        ],
        "distance_tag": "10k",
        "event_id": None,
        "training_id": None
    }
