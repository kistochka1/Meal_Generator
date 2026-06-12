from flask import Flask, jsonify, request, send_file
import random
import os

app = Flask(__name__)

# Хранилище блюд (в памяти сервера)
dishes = ['Борщ', 'Пельмени', 'Цезарь', 'Паста Карбонара']

# Получаем абсолютный путь к текущей папке
current_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    """Отдаем index.html при заходе на главную страницу"""
    index_path = os.path.join(current_dir, 'index.html')
    if os.path.exists(index_path):
        return send_file(index_path)
    else:
        return f"Файл index.html не найден в папке: {current_dir}", 404


# API endpoints
@app.route('/api/dishes', methods=['GET'])
def get_dishes():
    """Получить список всех блюд"""
    return jsonify(dishes)


@app.route('/api/dishes', methods=['POST'])
def add_dish():
    """Добавить новое блюдо"""
    data = request.get_json()
    dish_name = data.get('name', '').strip()

    if not dish_name:
        return jsonify({'error': 'Название блюда не может быть пустым'}), 400

    if dish_name in dishes:
        return jsonify({'error': 'Такое блюдо уже существует'}), 400

    dishes.append(dish_name)
    return jsonify({'success': True, 'dish': dish_name, 'total': len(dishes)})


@app.route('/api/dishes', methods=['DELETE'])
def delete_dish():
    """Удалить конкретное блюдо"""
    data = request.get_json()
    dish_name = data.get('name', '').strip()

    if dish_name in dishes:
        dishes.remove(dish_name)
        return jsonify({'success': True, 'dish': dish_name})
    else:
        return jsonify({'error': 'Блюдо не найдено'}), 404


@app.route('/api/dishes/clear', methods=['DELETE'])
def clear_dishes():
    """Очистить весь список"""
    dishes.clear()
    return jsonify({'success': True, 'message': 'Список очищен'})


@app.route('/api/dishes/random', methods=['GET'])
def random_dish():
    """Выбрать случайное блюдо"""
    if not dishes:
        return jsonify({'error': 'Список блюд пуст'}), 404

    chosen = random.choice(dishes)
    return jsonify({'dish': chosen})


if __name__ == '__main__':
    print("=" * 60)
    print("🍲 Приложение 'Выбор блюда' запущено!")
    print(f"📁 Текущая папка: {current_dir}")
    print("📄 Проверяю наличие index.html...")

    index_path = os.path.join(current_dir, 'index.html')
    if os.path.exists(index_path):
        print("✅ index.html найден!")
    else:
        print("❌ index.html НЕ найден!")
        print(f"   Создайте файл {index_path}")

    print("\n🌐 Откройте в браузере: http://127.0.0.1:5000")
    print("🔄 Для остановки сервера нажмите Ctrl+C")
    print("=" * 60)
    app.run(debug=True, port=5000)