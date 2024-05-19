from enum import Enum


class DistanceTagRunning(str, Enum):
    tag_5k_running = "5k"
    tag_10k_running = "10k"
    tag_15k_running = "15k"
    tag_21k_running = "half-marathon"
    tag_30k_running = "30k"
    tag_42k_running = "marathon"


class DistanceTagSwimming(str, Enum):
    tag_250_swimming = "250"
    tag_500_swimming = "500"
    tag_1000_swimming = "1000"
    tag_1500_swimming = "1500"
    tag_2000_swimming = "2000"


class ActivityType(str, Enum):
    running = "running"
    swimming = "swimming"


class TrackingType(str, Enum):
    personal = "personal"
    official = "official"
    split = "split"


class Terrain(str, Enum):
    road = "road"
    mixed = "mixed"
    trail = "trail"
    treadmill = "treadmill"


class Pool(str, Enum):
    pool_25m = "25m"
    pool_50m = "50m"
    open_waters = "open waters "


class TrainingTypeRunning(str, Enum):
    base = "base"
    high_effort = "high effort"
    interval = "interval"
    elevation_gain = "elevation gain"


class TrainingTypeSwimming(str, Enum):
    breaststroke = "breaststroke"
    crawl = "crawl"
    mixed = "mixed"


class RaceType(str, Enum):
    base = "base"
    high_effort = "high effort"
    fun = "fun"
