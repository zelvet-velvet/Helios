I want to write a code, showing stream from tello with yolov5 torch model in real-time with low latency. I have a wierd version, storing objrcts detected frame and show it. I considered due to the process storing, the latency is pretty high and I need to delete every frame I showed after stream so it is not what I want. 
After I doing some research and asking question on forum, I have a blur code structure of what I want to do.

I think my code should be build like this:

1.    **connect tello**

2.    **to get tello's frame somehow**

3.    **throw frame in to model dealing with boxes and plot them on frame**

4.    **show the frame**


Since there have many ways to fulfill the purpose I want to done with webcam and opencv on the forum. I have tried many ways to use opencv's command ```cv2.VideoCapture()``` to get tello's stream. But till now, I haven't found any ways which is working for me.

I was stuck in how to convert frame's data type for a while. After I found out I need to deal with boxes in the out put of model() and plot them on frame. I am now stuck with the data type again. The thing I want to know is  how to make stream from Tello SDK 2.0 captured by opencv with  ```cv2.VideoCapture() ```.

Is there anyone has same issue and already found out how to deal with or any idea about what I am trying?

Appreciate anyone's response.
