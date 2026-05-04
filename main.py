import re
import json
import os

class KoNormalizationProject:
    def __init__(self, mapping_path='mapping.json'):
        self.mapping_path = mapping_path
        self.word_map = self._load_mapping()
        self.pattern = self._compile_pattern()

    def _load_mapping(self):
        """JSON 파일에서 매핑 데이터를 로드합니다."""
        if not os.path.exists(self.mapping_path):
            # 파일이 없을 경우 기본값 생성
            return {"열공": "hard study", "가즈아": "let's go"}
        
        with open(self.mapping_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _compile_pattern(self):
        """사전의 키값들을 정규표현식 패턴으로 컴파일합니다."""
        if not self.word_map:
            return None
        # 단어 길이가 긴 순서대로 정렬 (중복 매칭 방지: '열공중'이 '열공'보다 먼저 매칭되게 함)
        sorted_keys = sorted(self.word_map.keys(), key=len, reverse=True)
        # 각 키를 escape 처리하여 특수문자 오류 방지
        pattern_str = "|".join(re.escape(key) for key in sorted_keys)
        return re.compile(pattern_str)

    def normalize(self, text):
        """입력된 문장을 정규화/번역합니다."""
        if not self.pattern or not text:
            return text
        
        # 패턴에 맞는 단어를 찾으면 dictionary에서 값을 가져와 치환
        return self.pattern.sub(lambda m: self.word_map[m.group(0)], text)

    def add_word(self, ko, en):
        """새로운 단어 쌍을 사전에 추가합니다."""
        self.word_map[ko] = en
        self._save_mapping()
        self.pattern = self._compile_pattern() # 패턴 재컴파일

    def _save_mapping(self):
        """변경된 사전을 파일로 저장합니다."""
        with open(self.mapping_path, 'w', encoding='utf-8') as f:
            json.dump(self.word_map, f, ensure_ascii=False, indent=2)

# --- 실행 예시 ---
if __name__ == "__main__":
    translator = KoNormalizationProject()

    test_sentences = [
        "이번 시험 열공해서 가즈아!",
        "오늘 회의 알잘딱깔센 하게 끝냈다.",
        "그건 좀 킹받네 진짜.",
        "문법 틀리면 않되니까 조심해."
    ]

    print("=== 변환 결과 ===")
    for sentence in test_sentences:
        result = translator.normalize(sentence)
        print(f"Original: {sentence}")
        print(f"Cleaned : {result}\n")
