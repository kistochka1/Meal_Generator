from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)


dishes = ['Борщ', 'Пельмени', 'Цезарь', 'Паста Карбонара']  # начальные примеры


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Выбор блюда - Flask приложение</title>
    <style>
        * {
            box-sizing: border-box;
            font-family: system-ui, 'Segoe UI', 'Helvetica Neue', sans-serif;
        }

        body {
            background: linear-gradient(145deg, #f5f7fc 0%, #eef2f8 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .card {
            max-width: 650px;
            width: 100%;
            background: rgba(255, 255, 255, 0.94);
            border-radius: 48px;
            box-shadow: 0 20px 35px -12px rgba(0, 0, 0, 0.2);
            padding: 28px 24px 36px;
            border: 1px solid rgba(255, 255, 255, 0.6);
        }

        h1 {
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 8px 0;
            background: linear-gradient(135deg, #1e2b3c, #2c4c6e);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .sub {
            color: #5a6e7c;
            border-left: 4px solid #ffa270;
            padding-left: 14px;
            margin-bottom: 28px;
            font-weight: 450;
        }

        .add-section {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 32px;
        }

        .add-section input {
            flex: 3;
            min-width: 160px;
            padding: 14px 18px;
            font-size: 1rem;
            border: 1.5px solid #dce5ec;
            border-radius: 44px;
            background: white;
            transition: 0.2s;
            outline: none;
        }

        .add-section input:focus {
            border-color: #ff9f5b;
            box-shadow: 0 0 0 3px rgba(255, 159, 91, 0.2);
        }

        .add-section button {
            flex: 1;
            background: #2c4c6e;
            border: none;
            padding: 0 20px;
            border-radius: 44px;
            font-weight: 600;
            font-size: 1rem;
            color: white;
            cursor: pointer;
            transition: 0.2s;
        }

        .add-section button:hover {
            background: #1f3b57;
            transform: scale(0.97);
        }

        .list-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin: 12px 4px 12px 4px;
        }

        .list-header h2 {
            font-size: 1.4rem;
            font-weight: 600;
            margin: 0;
            color: #1e2f3c;
        }

        .clear-btn {
            background: none;
            border: none;
            color: #b91c1c;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            padding: 5px 12px;
            border-radius: 40px;
            transition: 0.2s;
        }

        .clear-btn:hover {
            background: #ffe6e6;
        }

        .dish-list {
            background: #f8fafd;
            border-radius: 32px;
            padding: 8px;
            margin: 12px 0 22px;
            border: 1px solid #e9edf2;
            max-height: 320px;
            overflow-y: auto;
        }

        .dish-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: white;
            margin: 8px 0;
            padding: 12px 18px;
            border-radius: 60px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
            border: 1px solid #eef2f8;
        }

        .dish-name {
            font-size: 1.1rem;
            font-weight: 500;
            color: #1f2e3a;
        }

        .remove-dish {
            background: #ffedea;
            border: none;
            font-size: 1.3rem;
            font-weight: bold;
            color: #c2410c;
            width: 36px;
            height: 36px;
            border-radius: 40px;
            cursor: pointer;
            transition: 0.15s;
        }

        .remove-dish:hover {
            background: #ffd8cf;
        }

        .empty-message {
            text-align: center;
            color: #8ea0ae;
            padding: 30px 20px;
            font-style: italic;
        }

        .action-area {
            text-align: center;
            margin: 20px 0 12px;
        }

        .pick-btn {
            background: linear-gradient(110deg, #ff884d, #ffb162);
            border: none;
            padding: 16px 32px;
            font-size: 1.3rem;
            font-weight: 700;
            border-radius: 60px;
            color: white;
            cursor: pointer;
            width: 100%;
            max-width: 280px;
            box-shadow: 0 12px 18px -10px rgba(255, 110, 28, 0.4);
            transition: 0.15s;
        }

        .pick-btn:active {
            transform: scale(0.97);
        }

        .result-card {
            background: #ecfdf5;
            margin-top: 25px;
            padding: 16px 20px;
            border-radius: 48px;
            text-align: center;
            border-left: 8px solid #ff9f5b;
        }

        .result-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #557c55;
            font-weight: 600;
        }

        .result-dish {
            font-size: 1.9rem;
            font-weight: 800;
            color: #1a3a3a;
            margin-top: 6px;
        }

        .status {
            font-size: 0.8rem;
            text-align: center;
            margin-top: 15px;
            color: #2c6e2c;
        }

        footer {
            font-size: 0.7rem;
            text-align: center;
            margin-top: 20px;
            color: #94a3b8;
        }
    </style>
</head>
<body>

<div class="card">
    <h1>🍲 Выбор блюда</h1>
    <div class="sub">Создай свой список — пусть судьба решит!</div>

    <div class="add-section">
        <input type="text" id="dishInput" placeholder="Например: Борщ, Пицца, Паста..." autocomplete="off">
        <button id="addBtn">➕ Добавить</button>
    </div>

    <div class="list-header">
        <h2>📋 Мой список</h2>
        <button id="clearAllBtn" class="clear-btn">Очистить всё</button>
    </div>

    <div id="dishListContainer" class="dish-list">
        <div class="empty-message">✨ Загрузка... ✨</div>
    </div>

    <div class="action-area">
        <button id="pickRandomBtn" class="pick-btn">🎲 Выбрать случайное блюдо</button>
    </div>

    <div id="resultBox" class="result-card" style="display: none;">
        <div class="result-label">🍽️ Сегодня на ужин:</div>
        <div class="result-dish" id="selectedDishName"></div>
    </div>

    <div id="serverStatus" class="status"></div>
    <footer>Список хранится на сервере (Flask) | Все изменения синхронизируются</footer>
