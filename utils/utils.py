from schemas.activities import ActivityType, Activity
from schemas.results import DistanceTagRunning, DistanceTagSwimming, ResultBase, TrackingType, Goal


def calculate_pace(time: int, distance: float) -> int:
    return round(time / distance)


def calculate_speed(time: int, distance: float):
    return distance * 3600 / time


def get_activity_distance_tag(results: list[ResultBase], type: ActivityType):
    for result in results:
        if result.tracking_type == TrackingType.official:
            return get_distance_tag(result.distance, type)
        elif result.tracking_type == TrackingType.personal:
            return get_distance_tag(result.distance, type)
    return None


def get_distance_tag(distance: float, type: ActivityType):
    if type is ActivityType.running:
        if get_margin(5.0)[0] <= distance <= get_margin(5.0)[1]:
            return DistanceTagRunning.tag_5k_running
        if get_margin(10.0)[0] <= distance <= get_margin(10.0)[1]:
            return DistanceTagRunning.tag_10k_running
        if get_margin(15.0)[0] <= distance <= get_margin(15.0)[1]:
            return DistanceTagRunning.tag_15k_running
        if get_margin(21.1)[0] <= distance <= get_margin(21.1)[1]:
            return DistanceTagRunning.tag_21k_running
        if get_margin(30.0)[0] <= distance <= get_margin(30.0)[1]:
            return DistanceTagRunning.tag_30k_running
        if get_margin(42.2)[0] <= distance <= get_margin(42.2)[1]:
            return DistanceTagRunning.tag_42k_running
    elif type is ActivityType.swimming:
        if get_margin(0.250)[0] <= distance <= get_margin(0.250)[1]:
            return DistanceTagSwimming.tag_250_swimming
        if get_margin(0.500)[0] <= distance <= get_margin(0.500)[1]:
            return DistanceTagSwimming.tag_500_swimming
        if get_margin(1.0)[0] <= distance <= get_margin(1.0)[1]:
            return DistanceTagSwimming.tag_1000_swimming
        if get_margin(1.5)[0] <= distance <= get_margin(1.5)[1]:
            return DistanceTagSwimming.tag_1500_swimming
        if get_margin(2.0)[0] <= distance <= get_margin(2.0)[1]:
            return DistanceTagSwimming.tag_2000_swimming


def get_margin(number: float):
    return [number - number / 25, number + number / 25]


def sort_on_pace(activity: Activity):
    official_index, personal_index = get_official_and_personal_indices(activity)
    if official_index is not None:
        return activity.results[official_index].pace
    elif personal_index is not None:
        return activity.results[personal_index].pace


def get_official_and_personal_indices(activity: Activity):
    official_index = None
    personal_index = None

    for index, result in enumerate(activity.results):
        if result.tracking_type == TrackingType.official:
            official_index = index
        elif result.tracking_type == TrackingType.personal:
            personal_index = index

    return official_index, personal_index
