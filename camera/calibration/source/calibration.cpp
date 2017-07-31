#include <stdio.h>
#include <opencv2/opencv.hpp>

void draw_cross(cv::Mat& frame, int voffset = 0)
{
    int width = frame.size().width; 
    int height = frame.size().height; 
    int hcenter = width / 2;
    int vcenter = (height / 2) + voffset;

    cv::Scalar line_color(0, 255, 0, 127);
    line(frame, cv::Point(hcenter, 0), cv::Point(hcenter, height), line_color, 1);
    line(frame, cv::Point(0, vcenter), cv::Point(width, vcenter), line_color, 1);
    //line thickness is imprecise, so it's doubled manually
    if (width % 2 == 0) 
    {
        line(frame, cv::Point(hcenter + 1, 0), cv::Point(hcenter + 1, height), line_color, 1);
    }
    if (height % 2 == 0)
    {
        line(frame, cv::Point(0, vcenter + 1), cv::Point(width, vcenter + 1), line_color, 1);
    }
}

int main(int argc, char* argv[])
{
    cv::VideoCapture cap;
    if (!cap.open(0))
    {
        std::cerr << "Error while opening the camera\n";
        return -1;
    }
    cap.set(CV_CAP_PROP_FRAME_WIDTH, 1280);
    cap.set(CV_CAP_PROP_FRAME_HEIGHT, 960);
    cap.set(CV_CAP_PROP_FPS, 25);

    cv::Mat frame;
    int voffset = 0;
    while (true)
    {
        cap >> frame;
        if (frame.empty())
        {
            std::cerr << "Error while taking snapshot\n";
            break;
        }

        draw_cross(frame, voffset);
        imshow("Calibration", frame);

        switch (cv::waitKey(33))
        {
            case 84:
                voffset++;
                break;
            case 82:
                voffset--;
                break;
            case 27:
                return 0;
        }
    }

    return 0;
}
