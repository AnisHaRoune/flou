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

    bool first_frame = true;
    int width, height, hcenter, vcenter;
    cv::Mat frame;
    int key = 0;
    do
    {
        cap >> frame;
        if (frame.empty())
        {
            std::cerr << "Error while taking snapshot\n";
            break;
        }
        if (first_frame)
        {
            width = frame.size().width; 
            height = frame.size().height; 
            hcenter = width / 2;
            vcenter = height / 2;
            first_frame = false;
        }

        key = cv::waitKey(33);
        switch (key)
        {
            case 84:
                vcenter++;
                break;
            case 82:
                vcenter--;
                break;
        }


        cv::Mat cross(frame.size(), frame.type());
        line(cross, cv::Point(hcenter, 0), cv::Point(hcenter, height), cv::Scalar(0, 255, 0), 1);
        line(cross, cv::Point(0, vcenter), cv::Point(width, vcenter), cv::Scalar(0, 255, 0), 1);
        //line thickness is imprecise, so it's doubled manually
        if (width % 2 == 0) 
        {
            line(cross, cv::Point(hcenter + 1, 0), cv::Point(hcenter + 1, height), cv::Scalar(0, 255, 0), 1);
        }
        if (height % 2 == 0)
        {
            line(cross, cv::Point(0, vcenter + 1), cv::Point(width, vcenter + 1), cv::Scalar(0, 255, 0), 1);
        }

        cv::addWeighted(frame, 0.5, cross, 0.5, 0.0, frame);

        imshow("Calibration", frame);
    }
    while (key != 27); //30 FPS, escape key to exit

    return 0;
}
