import rospy

from app_manager_plugin import AppManagerPlugin

from gdrive_ros.srv import MultipleUpload
from gdrive_ros.srv import MultipleUploadRequest


class GdriveUploaderPlugin(AppManagerPlugin):
    def __init__(self):
        super(GdriveUploaderPlugin, self).__init__()

    @classmethod
    def app_manager_stop_plugin(cls, app, ctx):
        req = MultipleUploadRequest()
        req.file_paths = ctx['upload_file_paths']
        req.file_titles = ctx['upload_file_titles']
        req.parents_path = ctx['upload_parents_path']
        req.use_timestamp_folder = True
        req.use_timestamp_file_title = True
        gdrive_upload = rospy.ServiceProxy(
            ctx['upload_server_name'] + '/upload_multi',
            MultipleUpload
        )
        res = gdrive_upload(req)
        if all(res.successes):
            rospy.loginfo('Upload succeeded.')
        else:
            rospy.logerr('Upload failed')
        if 'upload_successes' in ctx:
            ctx['upload_successes'] += res.successes
        else:
            ctx['upload_successes'] = res.successes
        if 'upload_file_urls' in ctx:
            ctx['upload_file_urls'] += res.file_urls
        else:
            ctx['upload_file_urls'] = res.file_urls
        return ctx
