from models import Result, Activity, Untraceable


def create_result(tracking_type="personal"):
    return Result(
        distance=10.0,
        time=3000,
        tracking_type=tracking_type,
        pace=300,
        speed=12.0,
        distance_tag="10k"
    )


def create_activity(name="activity", date="2023-11-22"):
    return Activity(
        user_id=1,
        month_id=1,
        year_id=1,
        name=name,
        type="running",
        description="a test",
        date=date,
        results=[create_result()],
        environment="road",
        training_type="base",
        with_friends=0,
        distance_tag="10k"
    )


def create_untraceable(name="untraceable 1"):
    return Untraceable(
        user_id=1,
        name=name,
        description="test untraceables",
        dates=["2023-11-22", "2023-11-23"]
    )


def get_untraceables_json(names):
    return [
        {
            'dates': [
                '2023-11-22',
                '2023-11-23',
            ],
            'description': 'test untraceables',
            'id': count + 1,
            'name': name,
            'user_id': 1,
        } for count, name in enumerate(names)
    ]


def get_untraceable_json(id=1, name="untraceable 1", dates=None):
    if dates is None:
        dates = ['2023-11-22',
                 '2023-11-23', ]
    return {
        'dates': dates,
        'description': 'test untraceables',
        'id': id,
        'name': name,
        'user_id': 1,
    }


def get_user_json(id=1, user_name="user 1"):
    return {
        "id": id,
        "user_name": user_name,
        "activities": [],
        "untraceables": [],
        "events": [],
        "trainings": [],
    }


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


