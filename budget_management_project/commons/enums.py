import enum
import random
import json

class CustomEnum(enum.Enum):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    @classmethod
    def from_code(cls, code):
        """code 값으로 Enum 멤버 찾기"""
        for member in cls:
            if member.code == code:
                return member
        raise ValueError(f"{code}에 해당하는 Enum 멤버가 없습니다.")

    @classmethod
    def from_description(cls, description):
        """description 값으로 Enum 멤버 찾기"""
        for member in cls:
            if member.description == description:
                return member
        raise ValueError(f"'{description}'에 해당하는 Enum 멤버가 없습니다.")

    @classmethod
    def random_member(cls):
        """랜덤으로 Enum 멤버 하나 반환"""
        return random.choice(list(cls))

    @classmethod
    def next_member(cls, current_code):
        """현재 코드의 다음 Enum 멤버 반환 (순환 지원)"""
        members = list(cls)
        for i, member in enumerate(members):
            if member.code == current_code:
                return members[(i + 1) % len(members)]  # 순환
        raise ValueError(f"{current_code}에 해당하는 Enum 멤버가 없습니다.")

    @classmethod
    def previous_member(cls, current_code):
        """현재 코드의 이전 Enum 멤버 반환 (순환 지원)"""
        members = list(cls)
        for i, member in enumerate(members):
            if member.code == current_code:
                return members[(i - 1) % len(members)]  # 순환
        raise ValueError(f"{current_code}에 해당하는 Enum 멤버가 없습니다.")

    @classmethod
    def json(cls):
        """Enum을 JSON 형태로 변환"""
        return json.dumps({member.code: member.description for member in cls}, ensure_ascii=False)

    @classmethod
    def by_index(cls, index):
        """리스트 인덱스로 Enum 멤버 찾기"""
        members = list(cls)
        if 0 <= index < len(members):
            return members[index]
        raise IndexError(f"인덱스 {index}가 범위를 벗어났습니다.")

    @classmethod
    def length(cls):
        """Enum 멤버 개수 반환"""
        return len(cls)

    @classmethod
    def items(cls):
        """(name, code, description) 리스트 반환"""
        return [(member.name, member.code, member.description) for member in cls]

    @classmethod
    def reverse_lookup(cls, code_or_description):
        """code 또는 description으로 Enum 멤버 찾기"""
        for member in cls:
            if member.code == code_or_description or member.description == code_or_description:
                return member
        raise ValueError(f"{code_or_description}에 해당하는 Enum 멤버가 없습니다.")

    def __str__(self):
        """문자열 출력 형태 변경 (예: '1: 빨강')"""
        return f"{self.code}: {self.description}"

    def __repr__(self):
        """객체 표현 방식 변경"""
        return f"<{self.__class__.__name__}.{self.name}: {self.code} ({self.description})>"

    def __eq__(self, other):
        """== 연산자 지원 (예: Color.RED == 1)"""
        if isinstance(other, int):
            return self.code == other
        if isinstance(other, CustomEnum):
            return self.code == other.code
        return NotImplemented

# # ✅ 사용 예시 - Color Enum 정의
# class Color(CustomEnum):
#     RED = (1, "빨강")
#     BLUE = (2, "파랑")
#     GREEN = (3, "초록")
#     YELLOW = (4, "노랑")

# # ✅ 테스트 코드
# print(Color.from_code(1))  # 1: 빨강
# print(Color.from_description("파랑"))  # 2: 파랑
# print(Color.random_member())  # 랜덤한 색상 출력
# print(Color.next_member(3))  # 초록 → 노랑
# print(Color.previous_member(1))  # 빨강 → 노랑 (순환됨)
# print(Color.json())  # JSON 형식 출력: {"1": "빨강", "2": "파랑", "3": "초록", "4": "노랑"}
# print(Color.by_index(2))  # 초록
# print(Color.length())  # 4
# print(Color.items())  # [('RED', 1, '빨강'), ('BLUE', 2, '파랑'), ('GREEN', 3, '초록'), ('YELLOW', 4, '노랑')]
# print(Color.reverse_lookup("초록"))  # 3: 초록
# print(Color.reverse_lookup(2))  # 2: 파랑

# # ✅ == 연산 지원
# print(Color.RED == 1)       # True
# print(Color.RED == Color.RED) # True
# print(Color.RED == Color.BLUE) # False