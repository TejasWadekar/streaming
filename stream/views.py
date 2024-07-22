# import os
import io
import os
from django.http import StreamingHttpResponse

# from azure.storage.blob import BlobClient
# from azure.storage.blob import BlobServiceClient
# from os import getenv
from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
)

from .services import (
    generate_video_stream,
    stream_video_to_tempfile,
)
from moviepy.editor import VideoFileClip, concatenate_videoclips

def render_video_stream(request):
    # context = {"candidate_id": candidate_id}
    return render(request, "streaming.html", locals())


# class StreamVideoView(APIView):
#     authentication_classes = [
#         SessionAuthentication,
#         BasicAuthentication,
#     ]  # Or leave empty for no authentication
#     permission_classes = [AllowAny]

#     def get(self, request):

#         try:
#             # candidate = Candidate.objects.get(pk=candidate_id)
#             # sessions = candidate.sessions
#             # if not sessions:
#             #     return Response(
#             #         {"error": "No sessions found for the candidate"},
#             #         status=status.HTTP_404_NOT_FOUND,
#             #     )

#             # session = sessions.latest("session_started_at")
#             urls = ["https://trakiotsolutions.blob.core.windows.net/agrodata/TrakIot%202/Aksh%20desh/139/739/965/recordingrecording_1721387473255.webm?se=2024-11-16T11%3A11%3A13Z&sp=r&sv=2024-05-04&sr=b&sig=y4Ffe4qgBzIbIKvfbqlIhf1jj5pVxWWQ13LjT4HVNVM%3D", "https://trakiotsolutions.blob.core.windows.net/agrodata/TrakIot%202/Aksh%20desh/139/739/965/recordingrecording_1721387560814.webm?se=2024-11-16T11%3A12%3A41Z&sp=r&sv=2024-05-04&sr=b&sig=16DQaUHc/yzFfq87OoPgttQraNo7R8CmvLs0LA2FDOo%3D"]
#             # Concatenate videos
#             # if not urls:
#             #     return Response(
#             #         {"error": "No video URLs found for the latest session"},
#             #         status=status.HTTP_404_NOT_FOUND,
#             #     )
#             # concatenated_path = concatenate_videos(urls)
#             video_clips = []
#             temp_files = []
            
#             try:

#                 for url in urls:
#                     # video_stream = stream_video(url)
#                     temp_file_name = stream_video_to_tempfile(url)
#                     temp_files.append(temp_file_name)
#                     video_clip = VideoFileClip(temp_file_name)
#                     video_clips.append(video_clip)

#                 final_clip = concatenate_videoclips(video_clips)

#                 output_buffer = io.BytesIO()
#                 final_clip.write_videofile(
#                     output_buffer, codec="libvpz", logger=None
#                 )

#                 output_buffer.seek(0)


#                 response = StreamingHttpResponse(
#                     generate_video_stream(output_buffer), content_type="video/webm"
#                 )

#                 response["Content-Disposition"] = 'inline; filename="video.webm"'
#                 return response
            
#             finally:
                
#                 for temp_file in temp_files:
#                     temp_file.close()
#                     os.unlink(temp_file.name)
#             # except Candidate.DoesNotExist:
#             #     return Response(
#             #         {"error": {"detail": "Candidate not found"}},
#             #         status=status.HTTP_404_NOT_FOUND,
#             #     )
#         except Exception as e:
#             return Response(
#                 {"error": {"detail": str(e)}},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

import imageio
import tempfile
import os

def concatenate_videos_imageio(urls):
    temp_files = []
    try:
        # Create a temporary file to store the concatenated video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            output_file_path = temp_file.name

        with imageio.get_writer(output_file_path, codec='libvpx') as writer:
            for url in urls:
                # Read video
                video = imageio.get_reader(url)
                for frame in video:
                    writer.append_data(frame)

        return output_file_path

    finally:
        for temp_file in temp_files:
            os.remove(temp_file.name)

# In your view
class StreamVideoView(APIView):
    # ... (rest of the code remains the same)
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
    ]  # Or leave empty for no authentication
    permission_classes = [AllowAny]


    def get(self, request):
        try:
            urls = ["https://trakiotsolutions.blob.core.windows.net/agrodata/TrakIot%202/Aksh%20desh/139/739/965/recordingrecording_1721387473255.webm?se=2024-11-16T11%3A11%3A13Z&sp=r&sv=2024-05-04&sr=b&sig=y4Ffe4qgBzIbIKvfbqlIhf1jj5pVxWWQ13LjT4HVNVM%3D", "https://trakiotsolutions.blob.core.windows.net/agrodata/TrakIot%202/Aksh%20desh/139/739/965/recordingrecording_1721387560814.webm?se=2024-11-16T11%3A12%3A41Z&sp=r&sv=2024-05-04&sr=b&sig=16DQaUHc/yzFfq87OoPgttQraNo7R8CmvLs0LA2FDOo%3D"]
            

            final_video_path = concatenate_videos_imageio(urls)

            with open(final_video_path, 'rb') as f:
                response = StreamingHttpResponse(
                    f, content_type="video/webm"
                )
                response["Content-Disposition"] = 'inline; filename="video.webm"'
                return response

        except Exception as e:
            # logger.error(f"Error occurred: {str(e)}", exc_info=True)
            return Response({"error": {"detail": str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if os.path.exists(final_video_path):
                os.remove(final_video_path)