def get_activity_json(id=1, name="activity", tracking_type="personal", date="2023-11-22"):
    return {
        "name": name,
        "type": "running",
        "description": "a test",
        "date": date,
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


def get_stats_json():
    return {
        'best_efforts': {
            '10k': [
                {
                    'date': '2023-11-22',
                    'description': 'a test',
                    'distance_tag': '10k',
                    'environment': 'road',
                    'event_id': None,
                    'id': 1,
                    'month_id': 1,
                    'name': 'activity 1',
                    'race_type': None,
                    'results': [
                        {
                            'distance': 10.0,
                            'distance_tag': '10k',
                            'pace': 300,
                            'speed': 12.0,
                            'time': 3000,
                            'tracking_type': 'personal',
                            'url': None,
                        },
                    ],
                    'training_id': None,
                    'training_type': 'base',
                    'type': 'running',
                    'user_id': 1,
                    'with_friends': False,
                    'year_id': 1,
                },
                {
                    'date': '2023-11-23',
                    'description': 'a test',
                    'distance_tag': '10k',
                    'environment': 'road',
                    'event_id': None,
                    'id': 2,
                    'month_id': 1,
                    'name': 'activity 2',
                    'race_type': None,
                    'results': [
                        {
                            'distance': 10.0,
                            'distance_tag': '10k',
                            'pace': 300,
                            'speed': 12.0,
                            'time': 3000,
                            'tracking_type': 'personal',
                            'url': None,
                        },
                    ],
                    'training_id': None,
                    'training_type': 'base',
                    'type': 'running',
                    'user_id': 1,
                    'with_friends': False,
                    'year_id': 1,
                },
                {
                    'date': '2023-12-22',
                    'description': 'a test',
                    'distance_tag': '10k',
                    'environment': 'road',
                    'event_id': None,
                    'id': 3,
                    'month_id': 2,
                    'name': 'activity 3',
                    'race_type': None,
                    'results': [
                        {
                            'distance': 10.0,
                            'distance_tag': '10k',
                            'pace': 300,
                            'speed': 12.0,
                            'time': 3000,
                            'tracking_type': 'personal',
                            'url': None,
                        },
                    ],
                    'training_id': None,
                    'training_type': 'base',
                    'type': 'running',
                    'user_id': 1,
                    'with_friends': False,
                    'year_id': 1,
                },
                {
                    'date': '2024-11-22',
                    'description': 'a test',
                    'distance_tag': '10k',
                    'environment': 'road',
                    'event_id': None,
                    'id': 4,
                    'month_id': 3,
                    'name': 'activity 4',
                    'race_type': None,
                    'results': [
                        {
                            'distance': 10.0,
                            'distance_tag': '10k',
                            'pace': 300,
                            'speed': 12.0,
                            'time': 3000,
                            'tracking_type': 'personal',
                            'url': None,
                        },
                    ],
                    'training_id': None,
                    'training_type': 'base',
                    'type': 'running',
                    'user_id': 1,
                    'with_friends': False,
                    'year_id': 2,
                },
            ],
            '15k': [],
            '30k': [],
            '5k': [],
            'half-marathon': [],
            'marathon': [],
        },
        'monthly': [
            {
                'activities': [
                    {
                        'date': '2023-11-22',
                        'description': 'a test',
                        'distance_tag': '10k',
                        'environment': 'road',
                        'event_id': None,
                        'id': 1,
                        'month_id': 1,
                        'name': 'activity 1',
                        'race_type': None,
                        'results': [
                            {
                                'distance': 10.0,
                                'distance_tag': '10k',
                                'pace': 300,
                                'speed': 12.0,
                                'time': 3000,
                                'tracking_type': 'personal',
                                'url': None,
                            },
                        ],
                        'training_id': None,
                        'training_type': 'base',
                        'type': 'running',
                        'user_id': 1,
                        'with_friends': False,
                        'year_id': 1,
                    },
                    {
                        'date': '2023-11-23',
                        'description': 'a test',
                        'distance_tag': '10k',
                        'environment': 'road',
                        'event_id': None,
                        'id': 2,
                        'month_id': 1,
                        'name': 'activity 2',
                        'race_type': None,
                        'results': [
                            {
                                'distance': 10.0,
                                'distance_tag': '10k',
                                'pace': 300,
                                'speed': 12.0,
                                'time': 3000,
                                'tracking_type': 'personal',
                                'url': None,
                            },
                        ],
                        'training_id': None,
                        'training_type': 'base',
                        'type': 'running',
                        'user_id': 1,
                        'with_friends': False,
                        'year_id': 1,
                    },
                ],
                'activity_type': 'running',
                'month': '2023-11',
                'total_distance': 20.0,
                'total_time': 6000,
            },
            {
                'activities': [
                    {
                        'date': '2023-12-22',
                        'description': 'a test',
                        'distance_tag': '10k',
                        'environment': 'road',
                        'event_id': None,
                        'id': 3,
                        'month_id': 2,
                        'name': 'activity 3',
                        'race_type': None,
                        'results': [
                            {
                                'distance': 10.0,
                                'distance_tag': '10k',
                                'pace': 300,
                                'speed': 12.0,
                                'time': 3000,
                                'tracking_type': 'personal',
                                'url': None,
                            },
                        ],
                        'training_id': None,
                        'training_type': 'base',
                        'type': 'running',
                        'user_id': 1,
                        'with_friends': False,
                        'year_id': 1,
                    },
                ],
                'activity_type': 'running',
                'month': '2023-12',
                'total_distance': 10.0,
                'total_time': 3000,
            },
            {
                'activities': [
                    {
                        'date': '2024-11-22',
                        'description': 'a test',
                        'distance_tag': '10k',
                        'environment': 'road',
                        'event_id': None,
                        'id': 4,
                        'month_id': 3,
                        'name': 'activity 4',
                        'race_type': None,
                        'results': [
                            {
                                'distance': 10.0,
                                'distance_tag': '10k',
                                'pace': 300,
                                'speed': 12.0,
                                'time': 3000,
                                'tracking_type': 'personal',
                                'url': None,
                            },
                        ],
                        'training_id': None,
                        'training_type': 'base',
                        'type': 'running',
                        'user_id': 1,
                        'with_friends': False,
                        'year_id': 2,
                    },
                ],
                'activity_type': 'running',
                'month': '2024-11',
                'total_distance': 10.0,
                'total_time': 3000,
            },
        ],
        'yearly': [
            {
                'activities': [
                    {
                        'date': '2023-11-22',
                        'description': 'a test',
                        'distance_tag': '10k',
                        'environment': 'road',
                        'event_id': None,
                        'id': 1,
                        'month_id': 1,
                        'name': 'activity 1',
                        'race_type': None,
                        'results': [
                            {
                                'distance': 10.0,
                                'distance_tag': '10k',
                                'pace': 300,
                                'speed': 12.0,
                                'time': 3000,
                                'tracking_type': 'personal',
                                'url': None,
                            },
                        ],
                        'training_id': None,
                        'training_type': 'base',
                        'type': 'running',
                        'user_id': 1,
                        'with_friends': False,
                        'year_id': 1,
                    },
                    {
                        'date': '2023-11-23',
                        'description': 'a test',
                        'distance_tag': '10k',
                        'environment': 'road',
                        'event_id': None,
                        'id': 2,
                        'month_id': 1,
                        'name': 'activity 2',
                        'race_type': None,
                        'results': [
                            {
                                'distance': 10.0,
                                'distance_tag': '10k',
                                'pace': 300,
                                'speed': 12.0,
                                'time': 3000,
                                'tracking_type': 'personal',
                                'url': None,
                            },
                        ],
                        'training_id': None,
                        'training_type': 'base',
                        'type': 'running',
                        'user_id': 1,
                        'with_friends': False,
                        'year_id': 1,
                    },
                    {
                        'date': '2023-12-22',
                        'description': 'a test',
                        'distance_tag': '10k',
                        'environment': 'road',
                        'event_id': None,
                        'id': 3,
                        'month_id': 2,
                        'name': 'activity 3',
                        'race_type': None,
                        'results': [
                            {
                                'distance': 10.0,
                                'distance_tag': '10k',
                                'pace': 300,
                                'speed': 12.0,
                                'time': 3000,
                                'tracking_type': 'personal',
                                'url': None,
                            },
                        ],
                        'training_id': None,
                        'training_type': 'base',
                        'type': 'running',
                        'user_id': 1,
                        'with_friends': False,
                        'year_id': 1,
                    },
                ],
                'activity_type': 'running',
                'total_distance': 30.0,
                'total_time': 9000,
                'year': '2023',
            },
            {
                'activities': [
                    {
                        'date': '2024-11-22',
                        'description': 'a test',
                        'distance_tag': '10k',
                        'environment': 'road',
                        'event_id': None,
                        'id': 4,
                        'month_id': 3,
                        'name': 'activity 4',
                        'race_type': None,
                        'results': [
                            {
                                'distance': 10.0,
                                'distance_tag': '10k',
                                'pace': 300,
                                'speed': 12.0,
                                'time': 3000,
                                'tracking_type': 'personal',
                                'url': None,
                            },
                        ],
                        'training_id': None,
                        'training_type': 'base',
                        'type': 'running',
                        'user_id': 1,
                        'with_friends': False,
                        'year_id': 2,
                    },
                ],
                'activity_type': 'running',
                'total_distance': 10.0,
                'total_time': 3000,
                'year': '2024',
            }
        ]
    }
