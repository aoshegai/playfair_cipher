from typing import Tuple, List

class PlayfairCipher:
    def __init__(self, key: str):
        self.key = self._normalize_key(key)
        self.matrix = self._generate_matrix()
    
    def _normalize_key(self, key: str) -> str:
        """Нормализует ключ: верхний регистр, заменяет J на I, удаляет дубликаты"""
        normalized = []
        seen = set()
        for char in key.upper():
            if char == 'J':
                char = 'I'
            if char.isalpha() and char not in seen:
                normalized.append(char)
                seen.add(char)
        return ''.join(normalized)
    
    def _generate_matrix(self) -> List[List[str]]:
        """Генерирует матрицу 5x5 на основе ключа"""
        # Добавляем остальные буквы алфавита (I и J объединены)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [c for c in alphabet if c not in self.key]
        all_letters = self.key + ''.join(remaining_letters)
        
        # Создаем матрицу 5x5
        matrix = []
        for i in range(5):
            row = all_letters[i*5 : (i+1)*5]
            matrix.append(list(row))
        return matrix
    
    def _find_position(self, char: str) -> Tuple[int, int]:
        """Находит позицию символа в матрице"""
        char = char.upper().replace('J', 'I')
        for i, row in enumerate(self.matrix):
            if char in row:
                return (i, row.index(char))
        raise ValueError(f"Character {char} not found in matrix")
    
    def _prepare_text(self, text: str) -> str:
        """Подготавливает текст для шифрования/дешифрования"""
        text = text.upper().replace('J', 'I')
        text = ''.join(c for c in text if c.isalpha())
        
        # Разбиваем на пары, добавляем X между одинаковыми буквами
        prepared = []
        i = 0
        while i < len(text):
            if i == len(text) - 1:
                prepared.append(text[i] + 'X')
                break
            if text[i] == text[i+1]:
                prepared.append(text[i] + 'X')
                i += 1
            else:
                prepared.append(text[i] + text[i+1])
                i += 2
        return ''.join(prepared)
    
    def encrypt(self, plaintext: str) -> str:
        """Шифрует текст"""
        prepared = self._prepare_text(plaintext)
        ciphertext = []
        
        for i in range(0, len(prepared), 2):
            a, b = prepared[i], prepared[i+1]
            row_a, col_a = self._find_position(a)
            row_b, col_b = self._find_position(b)
            
            if row_a == row_b:
                # Одна строка - сдвиг вправо
                ciphertext.append(self.matrix[row_a][(col_a + 1) % 5])
                ciphertext.append(self.matrix[row_b][(col_b + 1) % 5])
            elif col_a == col_b:
                # Один столбец - сдвиг вниз
                ciphertext.append(self.matrix[(row_a + 1) % 5][col_a])
                ciphertext.append(self.matrix[(row_b + 1) % 5][col_b])
            else:
                # Прямоугольник - противоположные углы
                ciphertext.append(self.matrix[row_a][col_b])
                ciphertext.append(self.matrix[row_b][col_a])
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str) -> str:
        """Дешифрует текст"""
        prepared = self._prepare_text(ciphertext)
        plaintext = []
        
        for i in range(0, len(prepared), 2):
            a, b = prepared[i], prepared[i+1]
            row_a, col_a = self._find_position(a)
            row_b, col_b = self._find_position(b)
            
            if row_a == row_b:
                # Одна строка - сдвиг влево
                plaintext.append(self.matrix[row_a][(col_a - 1) % 5])
                plaintext.append(self.matrix[row_b][(col_b - 1) % 5])
            elif col_a == col_b:
                # Один столбец - сдвиг вверх
                plaintext.append(self.matrix[(row_a - 1) % 5][col_a])
                plaintext.append(self.matrix[(row_b - 1) % 5][col_b])
            else:
                # Прямоугольник - противоположные углы
                plaintext.append(self.matrix[row_a][col_b])
                plaintext.append(self.matrix[row_b][col_a])
        
        # Удаляем добавленные X
        result = ''.join(plaintext)
        if result.endswith('X'):
            result = result[:-1]
        
        # Удаляем X между повторяющимися буквами
        final = []
        i = 0
        while i < len(result):
            if i < len(result) - 2 and result[i] == result[i+2] and result[i+1] == 'X':
                final.append(result[i])
                final.append(result[i+2])
                i += 3
            else:
                final.append(result[i])
                i += 1
        
        return ''.join(final)