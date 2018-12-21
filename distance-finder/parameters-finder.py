from argparse import ArgumentParser
import math

def main():
    parser = ArgumentParser()
    parser.add_argument('distance_camera', type=float)
    parser.add_argument('angle_camera', type=float)
    parser.add_argument('filepath')
    parser.add_argument('--debug', '-d', action="store_true")
    args = parser.parse_args()

    angle_laser = (math.pi / 2) - args.angle_camera
    segment_camera = args.distance_camera * math.tan(args.angle_camera)

    print(angle_laser, segment_camera)


if __name__ == "__main__":
    main()
