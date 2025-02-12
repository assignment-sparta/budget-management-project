from budget_management_project.commons.enums import CustomEnum

class CategoryType(CustomEnum):
    ETC = (1, '기타')
    TUITION_FEE = (2, '학비')
    BOOK_FEE = (3, '교재비')
    COURSES_FEE = (4, '인강비')
    COMMUNICATION_FEE = (5, '통신요금')
    FOOD_FEE = (6, '식비')
    TRANSPORTATION_FEE = (7, '대중교통비')
    LEISURE_FEE = (8, '여가생활비')
    SELF_DEVELOPMENT_FEE = (9, '자기개발비')
    CLUB_FEE = (10, '동아리 비용')
    PREPARATION_FEE = (11, '개인 물품비')
    DORMITORY_FEE = (12, '기숙사비')
    HEALTHCARE_FEE = (13, '건강 비용')
