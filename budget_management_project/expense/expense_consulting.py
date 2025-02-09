import calendar
from datetime import date

class Consulting:
    category = ['total_amount','tuition_fee', 'book_fee', 'courses_fee', 'communication_fee',
            'food_fee', 'transportation_fee', 'leisure_fee', 'self_development_fee', 'club_fee', 'preparation_fee', 
            'dormitory_fee', 'healthcare_fee']
    def __init__(self, total_amount, tuition_fee, book_fee,
                courses_fee, communication_fee, food_fee, transportation_fee, leisure_fee, self_development_fee, club_fee,
                preparation_fee = None, dormitory_fee = None, healthcare_fee = None):
        local_dic = locals()
        for cates in Consulting.category:
            setattr(self, cates, local_dic.get(cates, 0))
    def calculate_daily_available(self):
        """
        오늘 이후 남은 일수를 기준으로 현재 total_amount에서 하루 사용 가능한 금액을 각 카테고리 별로 계산합니다.
        """
        __day = date.today()
        __month_days = calendar.monthrange(__day.year, __day.month)[1]
        remaining_days = max(1, __month_days-__day.day)
        # 오늘 소비 후, 내일부터 사용하므로 남은 날짜 수는 (month_days - today.day)
        daily_available = self.total_amount // remaining_days
        category_fee = {}
        for cates in Consulting.category[1:]:
            cates_fee = getattr(self, cates)
            if self.total_amount > 0:
                category_available = round(daily_available * (cates_fee / self.total_amount))
            else:
                category_available = 0
            category_fee[cates] = category_available
        return daily_available, category_fee