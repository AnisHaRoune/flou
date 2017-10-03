#include <stdio.h>
#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>

void draw_cross(cv::Mat& frame, int width, int height, int hoffset = 0, int voffset = 0)
{
    int hcenter = (width / 2) + hoffset;
    int vcenter = (height / 2) + voffset;

    line(frame, cv::Point(hcenter, 0), cv::Point(hcenter, height), 255, 1);
    line(frame, cv::Point(0, vcenter), cv::Point(width, vcenter), 255, 1);
    //line thickness is imprecise, so it's doubled manually
    if (width % 2 == 0) 
    {
        line(frame, cv::Point(hcenter + 1, 0), cv::Point(hcenter + 1, height), 255, 1);
    }
    if (height % 2 == 0)
    {
        line(frame, cv::Point(0, vcenter + 1), cv::Point(width, vcenter + 1), 255, 1);
    }
}

void plot_roi(cv::Mat& frame, int x, int y, int width)
{
    std::ofstream points;
    points.open("plot/points.data", std::ios::trunc);

    for (int i = 0; i < width; i++)
    {
        points << i << "\t" << (int)frame.at<uint8_t>(y, x + i) << std::endl;
    }

    points.close();
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
    bool crosshairs = true;
    const int rect_width = 256;
    const int rect_height = 256;
    int voffset = 0;
    int hoffset = 0;
    while (true)
    {
        cap >> frame;
        if (frame.empty())
        {
            std::cerr << "Error while taking snapshot\n";
            break;
        }
        cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);

        int width = frame.size().width; 
        int height = frame.size().height; 
        int hcenter = (width / 2) + hoffset;
        int vcenter = (height / 2) + voffset;
        int rect_left = hcenter - (rect_width / 2);
        int rect_top = vcenter - (rect_height / 2);
        int rect_right = hcenter + (rect_width / 2);
        int rect_bottom = vcenter + (rect_height / 2);

        switch (cv::waitKey(33))
        {
            case ' ':
                crosshairs = !crosshairs;
                break;
            case '\n':
                plot_roi(frame, rect_left, vcenter, rect_width);
                break;
            case 84:
                voffset++; //down
                break;
            case 82: // up
                voffset--;
                break;
            case 81: //left
                hoffset--;
                break;
            case 83: //right
                hoffset++;
                break;
            case 27: //ESC
                return 0;
        }

        if (crosshairs)
        {
            draw_cross(frame, width, height, hoffset, voffset);
            cv::rectangle(frame, cv::Point(rect_left, rect_top), cv::Point(rect_right, rect_bottom), 255);
        }
        imshow("Calibration", frame);
    }

    return 0;
}