</div>

<script>
    
    async function loadDishes() {
        try {
            const response = await fetch('/api/dishes');
            const dishes = await response.json();
            renderDishList(dishes);
            document.getElementById('serverStatus').innerHTML = '✅ Соединение с сервером установлено';
            document.getElementById('serverStatus').style.color = '#2c6e2c';
        } catch (error) {
            console.error('Ошибка загрузки:', error);
            document.getElementById('serverStatus').innerHTML = '❌ Ошибка соединения с сервером';
            document.getElementById('serverStatus').style.color = '#b91c1c';
        }
    }

    
    function renderDishList(dishes) {
        const container = document.getElementById('dishListContainer');

        if (dishes.length === 0) {
            container.innerHTML = '<div class="empty-message">🍽️ Список пуст. Добавьте любимые блюда!</div>';
            return;
        }

        const itemsHtml = dishes.map((dish, index) => `
            <div class="dish-item" data-index="${index}">
                <span class="dish-name">🍜 ${escapeHtml(dish)}</span>
                <button class="remove-dish" data-index="${index}" data-name="${escapeHtml(dish)}">✕</button>
            </div>
        `).join('');

        container.innerHTML = itemsHtml;

        
        document.querySelectorAll('.remove-dish').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const dishName = btn.getAttribute('data-name');
                if (confirm(`Удалить блюдо "${dishName}"?`)) {
                    await deleteDish(dishName);
                }
            });
        });
    }

    function escapeHtml(str) {
        return str.replace(/[&<>]/g, function(m) {
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        });
    }

    
    async function addDish() {
        const input = document.getElementById('dishInput');
        const dishName = input.value.trim();

        if (dishName === "") {
            alert("Пожалуйста, введите название блюда!");
            return;
        }

        try {
            const response = await fetch('/api/dishes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: dishName })
            });

            const result = await response.json();

            if (response.ok) {
                input.value = '';
                await loadDishes(); // Перезагружаем список
                document.getElementById('resultBox').style.display = 'none';
            } else {
                alert(result.error || 'Ошибка при добавлении');
            }
        } catch (error) {
            alert('Ошибка соединения с сервером');
        }
    }

    
    async function deleteDish(dishName) {
        try {
            const response = await fetch('/api/dishes', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: dishName })
            });

            if (response.ok) {
                await loadDishes();
                document.getElementById('resultBox').style.display = 'none';
            } else {
                const result = await response.json();
                alert(result.error || 'Ошибка при удалении');
            }
        } catch (error) {
            alert('Ошибка соединения с сервером');
        }
    }

    
    async function clearAllDishes() {
        if (!confirm("Вы уверены? Весь список блюд будет удалён.")) return;

        try {
            const response = await fetch('/api/dishes/clear', {
                method: 'DELETE'
            });

            if (response.ok) {
                await loadDishes();
                document.getElementById('resultBox').style.display = 'none';
            }
        } catch (error) {
            alert('Ошибка соединения с сервером');
        }
    }

    
    async function pickRandomDish() {
        try {
            const response = await fetch('/api/dishes/random');
            const result = await response.json();

            if (response.ok) {
                document.getElementById('selectedDishName').textContent = result.dish;
                document.getElementById('resultBox').style.display = 'block';

                // Анимация
                const resultBox = document.getElementById('resultBox');
                resultBox.style.transform = 'scale(1.01)';
                setTimeout(() => { resultBox.style.transform = ''; }, 150);
            } else {
                alert(result.error || 'Список пуст! Добавьте хотя бы одно блюдо.');
                document.getElementById('resultBox').style.display = 'none';
            }
        } catch (error) {
            alert('Ошибка соединения с сервером');
        }
    }

    
    document.getElementById('addBtn').addEventListener('click', addDish);
    document.getElementById('clearAllBtn').addEventListener('click', clearAllDishes);
    document.getElementById('pickRandomBtn').addEventListener('click', pickRandomDish);

    document.getElementById('dishInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addDish();
    });

    
    loadDishes();
</script>
</body>
</html>
"""


@app.route('/')
def index():

    return render_template_string(HTML_TEMPLATE)


@app.route('/api/dishes', methods=['GET'])
def get_dishes():

    return jsonify(dishes)


@app.route('/api/dishes', methods=['POST'])
def add_dish():

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

    data = request.get_json()
    dish_name = data.get('name', '').strip()

    if dish_name in dishes:
        dishes.remove(dish_name)
        return jsonify({'success': True, 'dish': dish_name})
    else:
        return jsonify({'error': 'Блюдо не найдено'}), 404


@app.route('/api/dishes/clear', methods=['DELETE'])
def clear_dishes():

    dishes.clear()
    return jsonify({'success': True, 'message': 'Список очищен'})


@app.route('/api/dishes/random', methods=['GET'])
def random_dish():

    if not dishes:
        return jsonify({'error': 'Список блюд пуст'}), 404

    chosen = random.choice(dishes)
    return jsonify({'dish': chosen})


if __name__ == '__main__':
    print("=" * 50)
    print("🍲 Приложение 'Выбор блюда' запущено!")
    print("📱 Откройте в браузере: http://127.0.0.1:5000")
    print("🔄 Для остановки сервера нажмите Ctrl+C")
    print("=" * 50)
    app.run(debug=True, port=5000)