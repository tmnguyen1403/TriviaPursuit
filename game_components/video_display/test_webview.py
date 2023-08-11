import pygame
import webview
import time
import multiprocessing

def start_video(video_url):
    #ChatGPT reference
    html = """
        <html>
            <head>
                <style>
                img {
                    max-width: 300px;
                    max-height: 200px;
                }
            </style>
        <head/>
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
            <p>Hello image</p>
            <img src="https://www.splashlearn.com/math-vocabulary/wp-content/uploads/2022/05/isosceles_triangles-6-01.png" alt="Image">
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