import unittest
from unittest.mock import patch, call
import os
import subprocess
from filmflix.tasks import convert_480p, convert_720p, delete_480p, delete_720p

class TestVideoTasks(unittest.TestCase):

    @patch('subprocess.run')
    def test_convert_480p(self, mock_run):
        source = "test_video.mp4"
        convert_480p(source)
        
        target = source + "_480p.mp4"
        cmd = f'ffmpeg -i "{source}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
        
        mock_run.assert_called_once_with(cmd, shell=True)

    @patch('subprocess.run')
    def test_convert_720p(self, mock_run):
        source = "test_video.mp4"
        convert_720p(source)
        
        target = source + "_720p.mp4"
        cmd = f'ffmpeg -i "{source}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
        
        mock_run.assert_called_once_with(cmd, shell=True)

    @patch('os.remove')
    def test_delete_480p(self, mock_remove):
        source = "test_video.mp4"
        delete_480p(source)
        
        target = source + "_480p.mp4"
        mock_remove.assert_called_once_with(target)

    @patch('os.remove')
    def test_delete_720p(self, mock_remove):
        source = "test_video.mp4"
        delete_720p(source)
        
        target = source + "_720p.mp4"
        mock_remove.assert_called_once_with(target)

if __name__ == '__main__':
    unittest.main()