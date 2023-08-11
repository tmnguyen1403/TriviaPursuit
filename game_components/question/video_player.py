import webview
import multiprocessing

class VideoPlayer:
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
        self.window = webview.create_window('Question Video', width=600, height=400, html=html)
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
    
    def play_video(self, video_url) -> bool:
        if self.webview_process and not self.webview_process.is_alive():
            print("Reset video")
            self.reset_view()

        if self.is_playing:
            print("Video is already playing")
            return False
        status = self.start_webview(video_url=video_url)
        return status