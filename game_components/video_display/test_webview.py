import pygame
import webview
import time
import multiprocessing

# pygame.init()
# clock = pygame.time.Clock()


# def on_closed():
#     print("Call on_closed")
#     print("End on_closed")


# video_url = "https://www.youtube.com/embed/XnbCSboujF4"
# video_view = webview.create_window("Test webview", video_url)
# video_view.events.closed += on_closed
# screen = pygame.display.set_mode((1200, 800))

# running = True
# start = False
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:
#                 if not start:
#                     start = True
#                     webview.start(video_view)
#                 else:
#                     print("hello mouseclick")
#                     video_view.destroy()
#     screen.fill((125,0,255))
#     pygame.display.flip()
#     clock.tick(60)
# pygame.quit()

"""
This example demonstrates a user-provided "drag region" to move a frameless window
around, whilst maintaining normal mouse down/move events elsewhere. This roughly
replicates `-webkit-drag-region`.
"""


'''
For video question:
Question
    Watch video button:

No Question
    Watch video to hear the question


'''
# import webview


# def display_screen_info():
#     screens = webview.screens
#     print('Available screens are: ' + str(screens))


# if __name__ == '__main__':
#     display_screen_info()  # display screen info before starting app

#     window = webview.create_window('Simple browser', 'https://pywebview.flowrl.com/hello')
#     window.events.closing += lambda : print("Hello closing")
#     window.events.closed += lambda : print("Hello closed")
#     window.events.minimized += lambda : print("Hello minimized")
#     webview.start(display_screen_info)
def start_video(video_url):
    #ChatGPT reference
    html = """
        <html>
        <body>
            <iframe id="youtube_player" width="560" height="315" src="VIDEO_SRC" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
            <script>
            // This function stops the YouTube video when the window is closed
            function stopVideoOnWindowClose() {
                var player = document.getElementById('youtube_player');
                if (player) {
                    player.contentWindow.postMessage('{"event":"command","func":"stopVideo","args":""}', '*');
                }
            }

            // Attach the stopVideoOnWindowClose function to the beforeunload event
            window.addEventListener('beforeunload', function (event) {
                stopVideoOnWindowClose();
            });
        </script>
        </body>
        </html>
    """
    html = html.replace("VIDEO_SRC", video_url)
    window = webview.create_window('Close video when play', html=html)
    webview.start()

def start_webview(video_url):
    # ChatGPT reference
    # The comma "," in args is needed to break the args
    webview_process = multiprocessing.Process(target=start_video, args=(video_url,))
   
    return webview_process
    

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((1200, 800))

    running = True
    start = False
    video_url = "https://www.youtube.com/embed/XnbCSboujF4"
    video2 ="https://www.youtube.com/embed/NzjF1pdlK7Y"
    videos = [video_url, video2]
    video_index = 0
    webview_process = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not start:
                        if webview_process != None and webview_process.is_alive():
                            webview_process.kill()
                            webview_process = None
                        start = True
                        webview_process = start_webview(video_url=videos[(video_index+1)%2])
                        video_index += 1
                        webview_process.start()
                    else:
                        start = False
                        print("hello mouseclick")
        screen.fill((125,0,255))
        #print("hi")
        pygame.display.flip()
        clock.tick(60)
        if webview_process:
            alive = webview_process.is_alive()
            print(f"alive {alive}")
            if not alive:
                webview_process = None 
    pygame.quit()