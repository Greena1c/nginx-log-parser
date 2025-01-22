# nginx-log-parser
## **Nginx Log Parser**

Цей проект аналізує логи Nginx, фільтрує їх за заданими параметрами (HTTP-статус, дата тощо) і записує результати у файли CSV. Також підтримується автоматичне комітування змін у Git.

---

### **Функціонал**

- Аналіз логів Nginx із регулярним виразом.
- Фільтрація логів за:
  - HTTP-статусом (наприклад, `400-500`).
  - Датою (наприклад, `26/04/2021`).
- Сортування результатів за будь-яким полем (наприклад, `Status`, `Size`).
- Збереження:
  - Усі логи (`all_logs.csv`).
  - Відфільтровані логи (`filtered_logs.csv`).
- Автоматичний коміт і пуш у Git.

---

### **Вимоги**

- **Python 3.12+**
- **Docker** (опційно)

---

### **Установка**

1. Клонувати репозиторій:
   ```bash
   git clone https://github.com/your-repo/nginx-log-parser.git
   cd nginx-log-parser
   ```

2. Встановити залежності (якщо використовуєте локально):
   ```bash
   pip install -r requirements.txt
   ```

---

### **Запуск**

#### **Локально**

1. **Без фільтрів:**
   ```bash
   python parst.py
   ```

2. **З фільтрами:**
   - За статусом:
     ```bash
     python parst.py --status-range 400-500
     ```
   - За датою:
     ```bash
     python parst.py --date 26/04/2021
     ```
   - Зі статусом, датою та сортуванням:
     ```bash
     python parst.py --status-range 400-500 --date 26/04/2021 --sort-by Size --sort-order asc
     ```

#### **У Docker**

1. **Зібрати образ:**
   ```bash
   docker build -t nginx-log-parser .
   ```

2. **Запуск без фільтрів:**
   ```bash
   docker run --rm nginx-log-parser
   ```

3. **Запуск із фільтрами:**
   ```bash
   docker run --rm nginx-log-parser --status-range 400-500 --date 26/04/2021
   ```

4. **Передача змінних середовища для Git:**
   ```bash
   docker run --rm -e GIT_USER_NAME="Your Name" -e GIT_USER_EMAIL="your.email@example.com" nginx-log-parser
   ```

---

### **Файли**

- `nginx.log` — вхідний файл із логами Nginx.
- `all_logs.csv` — усі логи без фільтрації.
- `filtered_logs.csv` — відфільтровані результати.

---

### **Додатково**

- **Git-інтеграція:** автоматично додає, комітить і пушить результати до вашого репозиторію.
- **Підтримка Docker:** спрощує розгортання і запуск.

---

### **Приклади**

1. **Без фільтрів:**
   ```bash
   python parst.py
   ```
   Результат: усі 89 рядків логів записані в `all_logs.csv` і `filtered_logs.csv`.

2. **Зі статусом 400-500:**
   ```bash
   python parst.py --status-range 400-500
   ```
   Результат: `filtered_logs.csv` містить тільки рядки зі статусами 400-500.

---

Серій Щедрик

