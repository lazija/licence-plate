import sys
from alprstream import AlprStream
from openalpr import Alpr
from vehicleclassifier import VehicleClassifier

# Initialize instances
alpr = Alpr("eu", "C:/Users/princ/Desktop/KOD/realtimeplates/openalpr.conf", "C:/Users/princ/Desktop/KOD/realtimeplates/runtime_data")
if not alpr.is_loaded():
    print('Error loading Alpr')
    sys.exit(1)
alpr_stream = AlprStream(frame_queue_size=10, use_motion_detection=True)
if not alpr_stream.is_loaded():
    print('Error loading AlprStream')
    sys.exit(1)
vehicle = VehicleClassifier("C:/Users/princ/Desktop/KOD/realtimeplates/openalpr.conf", "C:/Users/princ/Desktop/KOD/realtimeplates/runtime_data")
if not vehicle.is_loaded():
    print('Error loading VehicleClassifier')
    sys.exit(1)

# Connect to stream/video and process results
alpr_stream.connect_video_file('/path/to/video.mp4', 0)
while alpr_stream.video_file_active() or alpr_stream.get_queue_size() > 0:
    single_frame = alpr_stream.process_frame(alpr)
    active_groups = len(alpr_stream.peek_active_groups())
    print('Active groups: {:<3} \tQueue size: {}'.format(active_groups, alpr_stream.get_queue_size()))
    groups = alpr_stream.pop_completed_groups_and_recognize_vehicle(vehicle)
    for group in groups:
        print('=' * 40)
        print('Group from frames {}-{}'.format(group['frame_start'], group['frame_end']))
        print('Plate: {} ({:.2f}%)'.format(group['best_plate']['plate'], group['best_plate']['confidence']))
        print('Vehicle attributes')
        for attribute, candidates in group['vehicle'].items():
            print('\t{}: {} ({:.2f}%)'.format(attribute.capitalize(), candidates[0]['name'], candidates[0]['confidence']))
        print('=' * 40)

# Call when completely done to release memory
alpr.unload()
vehicle.unload()