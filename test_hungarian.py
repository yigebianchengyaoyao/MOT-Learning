from tracker.track import Track

from tracker.association import (
    associate_detections_to_tracks
)


tracks = [

    Track(
        [100, 100, 200, 300],
        1
    ),

    Track(
        [400, 100, 500, 300],
        2
    )

]


detections = [

    [110, 105, 210, 305],

    [410, 105, 510, 305]

]


matches, unmatched_dets, unmatched_tracks = (
    associate_detections_to_tracks(
        detections,
        tracks
    )
)


print(
    "匹配结果:",
    matches
)

print(
    "未匹配检测:",
    unmatched_dets
)

print(
    "未匹配轨迹:",
    unmatched_tracks
)