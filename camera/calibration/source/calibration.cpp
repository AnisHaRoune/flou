#include <stdio.h>
#include <opencv2/opencv.hpp>

int main(int argc, char* argv[])
{
    cv::VideoCapture cap;

    if (!cap.open(0))
    {
        std::cerr << "Error while opening the camera\n";
        return -1;
    }

    std::cout << cap.get(CV_CAP_PROP_FOURCC) << "\n";
    cv::Mat frame;
    while (cv::waitKey(33) != 27) //30 FPS, escape key to exit
    {
        cap >> frame;
        if (frame.empty())
        {
            std::cerr << "Error while taking snapshot\n";
            break;
        }

        int width = frame.size().width; 
        int height = frame.size().height; 
        int hcenter = width / 2;
        int vcenter = height / 2;
        int hthickness = width % 2 == 0 ? 1 : 0;
        int vthickness = height % 2 == 0 ? 1 : 0;

        cv::Mat cross(frame.size());
        line(cross, cv::Point(hcenter, 0), cv::Point(hcenter, height), cv::Scalar(0, 255, 0), hthickness);
        line(cross, cv::Point(0, vcenter), cv::Point(width, vcenter), cv::Scalar(0, 255, 0), vthickness);

        cv::addWeighted(frame, 0.5, cross, 0.5, 0.0, frame);

        imshow("Calibration", frame);
    }

    return 0;
}
