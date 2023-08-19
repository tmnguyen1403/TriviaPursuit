from utils_local import is_mac, is_windows

# if is_mac():
#     import webview
# else:
#     print("Webview is probably not supported on this system. Media questions will no be displayed")
import multiprocessing

class MediaPlayer:
    def __init__(self):
        self.window = None
        self.webview_process = None
        self.is_playing = False

    def start_video(self, video_url):
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
        self.window = webview.create_window('Question Video', width=600, height=400,
                                            html=html)
        webview.start()

    def show_image(self, img_url):
        #ChatGPT reference
        html = """
            <html>
                <head>
                    <title>Question Image</title>
                <head/>
                <body>
                    <img src="IMAGE_HTML_SRC" width="560" height="315"
                </body>
            </html>
        """
        html = html.replace("IMAGE_HTML_SRC", img_url)
        self.window = webview.create_window('Question Image', width=600, height=400, html=html)
        webview.start()

    def reset_view(self):
        if self.webview_process != None and self.webview_process.is_alive():
            self.webview_process.kill()
        self.webview_process = None
        self.is_playing = False
        
    def start_webview(self,video_url):
        print(f"start webview at {video_url}")
        if self.webview_process != None and self.webview_process.is_alive():
            self.webview_process.kill()
            self.webview_process = None
            self.is_playing = False
        self.webview_process = multiprocessing.Process(target=self.start_video, args=(video_url,))
        self.webview_process.start()
        self.is_playing = True
        return True
    
    def start_imageview(self,image_url):
        print(f"start imageview at {image_url}")
        if self.webview_process != None and self.webview_process.is_alive():
            self.webview_process.kill()
            self.webview_process = None
            self.is_playing = False
        self.webview_process = multiprocessing.Process(target=self.show_image, args=(image_url,))
        self.webview_process.start()
        self.is_playing = True
        return True
    
    def play_video(self, video_url) -> bool:
        #self.screen = screen
        if self.webview_process and not self.webview_process.is_alive():
            print("Reset video")
            self.reset_view()

        if self.is_playing:
            print("Video is already playing")
            return False
        status = self.start_webview(video_url=video_url)
        return status
    
    def play_image(self, image_url) -> bool:
        if self.webview_process and not self.webview_process.is_alive():
            print("Reset view")
            self.reset_view()

        if self.is_playing:
            print("Image is already displayed")
            return False
        status = self.start_imageview(image_url=image_url)
        return status