from django.core.cache import cache
from .models import BoardSetting

def get_board_setting():
    """
    보드 설정 저장
    """
    setting = cache.get("board_setting")

    if setting is None:
        setting = BoardSetting.objects.first()
        if setting:
            cache.set("board_setting", setting, timeout=3600)  # 다시 캐싱

    return setting