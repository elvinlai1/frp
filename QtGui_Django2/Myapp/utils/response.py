from rest_framework.renderers import JSONRenderer
import logging

logger = logging.getLogger('django')


class custom_renderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            logger.info("=====================message=====================\n")
            if isinstance(data, dict):
                msg = data.pop('message', 'success')
                code = data.pop('code', renderer_context["response"].status_code)
            else:
                msg = 'success'
                code = renderer_context["response"].status_code
            ret = {
                'msg': msg,
                'code': code,
                'data': data,
            }
            logger.info(ret)
            logger.info("\n")
            logger.info("=====================message=====================")
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
