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

    int width = cap.get(CV_CAP_PROP_FRAME_WIDTH); 
    int height = cap.get(CV_CAP_PROP_FRAME_HEIGHT); 
    int hcenter = width / 2;
    int vcenter = height / 2;

    cv::Mat cross(height, width, CV_8UC3);
    line(cross, cv::Point(hcenter, 0), cv::Point(hcenter, height), cv::Scalar(0, 255, 0));
    line(cross, cv::Point(0, vcenter), cv::Point(width, vcenter), cv::Scalar(0, 255, 0));

    //line thickness is broken, double line used instead
    if (width % 2 == 0)
    {
        line(cross, cv::Point(hcenter + 1, 0), cv::Point(hcenter + 1, height), cv::Scalar(0, 255, 0));
    }
    if (height % 2 == 0)
    {
        line(cross, cv::Point(0, vcenter + 1), cv::Point(width, vcenter + 1), cv::Scalar(0, 255, 0));
    }

    cv::Mat frame;
    while (cv::waitKey(33) != 27) //30 FPS, escape key to exit
    {
        cap >> frame;
        if (frame.empty())
        {
            std::cerr << "Error while taking snapshot\n";
            break;
        }

        double alpha = 0.25;
        cv::addWeighted(cross, alpha, frame, 1.0 - alpha, 0.0, frame);

        imshow("Calibration", frame);
    }

    return 0;
}
